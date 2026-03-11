# Command: git-stage-commit-push

Stage, generate a smart commit message from git diff, commit, and push.

## Steps

1. Inspect repo status
git status

2. Analyze changes
git diff

3. Stage changes
git add .

4. Generate a Conventional Commit message from the diff.

Format:
<type>(scope): short summary

- key change
- key change

5. Commit
git commit -m "<generated message>"

6. Push
git push