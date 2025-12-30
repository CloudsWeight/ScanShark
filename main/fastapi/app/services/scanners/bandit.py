"""Bandit scanner
"""
import asyncio
import json
import logging
from pathlib import Path

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
        # Check if Python files exist
        if not list(Path(repo_path).rglob('*.py')):
            logger.info("No Python files found, skipping Bandit")
            print("No Python files found, skipping Bandit")
            return {
                'tool': 'bandit',
                'status': 'skipped',
                'reason': 'No Python files found',
                'findings_count': 0,
                'findings': []
            }
        
        # Run Bandit
        process = await asyncio.create_subprocess_exec(
            'bandit',
            '-r',  # Recursive
            repo_path,
            '-f', 'json',  # JSON output
            '-o', 'bandit_output.json',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # Bandit exits with 1 if findings, 0 if clean
        # So non-zero doesn't mean error
        
        # Read results
        try:
            with open('/tmp/bandit_output.json') as f:
                raw_results = json.load(f)
        except FileNotFoundError:
            return {
                'tool': 'bandit',
                'status': 'error',
                'error': 'Output file not created'
            }
        
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