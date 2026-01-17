### Windows users
##Date: 17th Jan 2026

If you get an execution policy error running npm, execute the following to allow local scripts via RemoteSigned:
```powershell

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
