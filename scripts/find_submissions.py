import subprocess, sys

SUBMISSION_DIRS = [
    "Submission-Milestone1", "Submission-Milestone2",
    "Submission-Milestone3", "Submission-Milestone4",
]
EXTS = (".ipynb", ".py", ".txt", ".md", ".csv", ".json", ".html", ".pdf", ".docx", ".xlsx", ".zip")

def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return result.stdout.strip()

def main():
    before = sys.argv[1] if len(sys.argv) > 1 else ""
    after = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    paths = []
    if not before or set(before) == {"0"}:
        for folder in SUBMISSION_DIRS:
            paths.extend(git("ls-tree", "-r", "--name-only", after, "--", folder).splitlines())
    else:
        for folder in SUBMISSION_DIRS:
            paths.extend(git("diff", "--name-only", "--diff-filter=AM", before, after, "--", folder).splitlines())
    for path in sorted(set(paths)):
        if path.lower().endswith(EXTS):
            print(path)

if __name__ == "__main__":
    main()
