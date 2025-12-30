# app/services/scanners/semgrep.py

import asyncio
import json
import logging

logger = logging.getLogger(__name__)


async def scan(repo_path: str) -> dict:
    """
    Run Semgrep (multi-language SAST)
    """
    logger.info(f"Running Semgrep on {repo_path}")
    
    try:
        # Run Semgrep with auto config (uses community rules)
        process = await asyncio.create_subprocess_exec(
            'semgrep',
            'scan',
            '--config=auto',  # Auto-detect languages and use appropriate rules
            '--json',
            '--quiet',
            repo_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # Parse JSON output
        raw_results = json.loads(stdout.decode())
        
        # Normalize findings
        findings = []
        for result in raw_results.get('results', []):
            findings.append({
                'tool': 'semgrep',
                'type': 'security',
                'severity': result.get('extra', {}).get('severity', 'INFO'),
                'category': result.get('check_id', 'unknown'),
                'file': result.get('path', ''),
                'line': result.get('start', {}).get('line', 0),
                'description': result.get('extra', {}).get('message', ''),
                'code': result.get('extra', {}).get('lines', '')
            })
        
        logger.info(f"Semgrep found {len(findings)} issues")
        
        return {
            'tool': 'semgrep',
            'status': 'success',
            'findings_count': len(findings),
            'findings': findings
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Semgrep output parse error: {str(e)}")
        return {'tool': 'semgrep', 'status': 'error', 'error': 'Failed to parse output'}
    except Exception as e:
        logger.error(f"Semgrep scan failed: {str(e)}")
        return {'tool': 'semgrep', 'status': 'error', 'error': str(e)}