import sys
import os
import json
import importlib
from urllib.parse import urlparse
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime

if len(sys.argv) != 3:
    print("Usage: python server/test_task.py <task_rel_path> <json_basename>")
    print("Example: python server/test_task.py norbi/task3 task3_post.json")
    sys.exit(1)

# Ensure we're in the server directory context
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

task_rel_path = sys.argv[1].rstrip('.py')
json_basename = sys.argv[2]
script_dir = os.path.dirname(os.path.abspath(__file__))
request_json_path = os.path.join(script_dir, "captured_requests", json_basename)

# Parse task_rel_path for filename
parts = task_rel_path.split('/')
task_folder = parts[0] if len(parts) > 1 else ''
task_file = parts[-1]
task_name = f"{task_folder}_{task_file}" if task_folder else task_file

# Construct module name: norbi/task3 -> tasks.norbi.task3
task_module_name = f"tasks.{task_rel_path.replace('/', '.')}"

try:
    module = importlib.import_module(task_module_name)
except ImportError as e:
    print(f"Failed to import module {task_module_name}: {e}")
    sys.exit(1)

if not hasattr(module, 'router'):
    print(f"Module {task_module_name} does not have a 'router' attribute.")
    sys.exit(1)

app = FastAPI()
app.include_router(module.router)

client = TestClient(app)

try:
    with open(request_json_path, 'r', encoding='utf-8') as f:
        requests_data = json.load(f)
except FileNotFoundError:
    print(f"Request file {request_json_path} not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Invalid JSON in {request_json_path}: {e}")
    sys.exit(1)

results = []

for i, req in enumerate(requests_data, 1):
    full_url = req['path']
    parsed_url = urlparse(full_url)
    path = parsed_url.path
    query_string = parsed_url.query
    if query_string:
        path += f"?{query_string}"

    # Prepare request
    headers = {k: v for k, v in req['headers'].items() if k.lower() not in ['host', 'content-length']}
    params = req['query_params']
    body = req['body']

    method = req['method'].lower()
    if method == 'get':
        response = client.get(path, headers=headers, params=params)
    elif method == 'post':
        if isinstance(body, dict):
            response = client.post(path, json=body, headers=headers, params=params)
        else:
            response = client.post(path, data=body if body else None, headers=headers, params=params)
    elif method == 'put':
        if isinstance(body, dict):
            response = client.put(path, json=body, headers=headers, params=params)
        else:
            response = client.put(path, data=body if body else None, headers=headers, params=params)
    else:
        results.append({
            'request_index': i,
            'request': req,
            'error': f"Unsupported method: {method}"
        })
        continue

    try:
        response_data = response.json()
        body_data = response_data
    except ValueError:
        body_data = {'text': response.text, 'note': 'non-JSON response'}

    results.append({
        'request_index': i,
        'request': req,
        'response': {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': body_data
        }
    })

test_results_dir = os.path.join(script_dir, "test_results")
os.makedirs(test_results_dir, exist_ok=True)

normalized_filename = f"{task_name}.json"
results_filepath = os.path.join(test_results_dir, normalized_filename)

results_data = {
    'timestamp': datetime.now().isoformat(),
    'task_module': task_module_name,
    'input_json': json_basename,
    'num_requests': len(requests_data),
    'results': results
}

with open(results_filepath, 'w', encoding='utf-8') as f:
    json.dump(results_data, f, indent=2, ensure_ascii=False)

print(f"Test results saved to: {results_filepath}")