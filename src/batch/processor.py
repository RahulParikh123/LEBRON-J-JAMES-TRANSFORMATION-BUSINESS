"""
Batch processor for processing multiple files in parallel
"""
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from loguru import logger

from .file_scanner import FileScanner, FileInfo
from .progress_tracker import ProgressTracker


class BatchProcessor:
    """Process multiple files in batch"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.scanner = FileScanner(config)
        self.tracker = ProgressTracker(
            checkpoint_dir=self.config.get('checkpoint_dir', 'output/checkpoints')
        )
        self.max_workers = self.config.get('max_workers', 4)
        self.resume = self.config.get('resume', True)
    
    def process_directory(
        self,
        input_directory: str,
        output_directory: str = "output",
        patterns: Optional[List[str]] = None,
        recursive: bool = True,
        process_func: Optional[Callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process all files in a directory
        
        Args:
            input_directory: Directory containing files to process
            output_directory: Directory for output files
            patterns: File patterns to match (default: all supported)
            recursive: Whether to scan subdirectories
            process_func: Function to process each file (file_path, output_dir) -> result
            **kwargs: Additional arguments to pass to process_func
        
        Returns:
            Batch processing results
        """
        logger.info(f"Scanning directory: {input_directory}")
        
        # Scan for files
        files = self.scanner.scan_directory(
            directory=input_directory,
            patterns=patterns,
            recursive=recursive
        )
        
        if not files:
            logger.warning(f"No files found in {input_directory}")
            return {
                'status': 'no_files',
                'files_processed': 0,
                'files_found': 0
            }
        
        file_paths = [str(f.path) for f in files]
        summary = self.scanner.get_file_summary(files)
        
        logger.info(f"Found {summary['total_files']} files ({summary['total_size_gb']} GB)")
        
        # Initialize progress tracking
        self.tracker.initialize(file_paths, resume=self.resume)
        
        # Get files to process (skip already completed if resuming)
        if self.resume:
            files_to_process = self.tracker.get_pending_files()
            logger.info(f"Resuming: {len(files_to_process)} files pending, {len(self.tracker.get_completed_files())} already completed")
        else:
            files_to_process = file_paths
        
        if not files_to_process:
            logger.info("All files already processed")
            return self._create_results(output_directory, files)
        
        # Create output directory
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Process files
        results = self._process_files(
            files_to_process=files_to_process,
            output_directory=output_directory,
            process_func=process_func,
            **kwargs
        )
        
        # Create final results
        final_results = self._create_results(output_directory, files)
        final_results.update(results)
        
        return final_results
    
    def _process_files(
        self,
        files_to_process: List[str],
        output_directory: str,
        process_func: Optional[Callable],
        **kwargs
    ) -> Dict[str, Any]:
        """Process files in parallel"""
        if not process_func:
            raise ValueError("process_func is required")
        
        results = {
            'successful': [],
            'failed': [],
            'errors': {}
        }
        
        # Create progress bar
        self.tracker.create_progress_bar(len(files_to_process), "Processing files")
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(
                    self._process_single_file,
                    file_path,
                    output_directory,
                    process_func,
                    **kwargs
                ): file_path
                for file_path in files_to_process
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    if result['success']:
                        results['successful'].append(file_path)
                        self.tracker.complete_file(file_path, result.get('output_path'))
                    else:
                        results['failed'].append(file_path)
                        results['errors'][file_path] = result.get('error', 'Unknown error')
                        self.tracker.fail_file(file_path, result.get('error', 'Unknown error'))
                except Exception as e:
                    error_msg = str(e)
                    results['failed'].append(file_path)
                    results['errors'][file_path] = error_msg
                    self.tracker.fail_file(file_path, error_msg)
                    logger.error(f"Error processing {file_path}: {error_msg}")
                
                self.tracker.update_progress_bar(1)
        
        self.tracker.close_progress_bar()
        
        return results
    
    def _process_single_file(
        self,
        file_path: str,
        output_directory: str,
        process_func: Callable,
        **kwargs
    ) -> Dict[str, Any]:
        """Process a single file"""
        self.tracker.start_file(file_path)
        
        try:
            result = process_func(file_path, output_directory, **kwargs)
            
            if result and isinstance(result, dict):
                return {
                    'success': True,
                    'output_path': result.get('output_path'),
                    'result': result
                }
            else:
                return {
                    'success': True,
                    'output_path': None,
                    'result': result
                }
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            logger.error(f"Error processing {file_path}: {error_msg}")
            logger.debug(traceback.format_exc())
            return {
                'success': False,
                'error': error_msg
            }
    
    def _create_results(self, output_directory: str, files: List[FileInfo]) -> Dict[str, Any]:
        """Create final results summary"""
        progress = self.tracker.get_progress()
        summary = self.scanner.get_file_summary(files)
        
        return {
            'status': 'completed',
            'input_directory': str(files[0].path.parent) if files else None,
            'output_directory': output_directory,
            'files_found': summary['total_files'],
            'files_processed': progress['completed'],
            'files_failed': progress['failed'],
            'files_pending': progress['pending'],
            'progress_percent': progress['progress_percent'],
            'total_size_gb': summary['total_size_gb'],
            'file_summary': summary,
            'completed_files': self.tracker.get_completed_files(),
            'failed_files': self.tracker.get_failed_files()
        }

