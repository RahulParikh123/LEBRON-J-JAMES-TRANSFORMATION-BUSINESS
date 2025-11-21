"""
Main entry point for the Enterprise Data Transformation Platform
"""
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from loguru import logger

from src.ingestion.registry import FormatRegistry
from src.cleaning.pipeline import CleaningPipeline
from src.redaction.pipeline import RedactionPipeline
from src.compliance.checker import ComplianceChecker
from src.structuring.llm_formatter import LLMFormatter
from src.output.writer import OutputWriter
from src.batch import BatchProcessor, FileScanner
from src.ingestion.metadata_extractor import MetadataExtractor
from src.relationships import RelationshipDetector, RelationshipGraph
from src.structuring.agentic_formatter import AgenticAIFormatter
from typing import List


class DataTransformationPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize components
        self.registry = FormatRegistry()
        self.cleaning_pipeline = CleaningPipeline(self.config.get('cleaning', {}))
        self.redaction_pipeline = RedactionPipeline(self.config.get('redaction', {}))
        self.compliance_checker = ComplianceChecker(self.config.get('compliance', {}))
        self.llm_formatter = LLMFormatter(self.config.get('llm_formatting', {}))
        self.output_writer = OutputWriter(self.config.get('output', {}))
        
        # Batch processing components
        self.batch_processor = BatchProcessor(self.config.get('batch', {}))
        self.metadata_extractor = MetadataExtractor(self.config.get('metadata', {}))
        self.relationship_detector = RelationshipDetector(self.config.get('relationships', {}))
        self.agentic_formatter = AgenticAIFormatter(self.config.get('agentic_formatting', {}))
        
        # Setup logging
        log_level = self.config.get('log_level', 'INFO')
        logger.remove()
        logger.add(sys.stderr, level=log_level)
    
    def process(self, input_path: str, output_path: Optional[str] = None,
               narration_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process data through the complete pipeline
        
        Args:
            input_path: Path to input file or database connection string
            output_path: Path for output file
            narration_path: Optional path to human narration file
        
        Returns:
            Processing results
        """
        logger.info(f"Starting data transformation for: {input_path}")
        
        results = {
            'input_path': input_path,
            'steps': [],
            'output_path': None,
            'stats': {}
        }
        
        try:
            # Step 1: Ingestion
            logger.info("Step 1: Ingesting data...")
            handler = self.registry.get_handler(input_path)
            if not handler:
                raise ValueError(f"No handler found for: {input_path}")
            
            ingestion_result = handler.extract(input_path)
            results['steps'].append({
                'step': 'ingestion',
                'status': 'success',
                'metadata': ingestion_result.get('metadata', {})
            })
            
            data = ingestion_result.get('data')
            text_content = ingestion_result.get('text_content', [])
            structure = ingestion_result.get('structure', {})
            
            # Step 2: Cleaning
            logger.info("Step 2: Cleaning data...")
            cleaning_result = self.cleaning_pipeline.clean(
                data,
                schema=self.config.get('schema'),
                key_columns=self.config.get('key_columns')
            )
            results['steps'].append({
                'step': 'cleaning',
                'status': 'success',
                'stats': cleaning_result.get('stats', {})
            })
            
            cleaned_data = cleaning_result.get('cleaned_data')
            
            # Step 3: Redaction
            logger.info("Step 3: Detecting and redacting PII/PHI...")
            redaction_result = self.redaction_pipeline.process(
                cleaned_data,
                entity_types=self.config.get('entity_types'),
                columns=self.config.get('redaction_columns')
            )
            results['steps'].append({
                'step': 'redaction',
                'status': 'success',
                'stats': redaction_result.get('stats', {})
            })
            
            processed_data = redaction_result.get('processed_data')
            detected_entities = redaction_result.get('detection', {}).get('entities', [])
            
            # Store detailed redaction info for reporting
            redaction_details = {
                'entities_detected': redaction_result.get('detection', {}).get('entities', []),
                'by_column': redaction_result.get('detection', {}).get('by_column', {}),
                'entity_locations': []
            }
            
            # Extract entity locations (row, column, position) for DataFrame
            if isinstance(cleaned_data, pd.DataFrame) and detected_entities:
                for entity in detected_entities:
                    if 'row' in entity and 'column' in entity:
                        redaction_details['entity_locations'].append({
                            'type': entity.get('type'),
                            'row': entity.get('row'),
                            'column': entity.get('column'),
                            'text': entity.get('text', '')[:50],  # First 50 chars
                            'score': entity.get('score', 0)
                        })
            
            # Step 4: Compliance checking
            logger.info("Step 4: Checking compliance...")
            compliance_result = self.compliance_checker.check(
                processed_data,
                detected_entities=detected_entities,
                metadata=ingestion_result.get('metadata')
            )
            results['steps'].append({
                'step': 'compliance',
                'status': 'success',
                'result': compliance_result
            })
            
            # Step 5: Format for LLM training
            logger.info("Step 5: Formatting for LLM training...")
            
            # Load narration if provided
            narration = None
            if narration_path and Path(narration_path).exists():
                with open(narration_path, 'r', encoding='utf-8') as f:
                    narration = f.read()
            
            llm_formatted = self.llm_formatter.format_for_training(
                processed_data,
                text_content=text_content,
                narration=narration,
                metadata={
                    'structure': structure,
                    'processing_stats': {
                        'cleaning': cleaning_result.get('stats', {}),
                        'redaction': {
                            **redaction_result.get('stats', {}),
                            'entity_locations': redaction_details.get('entity_locations', []),
                            'by_column': redaction_details.get('by_column', {})
                        },
                        'compliance': compliance_result.get('summary', {})
                    }
                }
            )
            
            results['steps'].append({
                'step': 'llm_formatting',
                'status': 'success',
                'format': llm_formatted.get('format'),
                'record_count': llm_formatted.get('record_count', 0)
            })
            
            # Step 6: Write output
            logger.info("Step 6: Writing output...")
            if output_path:
                output_file = self.output_writer.write(
                    llm_formatted.get('content') or processed_data,
                    output_path,
                    format=self.config.get('output_format', 'auto')
                )
                results['output_path'] = str(output_file)
            else:
                # Auto-generate output path
                input_path_obj = Path(input_path)
                output_file = self.output_writer.write(
                    llm_formatted.get('content') or processed_data,
                    f"{input_path_obj.stem}_processed.jsonl",
                    format='jsonl'
                )
                results['output_path'] = str(output_file)
            
            results['steps'].append({
                'step': 'output',
                'status': 'success',
                'output_path': results['output_path']
            })
            
            # Aggregate statistics
            results['stats'] = {
                'total_steps': len(results['steps']),
                'successful_steps': sum(1 for s in results['steps'] if s.get('status') == 'success'),
                'entities_detected': redaction_result.get('stats', {}).get('entities_detected', 0),
                'entities_redacted': redaction_result.get('stats', {}).get('entities_redacted', 0),
                'compliance_issues': compliance_result.get('summary', {}).get('total_issues', 0),
                'output_records': llm_formatted.get('record_count', 0)
            }
            
            logger.info("Data transformation completed successfully!")
            logger.info(f"Output written to: {results['output_path']}")
            
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            results['error'] = str(e)
            results['status'] = 'failed'
            raise
        
        results['status'] = 'success'
        return results
    
    def process_batch(
        self,
        input_directory: str,
        output_directory: str = "output",
        detect_relationships: bool = True,
        patterns: Optional[List[str]] = None,
        recursive: bool = True
    ) -> Dict[str, Any]:
        """
        Process multiple files in batch with relationship detection
        
        Args:
            input_directory: Directory containing files to process
            output_directory: Directory for output files
            detect_relationships: Whether to detect relationships between files
            patterns: File patterns to match (default: all supported)
            recursive: Whether to scan subdirectories
        
        Returns:
            Batch processing results with relationships
        """
        logger.info(f"Starting batch processing: {input_directory}")
        
        # Process files through batch processor
        def process_single_file(file_path: str, output_dir: str) -> Dict[str, Any]:
            """Process a single file"""
            output_path = Path(output_dir) / "processed" / f"{Path(file_path).stem}_processed.jsonl"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            result = self.process(
                input_path=file_path,
                output_path=str(output_path)
            )
            return result
        
        # Run batch processing
        batch_results = self.batch_processor.process_directory(
            input_directory=input_directory,
            output_directory=output_directory,
            patterns=patterns,
            recursive=recursive,
            process_func=process_single_file
        )
        
        # Extract metadata for all processed files
        logger.info("Extracting metadata from processed files...")
        file_metadata_list = []
        processed_data_map = {}
        
        for file_path in batch_results.get('completed_files', []):
            try:
                metadata = self.metadata_extractor.extract(file_path)
                metadata_dict = self.metadata_extractor.to_dict(metadata)
                file_metadata_list.append(metadata_dict)
                
                # Load actual processed data content
                output_path = Path(output_directory) / "output" / "processed" / f"{Path(file_path).stem}_processed.jsonl"
                if not output_path.exists():
                    # Try alternative path
                    output_path = Path(output_directory) / "processed" / f"{Path(file_path).stem}_processed.jsonl"
                
                if output_path.exists():
                    # Read the processed file content
                    processed_data = {}
                    text_content = []
                    
                    with open(output_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    record = json.loads(line)
                                    value_str = record.get('value', '{}')
                                    value_data = json.loads(value_str) if isinstance(value_str, str) else value_str
                                    
                                    # Extract structured data and text representation
                                    if 'structured_data' in value_data:
                                        processed_data = value_data.get('structured_data', {})
                                    if 'text_representation' in value_data:
                                        text_content.append(value_data.get('text_representation', ''))
                                except (json.JSONDecodeError, KeyError):
                                    continue
                    
                    processed_data_map[metadata_dict['file_id']] = {
                        'output_path': str(output_path),
                        'data': processed_data,
                        'text_content': '\n\n'.join(text_content) if text_content else ''
                    }
                else:
                    # Fallback: just store path
                    processed_data_map[metadata_dict['file_id']] = {
                        'output_path': str(output_path),
                        'data': None,
                        'text_content': ''
                    }
            except Exception as e:
                logger.warning(f"Failed to extract metadata from {file_path}: {e}")
        
        # Detect relationships if enabled
        relationships = []
        relationship_graph = None
        
        if detect_relationships and len(file_metadata_list) > 1:
            logger.info("Detecting relationships between files...")
            relationships = self.relationship_detector.detect_relationships(file_metadata_list)
            
            # Build relationship graph
            relationship_graph = RelationshipGraph()
            relationship_graph.build_from_metadata_and_relationships(
                file_metadata_list,
                relationships,
                processed_data_map
            )
            
            # Save relationship graph
            graph_output = Path(output_directory) / "relationships" / "relationship_graph.json"
            graph_output.parent.mkdir(parents=True, exist_ok=True)
            relationship_graph.save(str(graph_output))
            
            # Save relationship summary
            summary = self.relationship_detector.get_relationship_summary(relationships)
            summary_output = Path(output_directory) / "relationships" / "relationships_summary.json"
            with open(summary_output, 'w') as f:
                import json
                json.dump(summary, f, indent=2)
        
        # Save metadata index
        metadata_output = Path(output_directory) / "metadata" / "file_metadata.json"
        metadata_output.parent.mkdir(parents=True, exist_ok=True)
        with open(metadata_output, 'w') as f:
            import json
            json.dump(file_metadata_list, f, indent=2, default=str)
        
        # Generate agentic AI training data if relationships detected
        agentic_output = None
        if relationships and relationship_graph:
            logger.info("Generating agentic AI training data...")
            
            # Prepare file data list with processed data
            file_data_list = []
            for metadata in file_metadata_list:
                file_id = metadata.get('file_id')
                file_data_list.append({
                    'file_id': file_id,
                    'metadata': metadata,
                    'processed_data': processed_data_map.get(file_id, {})
                })
            
            # Format for agentic AI
            agentic_data = self.agentic_formatter.format_for_agentic_ai(
                file_data_list,
                relationship_graph.to_dict()
            )
            
            # Save agentic AI training data
            agentic_output = Path(output_directory) / "agentic_ai" / "training_data.jsonl"
            agentic_output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(agentic_output, 'w', encoding='utf-8') as f:
                for record in agentic_data.get('content', []):
                    f.write(json.dumps(record, default=str, ensure_ascii=False) + '\n')
        
        # Create summary
        summary = {
            'status': 'completed',
            'batch_results': batch_results,
            'files_processed': len(file_metadata_list),
            'relationships_found': len(relationships),
            'output_directory': output_directory,
            'relationship_graph': str(Path(output_directory) / "relationships" / "relationship_graph.json") if relationship_graph else None,
            'agentic_ai_output': str(agentic_output) if agentic_output else None
        }
        
        # Save summary
        summary_output = Path(output_directory) / "summary.json"
        with open(summary_output, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Batch processing completed: {len(file_metadata_list)} files, {len(relationships)} relationships")
        
        return summary


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Enterprise Data Transformation Platform'
    )
    parser.add_argument('--input', '-i', required=True,
                       help='Input file path or database connection string')
    parser.add_argument('--output', '-o',
                       help='Output file path (auto-generated if not provided)')
    parser.add_argument('--narration', '-n',
                       help='Path to human narration file')
    parser.add_argument('--config', '-c',
                       help='Path to configuration YAML file')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    config['log_level'] = args.log_level
    
    # Initialize and run pipeline
    pipeline = DataTransformationPipeline(config)
    results = pipeline.process(
        input_path=args.input,
        output_path=args.output,
        narration_path=args.narration
    )
    
    # Print summary
    print("\n" + "="*60)
    print("Data Transformation Summary")
    print("="*60)
    print(f"Status: {results['status']}")
    print(f"Output: {results.get('output_path', 'N/A')}")
    print(f"\nStatistics:")
    for key, value in results.get('stats', {}).items():
        print(f"  {key}: {value}")
    print("="*60)
    
    return 0 if results['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())

