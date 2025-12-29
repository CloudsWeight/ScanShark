from fastapi import APIRouter, Request, BackgroundTasks
from typing import Dict
import logging
from app.services.orchestrator import run_full_scan

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        payload = await request.json()

        repo_url = payload.get('repository', {}).get('clone_url')
        repo_name = paylod.get('repository', {}).get('fullname')
        commit_sha = payload.get('after')

        if not repo_url:
            return {"error":"No repo URL in payload"}

        logger.info(f"Web hook for repo : {repo_name}, commit: {commit_sha}")

        background_tasks.add_task(
            run_full_san,
            repo_url=repo_url,
            repo_name=repo_name,
            commit_sha=commit_sha
            )

        return {
            "status":"accepted",
            "message": f"Scan queued for {repo_name}",
            "commit":commit_sha
        }

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return {"error": str(e)}, 500

@router.get("/test"):
async def test_tebhook():
    test_repo = "https://github.com/CloudsWeight/ScanShark/tree/main"
    result = await run_full_scan(
        repo_url=test_repo,
        repo_name="test/repo",
        commit_sha="test"
        )
    return result