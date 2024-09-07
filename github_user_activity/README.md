# [GitHub User Activity](https://roadmap.sh/projects/github-user-activity).
In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal. This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.

## Requirements
The application should run from the command line, accept the GitHub username as an argument, fetch the user’s recent activity using the GitHub API, and display it in the terminal. The user should be able to:
- Provide the GitHub username as an argument when running the CLI.
`github-activity <username>`
- Fetch the recent activity of the specified GitHub user using the GitHub API. You can use the following endpoint to fetch the user’s activity:
`https://api.github.com/users/<username>/events`
- Display the fetched activity in the terminal.
```
Output:
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened a new issue in kamranahmedse/developer-roadmap
- Starred kamranahmedse/developer-roadmap
- ...
```
You can learn more about the GitHub API [here](https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28).
- Handle errors gracefully, such as invalid usernames or API failures.
- Use a programming language of your choice to build this project.
- Do not use any external libraries or frameworks to fetch the GitHub activity.


## Usage
### Ensure the script is executable
Open your teminal and enter the command below to enable the script in executable mode:
```bash
chmod u+x github-activity.py
```

### Fetch User Activity
To fetch user activity, use the command below:
```bash
./github-activity.py PeterOyelegbin
```
