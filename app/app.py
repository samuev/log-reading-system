from typing import Set
from flask import Flask, request, jsonify
import json
import os
from pymongo import MongoClient
import threading
import queue
from collections import deque

import patterns

app = Flask(__name__)
username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
client = MongoClient(f'mongodb://{username}:{password}@mongodb:27017/logsdb')
db = client.logsdb

# initialize the MongoDB database
def init_db():
    db_name = 'logsdb'
    collection_name = 'logs'
    logs_schema = {
        'bsonType': 'object',
        'required': ['log_file_name', 'log_file_size_mb'],
        'properties': {
            'log_file_name': {
                'bsonType': 'string',
                'description': 'must be a string and is required'
            },
            'patterns_found': {
                'bsonType': 'array',
                'items': {
                    'bsonType': 'string',
                    'description': 'must be a string'
                },
                'description': 'must be an array of strings'
            },
            'log_file_size_mb': {
                'bsonType': 'double',
                'description': 'must be a double and is required'
            }
        }
    }

    if db_name not in client.list_database_names():
        db = client[db_name]
        db.create_collection(collection_name, validator={'$jsonSchema': logs_schema})
    else:
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name, validator={'$jsonSchema': logs_schema})


# Create a queue for managing tasks
task_queue = queue.Queue()

# Function to check patterns in the log file
def check_patterns_in_file(file_path: str, patterns_list: Set[str]) -> Set[str]:
    matched_patterns = set()
    with open(file_path, 'r') as file:
        try:
            # skip empty lines after trimming
            messages = [json.loads(line)['message'] for line in file.readlines() if line.strip()]
        except json.JSONDecodeError as e:
            file.seek(0)
            messages = file.readlines()
            # on each line trim all incuding '"message": "' and the postfix '"}'
            messages = [line[line.find('"message": "') + 12:line.rfind('"}')] for line in messages if '"message": "' in line]
            print(f"Recovering from JSONDecodeError in file: {file_path} - {e}")

        merged_messages = ''.join(messages)
        for pattern in patterns_list:
            if pattern in merged_messages:
                matched_patterns.add(pattern)
    return matched_patterns

# Worker function to process tasks from the queue
def worker():
    while True:
        # Get a task from the queue
        task = task_queue.get()
        try:
            process_log_file(*task)
        finally:
            # Mark the task as done
            task_queue.task_done()

# Start worker threads
for _ in range(2):  # Number of worker threads
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# Function to process the log file and add to DB
def process_log_file(filename, patterns_list):
    # Adjust the file_path to the directory where you have stored the log files
    file_path = os.path.join('/usr/src/app/logs', filename)
    if not os.path.exists(file_path):
        return
    found_patterns = check_patterns_in_file(file_path, patterns_list)
    log_file_size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 1)
    # Add to DB if pattern is found
    db.logs.update_one(
        {'log_file_name': filename},
        {'$set': {
            'patterns_found': list(found_patterns),
            'log_file_size_mb': log_file_size_mb
        }},
        upsert=True
    )

@app.route('/check-pattern', methods=['POST'])
def check_pattern():
    filename = request.json.get('filename')
    if not filename:
        return jsonify(error='No filename provided'), 400
    # Add the task to the queue
    task_queue.put((filename, patterns.patterns_set))
    return jsonify(message='Pattern check job enqueued'), 202


# Endpoint to get names of logs files that were searched
@app.route('/searched-logs', methods=['GET'])
def get_searched_logs():
    logs = db.logs.find({}, {'log_file_name': 1})
    if not logs:
        return jsonify(message='No logs have been searched'), 200
    log_names = [log['log_file_name'] for log in logs]
    return jsonify(log_names=log_names), 200

# Endpoint to delete log from DB
@app.route('/delete-log', methods=['DELETE'])
def delete_log():
    log_name = request.args.get('log_file_name')
    log_id = request.args.get('log_id')
    if log_name:
        db.logs.delete_one({'log_file_name': log_name})
        return jsonify(message='Log file name deleted'), 200
    elif log_id:
        db.logs.delete_one({'_id': log_id})
        return jsonify(message='Log ID deleted'), 200
    else:
        return jsonify(error='Wrong Log file name or id required'), 400

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
