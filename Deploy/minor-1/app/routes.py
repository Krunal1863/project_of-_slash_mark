# from flask import render_template, request, redirect, url_for
# from app import app

# # In-memory task list
# tasks = []

# # Route for the home page
# @app.route('/')
# def index():
#     return render_template('index.html', tasks=tasks)

# # Route to add a task
# @app.route('/add', methods=['POST'])
# def add_task():
#     description = request.form.get('description')
#     priority = request.form.get('priority')
#     if description and priority:
#         tasks.append({'description': description, 'priority': priority})
#     return redirect(url_for('index'))

# # Route to remove a task
# @app.route('/remove/<int:task_id>')
# def remove_task(task_id):
#     if 0 <= task_id < len(tasks):
#         tasks.pop(task_id)
#     return redirect(url_for('index'))

# # Route to prioritize tasks (sort by priority)
# @app.route('/prioritize')
# def prioritize_tasks():
#     priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
#     tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
#     return redirect(url_for('index'))

from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.csv"

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["description", "priority"])
        writer.writeheader()
        writer.writerows(tasks)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    description = request.form["description"]
    priority = request.form["priority"]
    tasks = load_tasks()
    tasks.append({"description": description, "priority": priority})
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/remove/<int:task_index>")
def remove_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/prioritize")
def prioritize_tasks():
    tasks = load_tasks()
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 4))
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/download")
def download_csv():
    return send_file(TASKS_FILE, as_attachment=True, download_name="tasks.csv")

if __name__ == "__main__":
    app.run(debug=True)