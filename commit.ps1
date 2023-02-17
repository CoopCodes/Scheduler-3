$message = Read-Host "enter commit message"
git add .
git commit -m "$message"
git push