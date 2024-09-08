#!/usr/bin/env python3

import requests, argparse

def github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None
    
def display_event(events):
    if not events:
        print("No activity found or an error occurred.")
        return

    for event in events:
        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name')
        if event_type and repo_name:
            if event_type == 'PushEvent':
                commits = event.get('payload', {}).get('commits', [])
                print(f"Pushed {len(commits)} commits to {repo_name}")
            elif event_type == 'IssuesEvent':
                action = event.get('payload', {}).get('action')
                if action == 'opened':
                    print(f"Opened a new issue in {repo_name}")
            elif event_type == 'WatchEvent':
                print(f"Starred {repo_name}")
            else:
                print(f"{event_type} in {repo_name}")


def main():
    parser = argparse.ArgumentParser(description="Fetch and display recent GitHub activity for a user.")
    parser.add_argument("username", help="GitHub username")
    args = parser.parse_args()
    
    username = args.username
    print(f"Fetching recent activity for GitHub user: {username}")
    
    events = github_activity(username)
    display_event(events)

if __name__ == '__main__':
    main()
