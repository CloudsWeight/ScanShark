from fastapi import APIRouter, Request, BackgroundTasks
from typing import Dict
import logging
from services.orchestrator import run_full_scan
from services.clone import clone
import os
import asyncio
import sys
import json

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    test_repo = "https://github.com/CloudsWeight/ScanShark"
    repo_path = clone(test_repo)
    output_file = os.path.join(repo_path, "bandit_output.json")
    process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m", "bandit",
            "-r", repo_path,
            "-f", "json",
            "-o", output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    stdout, stderr = await process.communicate()  # <-- wait for bandit to finish

    with open(output_file, "r", encoding="utf-8") as f:
            bandit_results = json.load(f)

    return {
        "status": "success",
        "repo_path": repo_path,
        "bandit": bandit_results,
        }

@router.get("/test")
async def test_webhook():
    test_repo = "https://github.com/CloudsWeight/ScanShark"
    repo_path = clone(test_repo)
    output_file = os.path.join(repo_path, "bandit_output.json")
    process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m", "bandit",
            "-r", repo_path,
            "-f", "json",
            "-o", output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    stdout, stderr = await process.communicate()  # <-- wait for bandit to finish

    with open(output_file, "r", encoding="utf-8") as f:
            bandit_results = json.load(f)

    return {
        "status": "success",
        "repo_path": repo_path,
        "bandit": bandit_results,
    }
    
