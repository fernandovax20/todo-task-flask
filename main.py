from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

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
    try:
        data = TODO.query.all()
        return render_template('index.html.j2', todos=data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todo-detail/<int:id>', methods=['GET'])
def todoDetail(id):
    try:
        todo = TODO.query.get(id)
        tasks = TASK.query.filter_by(todo_id=id).all()
        # tasks = db.session.query(TASK).join(TODO).filter(TASK.todo_id == id).all()
        return render_template('todo_detail.html.j2', todo=todo, tasks=tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create-todo', methods=['POST'])
def createTodo():
    try:
        nombre = request.form.get('name')
        todo = TODO(nombre=nombre)
        db.session.add(todo)
        db.session.commit()
        return jsonify({'message': 'Todo creado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-todo/<int:id>', methods=['DELETE'])
def deleteTodo(id):
    try:
        todo = TODO.query.with_for_update().get(id)
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @ Tasks =================================================================
@app.route('/create-task', methods=['POST'])
def createTask():
    try:
        nombre = request.form.get('name')
        todo_id = request.form.get('todo_id')
        task = TASK(nombre=nombre, todo_id=todo_id)
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task creado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-task/<int:id>', methods=['DELETE'])
def deleteTask(id):
    try:
        task = TASK.query.with_for_update().get(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-task/<int:id>', methods=['PUT'])
def updateTask(id):
    try:
        task = TASK.query.with_for_update().get(id)
        task.nombre = request.form.get('name')
        db.session.commit()
        return jsonify({'message': 'Task actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @ Inicializar base de datos ============================================
with app.app_context():
    
    def obtener_todos():
        response = requests.get('https://dummyjson.com/todos?limit=10&skip=0')
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'No se pudo obtener los datos'}

    db.create_all()
    if not TODO.query.first():
        todo_data = [
            ('Crear frontend', ['Comprender requerimientos', 'diagramar flujos', 'desarrollar mock up']),
            ('Desarrollar Backend', []),
        ]

        todos = obtener_todos()
        todo_data = todo_data + [(todo["todo"], []) for todo in todos["todos"]]
        # todo_data.extend([(todo["todo"], []) for todo in todos["todos"]])

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
