from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# @ Configuración de la aplicación =========================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///opciones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mi_secreto_super_secreto'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

# @ Modelos ================================================================
class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('TASK', backref='todo', lazy=True)

class TASK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)

# @ Todos =================================================================
@app.route('/')
def index():
    data = TODO.query.all()
    return render_template('index.html.j2', todos = data)

@app.route('/todo-detail/<int:id>', methods=['GET'])
def todoDetail(id):
    todo = TODO.query.get(id)
    tasks = TASK.query.filter_by(todo_id=id).all()
    return render_template('todo_detail.html.j2', todo = todo, tasks = tasks)

@app.route('/create-todo', methods=['POST'])
def createTodo():
    nombre = request.form.get('name')
    todo = TODO(nombre=nombre)
    db.session.add(todo)
    db.session.commit()
    return jsonify({'message': 'Todo creado correctamente'})

@app.route('/delete-todo/<int:id>', methods=['DELETE'])
def deleteTodo(id):
    todo = TODO.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo eliminado correctamente'})


# @ Tasks =================================================================
@app.route('/create-task', methods=['POST'])
def createTask():
    nombre = request.form.get('name')
    todo_id = request.form.get('todo_id')
    task = TASK(nombre=nombre, todo_id=todo_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task creado correctamente'})

@app.route('/delete-task/<int:id>', methods=['DELETE'])
def deleteTask(id):
    task = TASK.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task eliminado correctamente'})

@app.route('/update-task/<int:id>', methods=['PUT'])
def updateTask(id):
    task = TASK.query.get(id)
    task.nombre = request.form.get('name')
    db.session.commit()
    return jsonify({'message': 'Task actualizado correctamente'})


# @ Inicializar base de datos ============================================
with app.app_context():
    db.create_all()
    if not TODO.query.first():
        todo_data = [
            ('Crear frontend', ['Comprender requerimientos', 'diagramar flujos', 'desarrollar mock up']),
            ('Desarrollar Backend', []),
        ]

        for nombre, tasks in todo_data:
            todo = TODO(nombre=nombre)
            db.session.add(todo)
            db.session.commit()

            for task in tasks:
                new_task = TASK(nombre=task, todo_id =todo.id)
                db.session.add(new_task)

        db.session.commit()

# @ Inicializar Servicio ==============================================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
