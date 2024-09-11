# [Markdown Note-taking App](https://roadmap.sh/projects/markdown-note-taking-app).
You are required to build a simple note-taking app that lets users upload markdown files, check the grammar, save the note, and render it in HTML. The goal of this project is to help you learn how to handle file uploads in a RESTful API, parse and render markdown files using libraries, and check the grammar of the notes.


## Features
You have to implement the following features:
- You’ll provide an endpoint to check the grammar of the note.
- You’ll also provide an endpoint to save the note that can be passed in as Markdown text.
- Provide an endpoint to list the saved notes (i.e. uploaded markdown files).
- Return the HTML version of the Markdown note (rendered note) through another endpoint.


## Demo
Here's a simple demo of how the application should work:
[Watch the demo](https://youtu.be/2wgb0G9moRE)


## Usage
### Apply all Migrations
Open your teminal and enter the command below to apply migrations:
```bash
python manage.py migrate
```

### Start the Server
To access the web app start the server with the command below:
```bash
python manage.py runserver
```

### View the Web App
Launch your browser and access the web app using the link below:
```
http://127.0.0.1:8000/
```


## Notes
- Ensure that you are in the application project directory to run all the above command.
