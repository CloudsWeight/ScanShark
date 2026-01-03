"""Bandit scanner
"""
import asyncio
import json
import logging
from pathlib import Path
import sys
import os

logger = logging.getLogger(__name__)


async def scan(repo_path: str) -> dict:
    """
    Run Bandit (Python SAST) scanner
    
    Args:
        repo_path: Path to cloned repository
        
    Returns:
        Normalized findings
    """
    logger.info(f"Running Bandit on {repo_path}")
    print(f"Running Bandit on {repo_path}")
    try:
        process = await asyncio.create_subprocess_exec(
            'bandit',
            '-r',  # Recursive
            repo_path,
            '-f', 'json',  # JSON output
            '-o', 'bandit_output.json')

        stdout, stderr = await process.communicate()
        print(f"Bandit exited with code {process.returncode}")
        if stdout:
            print("STDOUT:", stdout.decode())
        if stderr:
            print("STDERR:", stderr.decode())
        
        with open('bandit_output.json') as f:
            raw_results = json.load(f)
        
        # Normalize findings
        findings = []
        for result in raw_results.get('results', []):
            findings.append({
                'tool': 'bandit',
                'type': 'security',
                'severity': result.get('issue_severity', 'UNKNOWN'),
                'confidence': result.get('issue_confidence', 'UNKNOWN'),
                'category': result.get('test_id', 'unknown'),
                'file': result.get('filename', ''),
                'line': result.get('line_number', 0),
                'description': result.get('issue_text', ''),
                'code': result.get('code', '')
            })
        
        logger.info(f"Bandit found {len(findings)} issues")
        
        return {
            'tool': 'bandit',
            'status': 'success',
            'findings_count': len(findings),
            'findings': findings,
            'metrics': raw_results.get('metrics', {})
        }
        
    except Exception as e:
        logger.error(f"Bandit scan failed: {str(e)}")
        return {
            'tool': 'bandit',
            'status': 'error',
            'error': str(e)
        }

async def test_scan(repo_path):
    print(f"testing {repo_path}")
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m", "bandit",
        "-r", repo_path,
        "-f", "json",
        "-o", "bandit_output.json"
    )
    stdout, stderr = await process.communicate()
    print(f"Bandit exited with code {process.returncode}")
    if stdout:
        print("STDOUT:", stdout.decode())
    if stderr:
        print("STDERR:", stderr.decode())
if __name__ == "__main__":
    asyncio.run(test_scan("."))
