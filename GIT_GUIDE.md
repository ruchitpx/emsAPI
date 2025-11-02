# 1. Initialize a new local repo and push
git init
git add .
git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/ruchitpx/emsAPI.git
git push -u origin main

git push -u origin main --force

# 2. Clone an existing repo
git clone https://github.com/ruchitpx/emsAPI.git

# 3. Pull latest changes from remote
git pull origin main

# 4. Status
git status

# ------------------------
# Common workflows summarized
# ------------------------

# First publish:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ruchitpx/emsAPI.git
git push -u origin main

# Daily update:
git pull --rebase origin main

git add .
git commit -m "Describe your change"
git push
