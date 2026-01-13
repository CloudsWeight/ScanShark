import git
import os
import uuid
from services.scanners.bandit import test_scan, scan
import asyncio 
import json
def clone(url="https://github.com/CloudsWeight/ScanShark", folder_name="scan_repo"):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # this will be fastapi\app\services\scanners
    uuid_folder = f"{folder_name}{uuid.uuid4()}"
    scan_dir = os.path.join(f"{base_dir}/scanners/", uuid_folder)  
    repo = git.Repo.clone_from(url, scan_dir, branch='main')
    return uuid_folder

if __name__ == "__main__":
    name = clone()
    print(name)
    results = asyncio.run(scan(f"scanners\\{name}"))
    print(json.dumps(results, indent=2))
