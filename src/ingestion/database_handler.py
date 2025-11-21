"""
Database handler (PostgreSQL, MySQL, SQLite)
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from .base_handler import BaseHandler


class DatabaseHandler(BaseHandler):
    """Handler for database connections"""
    
    def can_handle(self, connection_string: str) -> bool:
        """Check if connection string is valid"""
        try:
            # Try to create engine (won't connect yet)
            engine = create_engine(connection_string)
            return True
        except:
            return False
    
    def get_supported_extensions(self) -> List[str]:
        return ['sqlite', 'postgresql', 'mysql', 'mssql', 'oracle', 'mongodb']
    
    def extract(self, source: str, table_name: Optional[str] = None, 
                query: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Extract data from database
        
        Args:
            source: Database connection string
            table_name: Specific table to extract (if None, extracts all tables)
            query: Custom SQL query to execute
        """
        metadata = self.extract_metadata(source)
        
        try:
            engine = create_engine(source)
            
            if query:
                # Execute custom query
                df = pd.read_sql_query(text(query), engine)
                df = self.normalize_dataframe(df)
                records = df.to_dict('records')
                
                text_content = self._dataframe_to_text(df, f"Query Results")
                
                return {
                    'data': records,
                    'metadata': {**metadata, 'source_type': 'query'},
                    'text_content': [text_content],
                    'structure': {
                        'format': 'database',
                        'columns': list(df.columns),
                        'source': 'custom_query'
                    }
                }
            
            elif table_name:
                # Extract specific table
                df = pd.read_sql_table(table_name, engine)
                df = self.normalize_dataframe(df)
                records = df.to_dict('records')
                
                text_content = self._dataframe_to_text(df, table_name)
                
                metadata.update({
                    'table_name': table_name,
                    'row_count': len(df),
                    'column_count': len(df.columns)
                })
                
                return {
                    'data': records,
                    'metadata': metadata,
                    'text_content': [text_content],
                    'structure': {
                        'format': 'database',
                        'table_name': table_name,
                        'columns': list(df.columns)
                    }
                }
            else:
                # Extract all tables
                # Handle MongoDB differently (not SQL)
                if 'mongodb' in source.lower() or 'mongo' in source.lower():
                    try:
                        from pymongo import MongoClient
                        client = MongoClient(source)
                        db_name = source.split('/')[-1].split('?')[0]
                        db = client[db_name]
                        collections = db.list_collection_names()
                        
                        all_data = {}
                        all_text = []
                        
                        for collection_name in collections:
                            collection = db[collection_name]
                            # Get sample documents
                            docs = list(collection.find().limit(1000))
                            if docs:
                                df = pd.DataFrame(docs)
                                df = self.normalize_dataframe(df)
                                records = df.to_dict('records')
                                
                                all_data[collection_name] = {
                                    'data': records,
                                    'columns': list(df.columns),
                                    'row_count': len(records)
                                }
                                
                                text_content = self._dataframe_to_text(df, collection_name)
                                all_text.append(text_content)
                        
                        metadata.update({
                            'table_count': len(collections),
                            'tables': collections,
                            'total_rows': sum(t['row_count'] for t in all_data.values())
                        })
                        
                        return {
                            'data': all_data,
                            'metadata': metadata,
                            'text_content': all_text,
                            'structure': {
                                'format': 'mongodb',
                                'collections': collections,
                                'collection_count': len(collections)
                            }
                        }
                    except ImportError:
                        raise ValueError("pymongo required for MongoDB connections. Install with: pip install pymongo")
                
                # SQL databases
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                
                all_data = {}
                all_text = []
                
                for table in tables:
                    df = pd.read_sql_table(table, engine)
                    df = self.normalize_dataframe(df)
                    records = df.to_dict('records')
                    
                    all_data[table] = {
                        'data': records,
                        'columns': list(df.columns),
                        'row_count': len(df)
                    }
                    
                    text_content = self._dataframe_to_text(df, table)
                    all_text.append(text_content)
                
                metadata.update({
                    'table_count': len(tables),
                    'tables': tables,
                    'total_rows': sum(t['row_count'] for t in all_data.values())
                })
                
                return {
                    'data': all_data,
                    'metadata': metadata,
                    'text_content': all_text,
                    'structure': {
                        'format': 'database',
                        'tables': tables,
                        'table_count': len(tables)
                    }
                }
                
        except Exception as e:
            raise ValueError(f"Error reading from database {source}: {str(e)}")
    
    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract database metadata"""
        # Parse connection string to get database info
        db_type = 'unknown'
        if 'postgresql' in source.lower() or 'postgres' in source.lower():
            db_type = 'postgresql'
        elif 'mysql' in source.lower():
            db_type = 'mysql'
        elif 'sqlite' in source.lower():
            db_type = 'sqlite'
        elif 'mssql' in source.lower() or 'sqlserver' in source.lower():
            db_type = 'mssql'
        elif 'oracle' in source.lower():
            db_type = 'oracle'
        elif 'mongodb' in source.lower() or 'mongo' in source.lower():
            db_type = 'mongodb'
        
        return {
            'source_path': source,
            'source_type': 'database',
            'database_type': db_type,
            'handler_type': self.__class__.__name__,
        }
    
    def _dataframe_to_text(self, df: pd.DataFrame, table_name: str) -> str:
        """Convert DataFrame to text representation"""
        lines = [f"Table: {table_name}"]
        lines.append(f"Columns: {', '.join(df.columns)}")
        lines.append(f"Rows: {len(df)}")
        lines.append("")
        
        # Include sample rows
        sample_size = min(10, len(df))
        for idx, row in df.head(sample_size).iterrows():
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            lines.append(f"Row {idx}: {row_text}")
        
        return "\n".join(lines)

