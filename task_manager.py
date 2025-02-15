from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
deleted_tasks = []

def save_deleted_tasks_to_file():
    with open('Deleted_tasks.txt', 'w') as f:
        f.write(f"Deleted Tasks:\n")
        for task in deleted_tasks:
            f.write(f"{task['id']} : {task['name']}\n")


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, deleted_tasks=deleted_tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    if task_name:
        new_task = {'id': len(tasks) + 1, 'name': task_name}
        tasks.append(new_task)
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks, deleted_tasks
    task_to_delete = next((task for task in tasks if task['id'] == task_id), None)
    if task_to_delete:
        tasks = [task for task in tasks if task['id'] != task_id]
        deleted_tasks.append(task_to_delete)
        if len(deleted_tasks) > 10:
            save_deleted_tasks_to_file()
            deleted_tasks.clear()
    return redirect(url_for('index'))


@app.route('/terminate')
def terminate_deleted_tasks():
    global deleted_tasks
    save_deleted_tasks_to_file()
    deleted_tasks.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)