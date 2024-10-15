from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

#CRUD
#Create, Read, Update and Delete = criar, ler, atualizar e deletar

tasks = []
task_id_control = 1

#Metodo create
@app.route('/tasks', methods=['POST'])
def create_task():
    #Pegando referencia fora do metodo
    global task_id_control

    data = request.get_json()
    new_task = Task(id=task_id_control, title=data.get('title'), description=data.get('description', ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)

    #Retorno da api
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id})
    #JSONIFY sever para retorna algo em json


#Read
#No read geralmente temos dois end points para ele, temos a listagem de todos os recursos, tudo que eu tenho na minha base. E temos tambem a listagem de um recurso em especifico
@app.route('/tasks', methods=['GET'])
def get_tasks():
    #Modo 2
    tasks_list = [task.to_dict() for task in tasks]   
    #Modo 1
    #for task in tasks:
     #   tasks_list.append(task.to_dict())
    output = {
                "tasks": tasks_list,
                "total_tasks": len(tasks_list)

            }   
    return jsonify(output)

#Criando read com modo de busca, usando identificadores
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404

#Criação de teste sobre parametros de rotas
#@app.route('/user/<float:username_id>')
#def show_user(username_id):
#    print(username_id)
#    print(type(username_id))
#    return "%s" % username_id

#Desnvolvimento da UPDATE
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    print(task)

    if task == None:
        return jsonify({"message": "Não foi possivel encontrar atividade"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({"message": "Tarefa atualizada com sucesso"})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Não foi possivel encontrar a atividade"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Item removido com sucesso"})
            


if __name__ == "__main__":
    app.run(debug=True)