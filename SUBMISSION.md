# GitHub submission steps

1. Create the private repository named `gap-lab6-<your-roll-number>` in your GitHub account. Add `raytida` as a collaborator and verify the invitation is accepted, not pending.
2. Copy the contents of this folder into the repository root. Do not copy `.env`, `.venv`, `run_log.jsonl`, or `security_log.jsonl`. The included `.gitignore` excludes them.
3. From the repository root, install dependencies and run the local checks:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python check.py .
   ```

4. Commit each checkpoint as its own commit (at least six), then push the default branch. Confirm `.env` has never appeared in any commit on any branch.
5. In GitHub Settings → Collaborators, confirm `raytida` is an active collaborator.
6. Create and push the required submission tag:

   ```powershell
   git tag lab-6-submission
   git push origin --tags
   ```

7. Submit the private repository link through the OneDrive link shared by the course. The assignment says the course portal is not used.

The local folder is not connected to the user's GitHub account, so remote creation, collaborator invitation, commits, and tag publication remain for the repository owner.
