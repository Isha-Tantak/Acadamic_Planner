from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.String(20), nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

# Home Page: View Tasks
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.priority).all()
    return render_template('index.html', tasks=tasks)

# Add Task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        priority = request.form['priority']
        due_date = request.form['due_date']
        new_task = Task(title=title, priority=priority, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Update Task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.priority = request.form['priority']
        task.due_date = request.form['due_date']
        task.is_complete = 'is_complete' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_task.html', task=task)

# Delete Task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Mark Task Complete
@app.route('/complete/<int:id>')
def mark_complete(id):
    task = Task.query.get_or_404(id)
    task.is_complete = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
