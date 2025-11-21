"""
Text file handler (.txt, .md, .log, .xml, .yaml, .yml, .toml, .ini, .cfg)
"""
from typing import Dict, Any, List
from pathlib import Path
from .base_handler import BaseHandler
import json
import xml.etree.ElementTree as ET

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import tomli
    TOML_AVAILABLE = True
except ImportError:
    try:
        import toml
        TOML_AVAILABLE = True
    except ImportError:
        TOML_AVAILABLE = False


class TextHandler(BaseHandler):
    """Handler for text-based files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is a text file"""
        ext = Path(file_path).suffix.lower()
        return ext in ['.txt', '.md', '.markdown', '.log', '.xml', '.yaml', '.yml', 
                       '.toml', '.ini', '.cfg', '.conf', '.properties']
    
    def get_supported_extensions(self) -> List[str]:
        return ['.txt', '.md', '.markdown', '.log', '.xml', '.yaml', '.yml', 
                '.toml', '.ini', '.cfg', '.conf', '.properties']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """Extract data from text file"""
        metadata = self.extract_metadata(source)
        result = {
            'data': [],
            'metadata': metadata,
            'text_content': [],
            'structure': {}
        }
        
        try:
            ext = Path(source).suffix.lower()
            encoding = kwargs.get('encoding', 'utf-8')
            
            with open(source, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
            
            text_content = [content]
            structured_data = {}
            
            # Parse based on file type
            if ext == '.xml':
                try:
                    root = ET.fromstring(content)
                    structured_data = self._xml_to_dict(root)
                except ET.ParseError:
                    structured_data = {'raw': content}
            
            elif ext in ['.yaml', '.yml'] and YAML_AVAILABLE:
                try:
                    structured_data = yaml.safe_load(content)
                except Exception:
                    structured_data = {'raw': content}
            
            elif ext == '.toml' and TOML_AVAILABLE:
                try:
                    if hasattr(tomli, 'loads'):
                        structured_data = tomli.loads(content)
                    else:
                        structured_data = toml.loads(content)
                except Exception:
                    structured_data = {'raw': content}
            
            elif ext in ['.ini', '.cfg', '.conf', '.properties']:
                structured_data = self._parse_ini(content)
            
            else:
                # Plain text or markdown
                structured_data = {'text': content}
            
            result['data'] = [structured_data] if structured_data else []
            result['text_content'] = text_content
            result['structure'] = {
                'format': ext[1:] if ext else 'text',
                'line_count': len(content.splitlines()),
                'char_count': len(content)
            }
            
            metadata.update({
                'line_count': len(content.splitlines()),
                'char_count': len(content)
            })
            
        except Exception as e:
            raise ValueError(f"Error reading text file {source}: {str(e)}")
        
        return result
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """Convert XML element to dictionary"""
        result = {element.tag: {} if element.attrib else None}
        
        children = list(element)
        if children:
            dd = {}
            for dc in map(self._xml_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            result = {element.tag: dd}
        
        if element.attrib:
            result[element.tag].update(('@' + k, v) for k, v in element.attrib.items())
        
        if element.text:
            text = element.text.strip()
            if children or element.attrib:
                if text:
                    result[element.tag]['#text'] = text
            else:
                result[element.tag] = text
        
        return result
    
    def _parse_ini(self, content: str) -> Dict[str, Any]:
        """Parse INI-style configuration"""
        result = {}
        current_section = None
        
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                result[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if current_section:
                    result[current_section][key] = value
                else:
                    result[key] = value
        
        return result

