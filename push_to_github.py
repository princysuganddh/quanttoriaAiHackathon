"""
GitHub Push Utility for Quanttoria AI Maths
Usage:
    python push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>
Or set the environment variable GITHUB_TOKEN and run:
    python push_to_github.py
"""
import sys
import os
import getpass
from dulwich import porcelain
from dulwich.repo import Repo

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
REMOTE_REPO = "princysuganddh/quanttoriaAiHackathon"

def push_project(token=None):
    if not token:
        token = os.getenv("GITHUB_TOKEN")
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
    if not token:
        print("\nGitHub requires authentication to push.")
        token = getpass.getpass("Enter your GitHub Personal Access Token (PAT): ").strip()
    
    if not token:
        print("Error: No token provided. Aborting.")
        sys.exit(1)

    authenticated_url = f"https://{token}@github.com/{REMOTE_REPO}.git"
    print(f"Pushing to https://github.com/{REMOTE_REPO}.git (branch: main)...")

    repo = Repo(REPO_PATH)
    # Ensure branch main exists
    head = repo.head()
    repo.refs[b"refs/heads/main"] = head

    try:
        porcelain.push(repo, authenticated_url, b"refs/heads/main:refs/heads/main", force=True)
        print("\nSUCCESS! 🎉")
        print(f"Project successfully pushed to: https://github.com/{REMOTE_REPO}")
    except Exception as e:
        print("\nPush failed:", e)
        print("\nPlease verify:")
        print(f"1. That the repository exists at https://github.com/{REMOTE_REPO} (create it if not yet created at https://github.com/new).")
        print("2. That your Personal Access Token has 'repo' (write) permissions.")

if __name__ == "__main__":
    push_project()
