from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
import os
import tempfile
import shutil
import asyncio
from datetime import datetime
import io
from typing import Optional
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.process_excel import process_excel

router = APIRouter()

@router.post("/process-excel", summary="Process Excel file with comments")
async def process_excel_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    save_to_disk: bool = False
):
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are accepted")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        if save_to_disk:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"processed_{timestamp}_{file.filename}"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            await process_excel(temp_path, output_path)
            
            background_tasks.add_task(lambda: os.unlink(output_path) if os.path.exists(output_path) else None)
            background_tasks.add_task(lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None)
            
            return FileResponse(
                path=output_path,
                filename=output_filename,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            result_io = await process_excel(temp_path)
            
            background_tasks.add_task(lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None)
            
            return StreamingResponse(
                result_io,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={
                    'Content-Disposition': f'attachment; filename="processed_{file.filename}"'
                }
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")