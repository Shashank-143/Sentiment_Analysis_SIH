from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
import os
import tempfile
import shutil
import asyncio
from datetime import datetime
import io
import time
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
    # Debug information
    request_id = f"req_{os.getpid()}_{int(time.time())}"
    print(f"[{request_id}] Processing Excel file: {file.filename if file else 'No file'}")
    
    # Validate file input
    if not file:
        print(f"[{request_id}] Error: No file provided")
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not file.filename:
        print(f"[{request_id}] Error: File has no name")
        raise HTTPException(status_code=400, detail="File has no name")
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        print(f"[{request_id}] Error: Invalid file type: {file.filename}")
        raise HTTPException(
            status_code=400, 
            detail="Only Excel files (.xlsx, .xls) are accepted. Please ensure your file has the correct extension."
        )
    
    temp_path = None
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            # Reset file position to start
            await file.seek(0)
            try:
                # Copy the uploaded file to the temp file
                contents = await file.read()
                if not contents:
                    print("Error: Uploaded file is empty")
                    raise HTTPException(status_code=400, detail="Uploaded file is empty. Please check that your file contains data.")
                
                print(f"Read {len(contents)} bytes from uploaded file")
                temp_file.write(contents)
                temp_path = temp_file.name
            except Exception as file_read_error:
                print(f"Error reading uploaded file: {str(file_read_error)}")
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                raise HTTPException(
                    status_code=400, 
                    detail=f"Error reading uploaded file: {str(file_read_error)}. Please try uploading the file again."
                )
        
        # Verify the file was saved correctly
        if not temp_path or not os.path.exists(temp_path):
            raise HTTPException(status_code=500, detail="Failed to save uploaded file (file not found)")
            
        if os.path.getsize(temp_path) == 0:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise HTTPException(status_code=400, detail="Uploaded file is empty. Please check that your file contains data.")
        
        if save_to_disk:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"processed_{timestamp}_{file.filename}"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            await process_excel(temp_path, output_path)
            
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise HTTPException(status_code=500, detail="Failed to generate output file")
            
            background_tasks.add_task(lambda: os.unlink(output_path) if os.path.exists(output_path) else None)
            background_tasks.add_task(lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None)
            
            return FileResponse(
                path=output_path,
                filename=output_filename,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            print(f"Processing Excel file {temp_path}")
            try:
                result_io = await process_excel(temp_path)
                
                if not result_io:
                    print("Error: Failed to generate output content")
                    raise HTTPException(status_code=500, detail="Failed to generate output content")
                
                # Check if result_io is a BytesIO object before calling getbuffer()
                if not hasattr(result_io, 'getbuffer'):
                    print(f"Error: Unexpected result type: {type(result_io)}")
                    raise HTTPException(status_code=500, detail="Internal processing error: Invalid output format")
                
                if result_io.getbuffer().nbytes == 0:
                    print("Error: Empty output file generated")
                    raise HTTPException(status_code=500, detail="Empty output file generated")
                    
                background_tasks.add_task(lambda: os.unlink(temp_path) if os.path.exists(temp_path) else None)
                result_io.seek(0)
                print(f"Returning processed Excel file ({result_io.getbuffer().nbytes} bytes)")
            except Exception as e:
                print(f"Excel processing error: {str(e)}")
                import traceback
                print(traceback.format_exc())
                raise HTTPException(status_code=500, detail=f"Excel processing failed: {str(e)}")
            headers = {
                'Content-Disposition': f'attachment; filename="processed_{file.filename}"'
            }
            
            return StreamingResponse(
                result_io,
                media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers=headers
            )
            
    except ValueError as ve:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=400, detail=f"{str(ve)}")
    except Exception as e:
        # Clean up if error occurred
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        # Log the full exception
        import traceback
        print(f"Excel processing error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")