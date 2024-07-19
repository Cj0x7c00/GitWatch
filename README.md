## GitWatch
a simple python tool that watches a git repo

### how to
1. clone this repo
2. cd into the repo
3. int GitWatch, add a OnSetup file formatted like so:
``` py
def OnSetup(repo, owner, branch):
    # new commit logic
```
this function is called when a new commit is polled from the git repo.<br>
use tis  to  do any logic you need

4. run and forget
