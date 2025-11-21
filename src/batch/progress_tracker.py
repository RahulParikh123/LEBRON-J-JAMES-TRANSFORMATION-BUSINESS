"""
Progress tracking and checkpoint management for batch processing
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from tqdm import tqdm


@dataclass
class FileStatus:
    """Status of a file being processed"""
    file_path: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    progress: float = 0.0
    error: Optional[str] = None
    output_path: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class ProgressTracker:
    """Track progress of batch processing"""
    
    def __init__(self, checkpoint_dir: Optional[str] = None):
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else Path('output/checkpoints')
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_file = self.checkpoint_dir / 'batch_state.json'
        self.file_statuses: Dict[str, FileStatus] = {}
        self.progress_bar: Optional[tqdm] = None
    
    def initialize(self, file_paths: List[str], resume: bool = True):
        """Initialize tracking for a batch of files"""
        if resume and self.checkpoint_file.exists():
            # Load existing state
            self._load_checkpoint()
            # Update with any new files
            for file_path in file_paths:
                if file_path not in self.file_statuses:
                    self.file_statuses[file_path] = FileStatus(
                        file_path=file_path,
                        status='pending'
                    )
        else:
            # Initialize fresh
            for file_path in file_paths:
                self.file_statuses[file_path] = FileStatus(
                    file_path=file_path,
                    status='pending'
                )
        
        self._save_checkpoint()
    
    def start_file(self, file_path: str):
        """Mark file as processing"""
        if file_path in self.file_statuses:
            self.file_statuses[file_path].status = 'processing'
            self.file_statuses[file_path].started_at = datetime.now().isoformat()
            self._save_checkpoint()
    
    def complete_file(self, file_path: str, output_path: Optional[str] = None):
        """Mark file as completed"""
        if file_path in self.file_statuses:
            self.file_statuses[file_path].status = 'completed'
            self.file_statuses[file_path].progress = 1.0
            self.file_statuses[file_path].output_path = str(output_path) if output_path else None
            self.file_statuses[file_path].completed_at = datetime.now().isoformat()
            self._save_checkpoint()
    
    def fail_file(self, file_path: str, error: str):
        """Mark file as failed"""
        if file_path in self.file_statuses:
            self.file_statuses[file_path].status = 'failed'
            self.file_statuses[file_path].error = str(error)
            self.file_statuses[file_path].completed_at = datetime.now().isoformat()
            self._save_checkpoint()
    
    def get_pending_files(self) -> List[str]:
        """Get list of files that need processing"""
        return [
            path for path, status in self.file_statuses.items()
            if status.status in ['pending', 'failed']
        ]
    
    def get_completed_files(self) -> List[str]:
        """Get list of successfully completed files"""
        return [
            path for path, status in self.file_statuses.items()
            if status.status == 'completed'
        ]
    
    def get_failed_files(self) -> List[str]:
        """Get list of failed files"""
        return [
            path for path, status in self.file_statuses.items()
            if status.status == 'failed'
        ]
    
    def get_progress(self) -> Dict[str, Any]:
        """Get overall progress statistics"""
        total = len(self.file_statuses)
        if total == 0:
            return {
                'total': 0,
                'completed': 0,
                'failed': 0,
                'pending': 0,
                'progress_percent': 0.0
            }
        
        completed = len(self.get_completed_files())
        failed = len(self.get_failed_files())
        pending = len(self.get_pending_files())
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'pending': pending,
            'progress_percent': round((completed / total) * 100, 2) if total > 0 else 0.0
        }
    
    def create_progress_bar(self, total: int, desc: str = "Processing"):
        """Create a progress bar"""
        self.progress_bar = tqdm(total=total, desc=desc, unit="file")
    
    def update_progress_bar(self, n: int = 1):
        """Update progress bar"""
        if self.progress_bar:
            self.progress_bar.update(n)
    
    def close_progress_bar(self):
        """Close progress bar"""
        if self.progress_bar:
            self.progress_bar.close()
            self.progress_bar = None
    
    def _save_checkpoint(self):
        """Save current state to checkpoint file"""
        state = {
            'file_statuses': {
                path: asdict(status) for path, status in self.file_statuses.items()
            },
            'last_updated': datetime.now().isoformat()
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_checkpoint(self):
        """Load state from checkpoint file"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                state = json.load(f)
            
            self.file_statuses = {
                path: FileStatus(**status_dict)
                for path, status_dict in state.get('file_statuses', {}).items()
            }
        except (FileNotFoundError, json.JSONDecodeError):
            self.file_statuses = {}
    
    def clear_checkpoint(self):
        """Clear checkpoint file"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
        self.file_statuses = {}

