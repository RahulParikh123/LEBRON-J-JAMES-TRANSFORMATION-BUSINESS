"""
Relationship graph builder
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime


class RelationshipGraph:
    """Build and manage relationship graph"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
    
    def add_node(self, file_metadata: Dict[str, Any], processed_data: Optional[Dict[str, Any]] = None):
        """Add a file node to the graph"""
        node = {
            'id': file_metadata.get('file_id'),
            'type': 'file',
            'file_type': file_metadata.get('file_type'),
            'file_name': file_metadata.get('file_name'),
            'file_path': file_metadata.get('file_path'),
            'metadata': file_metadata,
            'processed_data_ref': processed_data.get('output_path') if processed_data else None
        }
        self.nodes.append(node)
    
    def add_edge(self, relationship: Dict[str, Any]):
        """Add a relationship edge to the graph"""
        edge = {
            'source': relationship.get('source_file_id'),
            'target': relationship.get('target_file_id'),
            'relationship_type': relationship.get('relationship_type'),
            'relationship_description': relationship.get('relationship_description'),
            'confidence': relationship.get('confidence'),
            'evidence': relationship.get('evidence', [])
        }
        self.edges.append(edge)
    
    def build_from_metadata_and_relationships(
        self,
        file_metadata_list: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        processed_data_map: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """Build graph from metadata and relationships"""
        processed_data_map = processed_data_map or {}
        
        # Add all nodes
        for metadata in file_metadata_list:
            file_id = metadata.get('file_id')
            processed_data = processed_data_map.get(file_id)
            self.add_node(metadata, processed_data)
        
        # Add all edges
        for relationship in relationships:
            self.add_edge(relationship)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary"""
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'node_count': len(self.nodes),
            'edge_count': len(self.edges),
            'created_at': datetime.now().isoformat()
        }
    
    def save(self, output_path: str):
        """Save graph to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        graph_dict = self.to_dict()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_dict, f, indent=2, default=str)
    
    def get_node_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get node by ID"""
        for node in self.nodes:
            if node['id'] == node_id:
                return node
        return None
    
    def get_edges_for_node(self, node_id: str) -> List[Dict[str, Any]]:
        """Get all edges connected to a node"""
        return [
            edge for edge in self.edges
            if edge['source'] == node_id or edge['target'] == node_id
        ]
    
    def get_connected_files(self, file_id: str) -> List[Dict[str, Any]]:
        """Get all files connected to a given file"""
        connected_ids = set()
        
        for edge in self.edges:
            if edge['source'] == file_id:
                connected_ids.add(edge['target'])
            elif edge['target'] == file_id:
                connected_ids.add(edge['source'])
        
        return [self.get_node_by_id(node_id) for node_id in connected_ids if self.get_node_by_id(node_id)]

