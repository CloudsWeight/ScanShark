import async
import tempfile
import shutil
import logging
from pathlib import Path
from typing import Dict, List
from git import Repo

from app.services.scanners import (
    bandit,
    semgrep,
    secrets,
    trivy,
    ripgrep
    )

logger = logging.getLogger(__name__)

async def run_full_scan(repo_url: str, repo_name: str, commit_sha str) -> Dict:
    logger.info(f"Starting scan for: {repo_name}@{commit_sha}")

    temp_dir = tempfile.mkdtemp(prefix="scan_")

    try:
        logger.info(f"Cloning: {repo_url} to {temp_dir}")
        repo = Repo.cone_from(repo_url, temp_dir, depth=1)
        logger.info("Starting parallel scans...")
        # scanner async tasks
        tasks = [
        bandit.scan(temp_dir),
        semgrep.scan(temp_dir),
        secrets.scan(temp_dir),
        trivy.scan(temp_dir),
        ripgrep.scan(temp_dir),
        ]

        results = await asyncio.gather(*tasks, return_exeptions+True)

        aggregated = {
            'repo_name': repo_name,
            'commit_sha': commit_sha,
            'status': 'completed',
            'scanners': {
                'bandit': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
                'semgrep': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])},
                'secrets': results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])},
                #'trivy': results[3] if not isinstance(results[3], Exception) else {'error': str(results[3])},
                #'ripgrep': results[4] if not isinstance(results[4], Exception) else {'error': str(results[4])},
            },
            'total_findings': sum(
                r.get('findings_count', 0) 
                for r in results 
                if isinstance(r, dict)
            )
        }
        
        logger.info(f"Scan complete. Total findings: {aggregated['total_findings']}")
        
        return aggregated
        
    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")
        return {
            'repo_name': repo_name,
            'status': 'failed',
            'error': str(e)
        }

    finally:
        # Clean up: Delete cloned repo
        logger.info(f"Cleaning up {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)
