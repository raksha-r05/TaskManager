import requests

# Delete all existing tasks at the beginning
print("Deleting all existing tasks...")
response = requests.get("http://localhost:8002/api/v1/tasks/")
existing_tasks = response.json()
for task in existing_tasks:
    task_id = task["id"]
    delete_response = requests.delete(f"http://localhost:8002/api/v1/tasks/{task_id}")
    #print(f"Deleted task {task_id}: {delete_response.status_code}")

print("All existing tasks deleted.")
print('--------------------------------')

response = requests.post("http://localhost:8002/api/v1/tasks/", json={
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "priority": 1
})
task_id = response.json()["id"]
#print(response.json())

response = requests.get("http://localhost:8002/api/v1/tasks/")
print(response.json())
print('--------------------------------')

response = requests.put(f"http://localhost:8002/api/v1/tasks/{task_id}", json={
    "title": "Buy groceries and fruits",
    "description": "Milk, bread, eggs and fruits",
    "priority": 1
})
#print(response.json())

response = requests.get("http://localhost:8002/api/v1/tasks/")
print(response.json())
print('--------------------------------')

response = requests.delete(f"http://localhost:8002/api/v1/tasks/{task_id}")
print("Delete response status:", response.status_code)
#print(response.json())