"""
Agentic AI formatter for multi-file context training data
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from loguru import logger


class AgenticAIFormatter:
    """Format data for agentic AI training with multi-file context"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.include_reasoning = self.config.get('include_reasoning', True)
        self.include_relationships = self.config.get('include_relationships', True)
    
    def format_for_agentic_ai(
        self,
        file_data_list: List[Dict[str, Any]],
        relationship_graph: Optional[Dict[str, Any]] = None,
        include_reasoning: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Format files and relationships for agentic AI training
        
        Args:
            file_data_list: List of processed file data with metadata
            relationship_graph: Relationship graph (from RelationshipGraph)
            include_reasoning: Whether to include synthetic reasoning
        
        Returns:
            Formatted training data
        """
        include_reasoning = include_reasoning if include_reasoning is not None else self.include_reasoning
        
        training_records = []
        
        # Create a map of file_id to file_data
        file_map = {file_data.get('file_id'): file_data for file_data in file_data_list}
        
        # Process each file as a primary file
        for primary_file in file_data_list:
            primary_id = primary_file.get('file_id')
            
            # Find related files
            related_files = self._get_related_files(
                primary_id,
                relationship_graph,
                file_map
            )
            
            # Create training record
            record = self._create_training_record(
                primary_file,
                related_files,
                relationship_graph,
                include_reasoning
            )
            
            if record:
                training_records.append(record)
        
        return {
            'format': 'agentic_ai',
            'record_count': len(training_records),
            'content': training_records,
            'metadata': {
                'total_files': len(file_data_list),
                'total_relationships': len(relationship_graph.get('edges', [])) if relationship_graph else 0,
                'include_reasoning': include_reasoning
            }
        }
    
    def _get_related_files(
        self,
        primary_file_id: str,
        relationship_graph: Optional[Dict[str, Any]],
        file_map: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Get files related to the primary file"""
        if not relationship_graph:
            return []
        
        related = []
        edges = relationship_graph.get('edges', [])
        
        for edge in edges:
            source_id = edge.get('source')
            target_id = edge.get('target')
            
            if source_id == primary_file_id:
                # Primary file is source, target is related
                related_file = file_map.get(target_id)
                if related_file:
                    related.append({
                        'file_data': related_file,
                        'relationship': edge
                    })
            elif target_id == primary_file_id:
                # Primary file is target, source is related
                related_file = file_map.get(source_id)
                if related_file:
                    # Reverse relationship direction
                    reversed_edge = edge.copy()
                    reversed_edge['relationship_type'] = self._reverse_relationship_type(edge.get('relationship_type'))
                    related.append({
                        'file_data': related_file,
                        'relationship': reversed_edge
                    })
        
        return related
    
    def _reverse_relationship_type(self, rel_type: str) -> str:
        """Reverse relationship direction"""
        reverse_map = {
            'INFORMS': 'INFORMED_BY',
            'SUMMARIZES': 'SUMMARIZED_BY',
            'DOCUMENTS': 'DOCUMENTED_BY',
            'REFERENCES': 'REFERENCED_BY',
            'RELATED_TO': 'RELATED_TO'  # Symmetric
        }
        return reverse_map.get(rel_type, 'RELATED_TO')
    
    def _create_training_record(
        self,
        primary_file: Dict[str, Any],
        related_files: List[Dict[str, Any]],
        relationship_graph: Optional[Dict[str, Any]],
        include_reasoning: bool
    ) -> Optional[Dict[str, Any]]:
        """Create a single training record"""
        primary_metadata = primary_file.get('metadata', {})
        primary_processed = primary_file.get('processed_data', {})
        
        # Build context with actual processed data
        context = {
            'primary_file': {
                'file_id': primary_metadata.get('file_id'),
                'file_name': primary_metadata.get('file_name'),
                'file_type': primary_metadata.get('file_type'),
                'structured_data': primary_processed.get('data') if primary_processed.get('data') else None,
                'text_representation': primary_processed.get('text_content', '') or primary_processed.get('text_representation', ''),
                'metadata': primary_metadata
            }
        }
        
        # Add related files
        if related_files:
            context['related_files'] = []
            for related in related_files:
                related_file_data = related['file_data']
                related_metadata = related_file_data.get('metadata', {})
                related_processed = related_file_data.get('processed_data', {})
                relationship = related['relationship']
                
                context['related_files'].append({
                    'file_id': related_metadata.get('file_id'),
                    'file_name': related_metadata.get('file_name'),
                    'file_type': related_metadata.get('file_type'),
                    'relationship': relationship.get('relationship_type'),
                    'relationship_description': relationship.get('relationship_description'),
                    'confidence': relationship.get('confidence'),
                    'structured_data': related_processed.get('data') if related_processed.get('data') else None,
                    'text_representation': related_processed.get('text_content', '') or related_processed.get('text_representation', ''),
                    'metadata': related_metadata
                })
        
        # Build relationships list
        relationships = []
        if related_files:
            for related in related_files:
                relationship = related['relationship']
                relationships.append({
                    'source': primary_metadata.get('file_id'),
                    'target': related['file_data'].get('metadata', {}).get('file_id'),
                    'type': relationship.get('relationship_type'),
                    'confidence': relationship.get('confidence'),
                    'evidence': relationship.get('evidence', []),
                    'reasoning': self._generate_reasoning(
                        primary_file,
                        related['file_data'],
                        relationship
                    ) if include_reasoning else None
                })
        
        # Generate synthetic reasoning
        synthetic_reasoning = None
        if include_reasoning and related_files:
            synthetic_reasoning = self._generate_synthetic_reasoning(
                primary_file,
                related_files
            )
        
        # Generate training prompt and completion
        training_prompt, training_completion = self._generate_training_prompt_completion(
            primary_file,
            related_files,
            synthetic_reasoning
        )
        
        return {
            'id': f"training_record_{primary_metadata.get('file_id', 'unknown')}",
            'context': context,
            'relationships': relationships,
            'synthetic_reasoning': synthetic_reasoning,
            'training_prompt': training_prompt,
            'training_completion': training_completion
        }
    
    def _generate_reasoning(
        self,
        file1: Dict[str, Any],
        file2: Dict[str, Any],
        relationship: Dict[str, Any]
    ) -> str:
        """Generate reasoning for a relationship"""
        file1_name = file1.get('metadata', {}).get('file_name', 'File 1')
        file2_name = file2.get('metadata', {}).get('file_name', 'File 2')
        rel_type = relationship.get('relationship_type', 'RELATED_TO')
        evidence = relationship.get('evidence', [])
        
        # Build reasoning from evidence
        reasoning_parts = []
        
        # Check for shared entities
        for ev in evidence:
            if 'shared_entities' in ev.get('evidence', {}):
                entities = ev['evidence']['shared_entities']
                if entities:
                    reasoning_parts.append(
                        f"Both files share entities: {', '.join(entities[:5])}"
                    )
            
            if 'shared_terms' in ev.get('evidence', {}):
                terms = ev['evidence']['shared_terms']
                if terms:
                    reasoning_parts.append(
                        f"Both files share key terms: {', '.join(terms[:5])}"
                    )
            
            if 'filename_similarity' in ev.get('evidence', {}):
                similarity = ev['evidence']['filename_similarity']
                reasoning_parts.append(
                    f"Filenames are {similarity:.0%} similar"
                )
        
        # Build final reasoning
        if reasoning_parts:
            reasoning = f"{file1_name} {rel_type.lower()} {file2_name}. "
            reasoning += " ".join(reasoning_parts)
        else:
            reasoning = f"{file1_name} is {rel_type.lower()} {file2_name}."
        
        return reasoning
    
    def _generate_synthetic_reasoning(
        self,
        primary_file: Dict[str, Any],
        related_files: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Generate synthetic reasoning about file relationships"""
        if not related_files:
            return None
        
        primary_type = primary_file.get('metadata', {}).get('file_type', '')
        primary_name = primary_file.get('metadata', {}).get('file_name', '')
        
        # Determine workflow
        workflow = self._infer_workflow(primary_file, related_files)
        
        # Generate abstraction
        abstraction = self._generate_abstraction(primary_file, related_files, workflow)
        
        # Generate actions
        actions = self._generate_actions(primary_file, related_files)
        
        return {
            'abstraction': abstraction,
            'workflow': workflow,
            'actions': actions
        }
    
    def _infer_workflow(
        self,
        primary_file: Dict[str, Any],
        related_files: List[Dict[str, Any]]
    ) -> str:
        """Infer workflow from file types"""
        file_types = [primary_file.get('metadata', {}).get('file_type', '')]
        file_types.extend([rf['file_data'].get('metadata', {}).get('file_type', '') for rf in related_files])
        
        # Common workflows
        if 'word' in file_types and 'excel' in file_types and 'powerpoint' in file_types:
            return "Documentation → Data Analysis → Presentation"
        elif 'excel' in file_types and 'powerpoint' in file_types:
            return "Data Collection → Visualization"
        elif 'word' in file_types and 'excel' in file_types:
            return "Documentation → Data Processing"
        else:
            return "Data Processing Workflow"
    
    def _generate_abstraction(
        self,
        primary_file: Dict[str, Any],
        related_files: List[Dict[str, Any]],
        workflow: str
    ) -> str:
        """Generate abstraction of the file relationships"""
        primary_name = primary_file.get('metadata', {}).get('file_name', 'primary file')
        related_names = [rf['file_data'].get('metadata', {}).get('file_name') for rf in related_files]
        
        abstraction = f"This is a {workflow.lower()} where {primary_name} "
        
        if len(related_files) == 1:
            rel = related_files[0]['relationship']
            abstraction += f"{rel.get('relationship_type', 'RELATED_TO').lower()} {related_names[0]}."
        else:
            abstraction += f"connects to {len(related_files)} related files: {', '.join(related_names[:3])}."
        
        return abstraction
    
    def _generate_actions(self, primary_file: Dict[str, Any], related_files: List[Dict[str, Any]]) -> List[str]:
        """Generate action sequence"""
        actions = []
        
        primary_type = primary_file.get('metadata', {}).get('file_type', '')
        
        for related in related_files:
            rel_type = related['relationship'].get('relationship_type', '')
            related_type = related['file_data'].get('metadata', {}).get('file_type', '')
            
            if rel_type == 'INFORMS':
                if primary_type == 'excel' and related_type == 'powerpoint':
                    actions.append(f"Extract data from {primary_file.get('metadata', {}).get('file_name')}")
                    actions.append(f"Create visualizations")
                    actions.append(f"Generate presentation in {related['file_data'].get('metadata', {}).get('file_name')}")
                elif primary_type == 'word' and related_type == 'excel':
                    actions.append(f"Extract information from {primary_file.get('metadata', {}).get('file_name')}")
                    actions.append(f"Create data model in {related['file_data'].get('metadata', {}).get('file_name')}")
        
        if not actions:
            actions.append(f"Process {primary_file.get('metadata', {}).get('file_name')}")
            actions.append(f"Link to related files")
        
        return actions
    
    def _generate_training_prompt_completion(
        self,
        primary_file: Dict[str, Any],
        related_files: List[Dict[str, Any]],
        synthetic_reasoning: Optional[Dict[str, Any]]
    ) -> tuple[str, str]:
        """Generate training prompt and completion"""
        primary_name = primary_file.get('metadata', {}).get('file_name', 'file')
        primary_type = primary_file.get('metadata', {}).get('file_type', '')
        
        if related_files:
            related_names = [rf['file_data'].get('metadata', {}).get('file_name') for rf in related_files]
            
            prompt = f"Given a {primary_type} file '{primary_name}', identify related files and explain how they connect."
            
            completion_parts = [f"The file '{primary_name}' is connected to:"]
            
            for related in related_files:
                rel_name = related['file_data'].get('metadata', {}).get('file_name')
                rel_type = related['relationship'].get('relationship_type', 'RELATED_TO')
                rel_desc = related['relationship'].get('relationship_description', '')
                completion_parts.append(f"- '{rel_name}' through a {rel_type} relationship: {rel_desc}")
            
            if synthetic_reasoning:
                completion_parts.append(f"\nWorkflow: {synthetic_reasoning.get('workflow', '')}")
                completion_parts.append(f"Abstraction: {synthetic_reasoning.get('abstraction', '')}")
            
            completion = "\n".join(completion_parts)
        else:
            prompt = f"Describe the {primary_type} file '{primary_name}'."
            completion = f"The file '{primary_name}' is a {primary_type} file with no detected relationships to other files."
        
        return prompt, completion

