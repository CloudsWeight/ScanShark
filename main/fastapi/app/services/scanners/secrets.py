# app/services/scanners/secrets.py

import asyncio
import json
import logging

logger = logging.getLogger(__name__)


async def scan(repo_path: str) -> dict:
    """
    Run detect-secrets scanner
    """
    logger.info(f"Running detect-secrets on {repo_path}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            'detect-secrets',
            'scan',
            '--all-files',
            repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        raw_results = json.loads(stdout.decode())
        
        # Normalize findings
        findings = []
        for file_path, secrets_list in raw_results.get('results', {}).items():
            for secret in secrets_list:
                findings.append({
                    'tool': 'detect-secrets',
                    'type': 'secret',
                    'severity': 'HIGH',
                    'category': secret.get('type', 'unknown_secret'),
                    'file': file_path,
                    'line': secret.get('line_number', 0),
                    'description': f"Potential {secret.get('type', 'secret')} detected"
                })
        
        logger.info(f"detect-secrets found {len(findings)} secrets")
        
        return {
            'tool': 'detect-secrets',
            'status': 'success',
            'findings_count': len(findings),
            'findings': findings
        }
        
    except Exception as e:
        logger.error(f"detect-secrets scan failed: {str(e)}")
        return {'tool': 'detect-secrets', 'status': 'error', 'error': str(e)}