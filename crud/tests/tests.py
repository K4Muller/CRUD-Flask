#Teste automatizado
import pytest
import requests

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

#Create
def test_create_task():
    #Dados
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }

    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data) #envio de dados
    
    assert response.status_code == 200 #Validação
    response_json = response.json() #Variavel para armazenar msg
    assert "message" in response_json #validação de msg
    assert "id" in response_json #Verificação de se id existe
    tasks.append(response_json['id'])

#Read todos
def test_get_tasks():
    #Linha que vai pegar o codigo http ex (200, 404)
    response = requests.get(f"{BASE_URL}/tasks")
    #Verifica se foi 200
    assert response.status_code == 200
    #Pega o conteudo json
    response_json = response.json()
    
    #Checa as msgs json
    assert "tasks" in response_json
    assert "total_tasks" in response_json


#Read individual
def test_get_task():
    if tasks:
        #Pega o primeiro elemento da lista tasks
        task_id = tasks[0]

        #Pega codigo http
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        
        #Verifica codigo http
        assert response.status_code == 200
        #Pega a msg json
        response_json = response.json()
        #Faz a verificação
        assert task_id == response_json['id']


#Update
def test_update_tast():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": False,
            "description": "Nova att",
            "title": "Titulo atualizado"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        
        response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        #Nova requisição para nova validação
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404