from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from app.infrastructure.workers.analysis_worker import AnalysisWorker
from app.application.dtos.analysis_dto import UploadResponse, TaskStatus

# СОЗДАЕМ РОУТЕР
router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

# СОЗДАЕМ ВОРКЕР
worker = AnalysisWorker(max_concurrent=5)

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Загрузка файла для анализа"""
    
    if not file.filename.endswith(('.txt', '.doc', '.docx')):
        raise HTTPException(
            status_code=400,
            detail="Поддерживаются только текстовые файлы (.txt, .doc, .docx)"
        )
    
    content = await file.read()
    
    if len(content) > 100 * 1024 * 1024:  # 100MB
        raise HTTPException(
            status_code=413,
            detail="Файл слишком большой. Максимальный размер 100MB"
        )
    
    task_id = await worker.submit(content, file.filename)
    
    return UploadResponse(
        task_id=task_id,
        status="queued",
        message="Файл принят в обработку"
    )

@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_status(task_id: str):
    """Получение статуса обработки"""
    status = worker.get_status(task_id)
    
    if status["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return TaskStatus(**status)

@router.get("/download/{task_id}")
async def download_result(task_id: str):
    """Скачать результат анализа"""
    status = worker.get_status(task_id)
    
    if status["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail="Результат ещё не готов или произошла ошибка"
        )
    
    if not os.path.exists(status["result_path"]):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        status["result_path"],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=status["filename"]
    )