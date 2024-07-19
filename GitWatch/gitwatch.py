import requests
import time
import threading
import argparse

from OnSetup import *



# Function to get the latest commit hash
def get_latest_commit(o, r, b):

    URL = f"https://api.github.com/repos/{o}/{r}/commits?sha={b}"

    response = requests.get(URL)
    response.raise_for_status()

    commits = response.json()
    if commits:
        return commits[0]["sha"]
    return None

# Function to perform an action when a new commit is detected
def on_new_commit(commit, repo, owner, branch):
    print(f"> New commit detected: {commit}")
    OnSetup(repo=repo, owner=owner, branch=branch)
    
def poll_fn(interval, repo, owner, branch, latestc, OnCommit):
    sTime = time.time()
    while True:
        #Check if the elapsed time has reached  the poll interval
        cTime = time.time()
        eTime = cTime - sTime
        if  eTime >= interval:
            sTime = cTime
            current_commit = get_latest_commit(owner, repo, branch)
            if current_commit and current_commit != latestc:
                latestc = current_commit
                on_new_commit(current_commit, repo=repo, owner=owner, branch=branch)

def main(interval, repo, owner, branch):
    latest_commit = get_latest_commit(owner, repo, branch)
    if not latest_commit:
        print("> No commits found or unable to fetch commits.")
        return

    print(f"> Starting with latest commit: {latest_commit}")

    poll_thread = threading.Thread(target=poll_fn, args=(interval, repo, owner, branch, latest_commit, on_new_commit))
    poll_thread.daemon = True
    poll_thread.start()

    while True:
        ui = input('> ')
        match ui:
            case 'CI':
                print('> CI')
            case 'exit':
                print('> Exiting ...')
                break
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Watch a github repo and do some action if there has been a commit')

    # Add an argument
    parser.add_argument('-i', '--interval', type=int, default=60, required=False, help='poll interval (in seconds)')
    parser.add_argument('-r', '--repo', type=str, required=True, help='repository name')
    parser.add_argument('-o', '--owner', type=str, required=True, help='owner/organization')
    parser.add_argument('-b', '--branch', type=str, required=True, help='branch to watch')

    ## Parse the arguments
    args = parser.parse_args()
    
    POLL_INTERVAL = args.interval
    REPO = args.repo
    OWNER = args.owner
    BRANCH = args.branch

    #print(POLL_INTERVAL, REPO, OWNER, BRANCH, sep=', ')

    main(POLL_INTERVAL, REPO, OWNER, BRANCH)