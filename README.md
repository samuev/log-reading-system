
# Log Reading System

This system is designed to read and check patterns in a specified log file. It consists of three main components: a MongoDB database, a Flask REST server, and a Python queue system.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository from the repo root directory:

```bash
git clone <repository_url>
cd <repository_directory>
cd app
```

2. Build and start the Docker containers:

```bash
docker-compose up -d
```
## Creating a User for Your MongoDB Database
The user created automatically by mongo-init.js script that used by docker-compose and this user used by the flask app

3. Enter the MongoDB Docker container:

```bash
docker exec -it mongodb bash
```

4. Log in to the MongoDB root administrative account:

```bash
mongosh -u root -p rootpassword
```

5. Switch to the 'logsdb' database:

```bash
use logsdb
```

6. View database entries after sending REST requests:

```bash
db.logs.find()
```

7. Exit the MongoDB shell:

```bash
exit
```

8. Exit the container:

```bash
exit
```

## Usage

The system provides several endpoints for managing log files:

- `POST /check-pattern`: Enqueues a job to check patterns in a specified log file.If patterns are found, they are stored in the MongoDB database along with the log file name and log file size.
- `GET /searched-logs`: Returns the names of log files that have been searched and the patterns found in them, if any.
- `DELETE /delete-log`: Deletes a log from the database.

## REST examples
In this examples, replace "log1.txt" with the name of the log file you want to proceed from /logs directory
```bash
curl -X POST -H "Content-Type: application/json" -d '{"filename":"log1.txt"}' http://localhost:5000/check-pattern
curl -X GET http://localhost:5000/searched-logs
curl -X DELETE "http://localhost:5000/delete-log?log_file_name=log1.txt"
curl -X DELETE "http://localhost:5000/delete-log?log_id=log_id"
```
## Environment Variables

The system uses the following environment variables:

- `MONGODB_USERNAME`: The username for the MongoDB database.
- `MONGODB_PASSWORD`: The password for the MongoDB database.

These variables are set in the `docker-compose.yml` file.

## Dockerization
The entire solution is dockerized, which means it can be easily set up and run on any system with Docker installed. The Docker Compose file in the app directory of the project defines the services that make up the application (the Flask server and the MongoDB database), and the Dockerfiles define the environment and the dependencies needed to run the services.

## Unittest 
In this project I created two separate unittests:
1. test_app.py - for functional testing
2. unittest_flask.py - testing Rest api with mock db 
```bash
python -m unittest test_app.TestCheckPatternsInFile
```
```bash
python -m unittest unittest_flask.FlaskTestCase 
```

## Contributing

Contributions are welcome. Please open an issue.
