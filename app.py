from flask import Flask, request, jsonify
from models.task import Taks

app = Flask(__name__)

tasks = []
task_id = 1

'''ROTA PARA CRIAR TAREFAS'''
@app.route('/tasks', methods=['POST'])
def create_task():
  global task_id
  data = request.get_json()
  new_task = Taks(id=task_id, title=data.get('title'), description=data.get('description'), completed=False)
  task_id += 1
  tasks.append(new_task)
  return jsonify({'message': 'Nova tarefas criada com Sucesso!'})


'''ROTA PARA BUSCAR TAREFAS'''
@app.route('/tasks', methods=['GET'])
def search_tasks():
  task_list = [task.to_dict() for task in tasks]
  output = {          
          "tasks": task_list,
          "total_tasks" : 0
  }
  return jsonify(output)

if __name__ == "__main__":
  app.run(debug=True)