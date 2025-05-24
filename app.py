from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id = 1

# Rota para Criar Tarefas
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not isinstance(title, str) or not isinstance(description, str):
        return jsonify({'error': 'Título e descrição devem ser strings!'}), 400
    new_task = Task(id=task_id, title=title, description=description, completed=False)
    task_id += 1
    tasks.append(new_task)
    return jsonify({'message': 'Nova tarefa criada com sucesso!'})

# Rota para buscar todas as tarefas
@app.route('/tasks', methods=['GET'])
def search_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(tasks)
    }
    return jsonify(output)

# Rota para buscar tarefa por título
@app.route('/tasks/<title>', methods=['GET'])
def get_title(title):
    for t in tasks:
        if t.title == title:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar esta tarefa!"}), 404

# Rota para atualizar tarefa
@app.route('/tasks/<title>', methods=['PUT'])
def update_task(title):
    task = next((t for t in tasks if t.title == title), None)
    if task is None:
        return jsonify({"error": "Tarefa não encontrada!"}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200

# Rota para Deletar tarefa
@app.route('/tasks/delete-task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = next((t for t in tasks if t.id == id), None)
    if not task:
        return jsonify({'message': 'Tarefa não encontrada!'}), 404
    tasks.remove(task)
    return jsonify({'message': 'Tarefa deletada com sucesso'}), 200

if __name__ == "__main__":
    app.run(debug=True)