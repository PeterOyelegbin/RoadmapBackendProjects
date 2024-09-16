# [Workout Tracker](https://roadmap.sh/projects/fitness-workout-tracker).
This project involves creating a backend system for a workout tracker application where users can sign up, log in, create workout plans, and track their progress. The system will feature JWT authentication, CRUD operations for workouts, and generate reports on past workouts.


## Requirements
You are required to develop an API for a workout tracker application that allows users to manage their workouts and track their progress. Your first task is to think about the database schema and the API endpoints that will be needed to support the application’s functionality. Here are some of the key features you should consider:

### Exercise Data
You should write a data seeder to populate the database with a list of exercises. Each exercise should have a name, description, and category (e.g., cardio, strength, flexibility) or muscle group (e.g., chest, back, legs). Exercises will be used to create workout plans.

### User Authentication and Authorization
Users will be able to sign up, log in, and log out of the application. You should use JWT tokens for authentication and authorization. Only authenticated users should be able to create, update, and delete workout plans. Needless to say, users should only be able to access their own workout plans.
- Sign-Up: Allow users to create an account.
- Login: Allow users to log in to their account.
- JWT: Use JSON Web Tokens for authentication.

### Workout Management
Users will be able to create their workout plans. Workout plans should consist of multiple exercises, each with a set number of repetitions, sets, and weights. Users should be able to update and delete their workout plans. Additionally, users should be able to schedule workouts for specific dates and times.
- Create Workout: Allow users to create workouts composed of multiple exercises.
- Update Workout: Allow users to update workouts and add comments.
- Delete Workout: Allow users to delete workouts.
- Schedule Workouts: Allow users to schedule workouts for specific dates and times.
- List Workouts: List active or pending workouts sorted by date and time.
- Generate Reports: Generate reports on past workouts and progress.


## Demo
Here's a simple demo of how the application should work:
[Watch the video](https://www.youtube.com/watch?v=IyHRBj_iKY0)


## Usage
### Install Dependencies
Open your teminal and enter the command below to install needed dependencies:
```bash
pip install -r requirements.txt
```

### Start the Server
To start the broadcast server, use the command below:
```bash
python broadcast-server.py start
```

### Coonect to the Server
Open a new terminal and enter the command below to connect to the server already running as shown below:
```bash
python broadcast-server.py connect
```
