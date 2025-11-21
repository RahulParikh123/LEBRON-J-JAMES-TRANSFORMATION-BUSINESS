"""
FastAPI Backend for Data Transformation Platform
Exposes the platform as a REST API service
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import uuid
import json
from pathlib import Path
import shutil
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import DataTransformationPipeline

app = FastAPI(
    title="Data Transformation Platform API",
    description="Enterprise Data Transformation Platform for LLM Training",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("api_output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# In-memory job tracking (use Redis/DB in production)
jobs = {}


class ProcessingRequest(BaseModel):
    """Request model for processing"""
    config: Optional[Dict[str, Any]] = None
    narration: Optional[str] = None
    output_format: Optional[str] = "jsonl"


class JobStatus(BaseModel):
    """Job status model"""
    job_id: str
    status: str
    progress: float
    message: str
    output_path: Optional[str] = None
    stats: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Data Transformation Platform API",
        "version": "0.1.0",
        "endpoints": {
            "upload_and_process": "/api/v1/process",
            "job_status": "/api/v1/jobs/{job_id}",
            "download_result": "/api/v1/jobs/{job_id}/download",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/process")
async def process_file(
    file: UploadFile = File(...),
    narration: Optional[UploadFile] = File(None),
    config: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """
    Upload and process a data file
    
    Args:
        file: Data file to process (CSV, JSON, Excel, PPT, etc.)
        narration: Optional narration file
        config: Optional JSON configuration string
    """
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save narration if provided
    narration_path = None
    if narration:
        narration_path = UPLOAD_DIR / f"{job_id}_narration_{narration.filename}"
        with open(narration_path, "wb") as buffer:
            shutil.copyfileobj(narration.file, buffer)
    
    # Parse config if provided
    pipeline_config = {}
    if config:
        try:
            pipeline_config = json.loads(config)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON configuration")
    
    # Initialize job
    jobs[job_id] = {
        "status": "processing",
        "progress": 0.0,
        "message": "Processing started",
        "output_path": None,
        "stats": None,
        "error": None,
        "created_at": datetime.now().isoformat()
    }
    
    # Process in background
    if background_tasks:
        background_tasks.add_task(
            process_data_background,
            job_id,
            str(file_path),
            str(narration_path) if narration_path else None,
            pipeline_config
        )
    else:
        # Process synchronously (for testing)
        process_data_background(
            job_id,
            str(file_path),
            str(narration_path) if narration_path else None,
            pipeline_config
        )
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "File uploaded and processing started"
    }


def process_data_background(
    job_id: str,
    file_path: str,
    narration_path: Optional[str],
    config: Dict[str, Any]
):
    """Process data in background"""
    try:
        # Update progress
        jobs[job_id]["progress"] = 10.0
        jobs[job_id]["message"] = "Initializing pipeline..."
        
        # Initialize pipeline
        pipeline = DataTransformationPipeline(config)
        
        jobs[job_id]["progress"] = 20.0
        jobs[job_id]["message"] = "Processing data..."
        
        # Generate output path
        output_filename = f"{job_id}_processed.jsonl"
        output_path = OUTPUT_DIR / output_filename
        
        # Process data
        results = pipeline.process(
            input_path=file_path,
            output_path=str(output_path),
            narration_path=narration_path
        )
        
        # Update job status
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100.0
        jobs[job_id]["message"] = "Processing completed successfully"
        jobs[job_id]["output_path"] = str(output_path)
        jobs[job_id]["stats"] = results.get("stats", {})
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["progress"] = 0.0
        jobs[job_id]["message"] = f"Processing failed: {str(e)}"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["failed_at"] = datetime.now().isoformat()


@app.get("/api/v1/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        output_path=job.get("output_path"),
        stats=job.get("stats"),
        error=job.get("error")
    )


@app.get("/api/v1/jobs/{job_id}/download")
async def download_result(job_id: str):
    """Download processed result file"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Status: {job['status']}"
        )
    
    output_path = job.get("output_path")
    if not output_path or not Path(output_path).exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_path,
        media_type="application/octet-stream",
        filename=f"processed_{job_id}.jsonl"
    )


@app.get("/api/v1/jobs")
async def list_jobs(limit: int = 10):
    """List recent jobs"""
    job_list = []
    for job_id, job_data in list(jobs.items())[-limit:]:
        job_list.append({
            "job_id": job_id,
            "status": job_data["status"],
            "created_at": job_data.get("created_at"),
            "message": job_data["message"]
        })
    
    return {"jobs": job_list, "total": len(jobs)}


@app.delete("/api/v1/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its files"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete output file
    output_path = jobs[job_id].get("output_path")
    if output_path and Path(output_path).exists():
        Path(output_path).unlink()
    
    # Delete uploaded files
    for file_path in UPLOAD_DIR.glob(f"{job_id}*"):
        file_path.unlink()
    
    # Remove job
    del jobs[job_id]
    
    return {"message": "Job deleted successfully"}


@app.get("/api/v1/formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    from src.ingestion.registry import FormatRegistry
    registry = FormatRegistry()
    
    return {
        "supported_formats": registry.get_supported_formats(),
        "handlers": [
            "ExcelHandler",
            "CSVHandler",
            "JSONHandler",
            "PPTHandler",
            "DatabaseHandler"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

