from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'   # Required for flash messages

# 🔹 Initialize database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')
    conn.commit()
    conn.close()

init_db()

# 🔹 Home route (display tasks)
@app.route('/')
def home():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)

# 🔹 Add task (with duplicate check + flash)
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task'].strip()

    if not task:
        flash("Task cannot be empty!")
        return redirect(url_for('home'))

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    # Check if task already exists
    c.execute('SELECT * FROM tasks WHERE task = ?', (task,))
    existing_task = c.fetchone()

    if existing_task:
        conn.close()
        flash("Task already exists!")
        return redirect(url_for('home'))

    # Insert new task
    c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()

    flash("Task added successfully!")
    return redirect(url_for('home'))

# 🔹 Delete task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash("Task deleted successfully!")
    return redirect(url_for('home'))

# 🔹 Run app
if __name__ == '__main__':
    app.run(debug=True)