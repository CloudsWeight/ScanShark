from fastapi import APIRouter, Request, BackgroundTasks
from typing import Dict
import logging
from services.orchestrator import run_full_scan
import os

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    return payload

@router.get("/test")
async def test_webhook():
    test_repo = "https://github.com/CloudsWeight/ScanShark"
    result = await run_full_scan(
        repo_url=test_repo,
        repo_name="CloudsWeight/ScanShark",
        commit_sha="test"
        )
    print(result)
    return result
