"""
LLM formatter - format data optimally for LLM training
Supports structured data + text + human narration
"""
from typing import Any, Dict, List, Optional
import pandas as pd
import json
from pathlib import Path


class LLMFormatter:
    """Format data for LLM training with flexible structure"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.output_format = self.config.get('output_format', 'jsonl')
        self.include_text = self.config.get('include_text', True)
        self.include_structure = self.config.get('include_structure', True)
        self.narration_path = self.config.get('narration_path', None)
    
    def format_for_training(self, data: Any, text_content: Optional[List[str]] = None,
                           narration: Optional[str] = None,
                           metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Format data for LLM training
        
        Args:
            data: Structured data (DataFrame, list, dict)
            text_content: Text representations of the data
            narration: Human narration/description
            metadata: Additional metadata
        
        Returns:
            Formatted training data
        """
        # Combine structured data, text, and narration
        training_records = []
        
        # Convert data to records
        if isinstance(data, pd.DataFrame):
            records = data.to_dict('records')
        elif isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
        else:
            records = [{'value': data}]
        
        # Create training records
        for idx, record in enumerate(records):
            training_record = {
                'id': f"record_{idx}",
                'structured_data': record
            }
            
            # Add text representation if available
            if text_content and idx < len(text_content):
                training_record['text_representation'] = text_content[idx]
            elif text_content:
                # Use first text if available
                training_record['text_representation'] = text_content[0]
            
            # Add narration if available
            if narration:
                training_record['human_narration'] = narration
            elif self.narration_path and Path(self.narration_path).exists():
                with open(self.narration_path, 'r', encoding='utf-8') as f:
                    training_record['human_narration'] = f.read()
            
            # Add metadata
            if metadata:
                training_record['metadata'] = metadata
            
            training_records.append(training_record)
        
        # Format according to output format
        if self.output_format == 'jsonl':
            return self._format_jsonl(training_records)
        elif self.output_format == 'json':
            return self._format_json(training_records)
        elif self.output_format == 'text':
            return self._format_text(training_records)
        else:
            return self._format_jsonl(training_records)  # Default
    
    def _format_jsonl(self, records: List[Dict]) -> Dict[str, Any]:
        """Format as JSONL for training"""
        jsonl_lines = [json.dumps(record, default=str, ensure_ascii=False) 
                       for record in records]
        jsonl_content = '\n'.join(jsonl_lines)
        
        return {
            'format': 'jsonl',
            'content': jsonl_content,
            'record_count': len(records),
            'metadata': {
                'format': 'jsonl',
                'encoding': 'utf-8',
                'training_ready': True
            }
        }
    
    def _format_json(self, records: List[Dict]) -> Dict[str, Any]:
        """Format as JSON for training"""
        json_content = json.dumps(records, indent=2, default=str, ensure_ascii=False)
        
        return {
            'format': 'json',
            'content': json_content,
            'record_count': len(records),
            'metadata': {
                'format': 'json',
                'encoding': 'utf-8',
                'training_ready': True
            }
        }
    
    def _format_text(self, records: List[Dict]) -> Dict[str, Any]:
        """Format as text for training (conversational format)"""
        text_lines = []
        
        for record in records:
            # Structured data section
            if 'structured_data' in record:
                text_lines.append("## Structured Data")
                text_lines.append(json.dumps(record['structured_data'], indent=2, default=str))
                text_lines.append("")
            
            # Text representation section
            if 'text_representation' in record:
                text_lines.append("## Text Representation")
                text_lines.append(record['text_representation'])
                text_lines.append("")
            
            # Human narration section
            if 'human_narration' in record:
                text_lines.append("## Human Narration")
                text_lines.append(record['human_narration'])
                text_lines.append("")
            
            text_lines.append("---")
            text_lines.append("")
        
        text_content = '\n'.join(text_lines)
        
        return {
            'format': 'text',
            'content': text_content,
            'record_count': len(records),
            'metadata': {
                'format': 'text',
                'encoding': 'utf-8',
                'training_ready': True
            }
        }
    
    def create_training_prompt(self, record: Dict, task_type: str = 'general') -> str:
        """
        Create a training prompt from a record
        
        Args:
            record: Training record
            task_type: Type of training task ('general', 'qa', 'summarization', etc.)
        """
        prompt_parts = []
        
        if task_type == 'qa':
            # Question-answering format
            if 'human_narration' in record:
                prompt_parts.append(f"Context: {record['human_narration']}")
            if 'text_representation' in record:
                prompt_parts.append(f"Data: {record['text_representation']}")
            if 'structured_data' in record:
                prompt_parts.append(f"Structured: {json.dumps(record['structured_data'], default=str)}")
        
        elif task_type == 'summarization':
            # Summarization format
            if 'structured_data' in record:
                prompt_parts.append(f"Data to summarize:\n{json.dumps(record['structured_data'], indent=2, default=str)}")
            if 'human_narration' in record:
                prompt_parts.append(f"Summary: {record['human_narration']}")
        
        else:
            # General format
            if 'structured_data' in record:
                prompt_parts.append(f"Structured Data:\n{json.dumps(record['structured_data'], indent=2, default=str)}")
            if 'text_representation' in record:
                prompt_parts.append(f"Text Representation:\n{record['text_representation']}")
            if 'human_narration' in record:
                prompt_parts.append(f"Human Narration:\n{record['human_narration']}")
        
        return '\n\n'.join(prompt_parts)
    
    def save_training_data(self, formatted_data: Dict[str, Any], output_path: str):
        """Save formatted training data to file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if formatted_data['format'] == 'jsonl':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_data['content'])
        elif formatted_data['format'] == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_data['content'])
        elif formatted_data['format'] == 'text':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_data['content'])
        elif 'data' in formatted_data:  # Parquet
            formatted_data['data'].to_parquet(output_path, index=False)
        
        return output_path

