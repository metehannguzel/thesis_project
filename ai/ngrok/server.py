import socket
import subprocess
import os
import json

model_script_path = os.path.join(os.getcwd(), "main.py")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 80))

server.listen()

while True:
    client, addr = server.accept()
    client.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n".encode())
    result = subprocess.run(["python", model_script_path], capture_output=True, text=True)

    if result.returncode == 0 and result.stdout:
        stdout_data = result.stdout
        start_index = stdout_data.rfind("{")
        end_index = stdout_data.rfind("}") + 1

        if start_index != -1 and end_index != -1:
            json_string = stdout_data[start_index:end_index]
            try:
                response_data = json.loads(json_string)
                response = json.dumps(response_data)
                print(response)
                client.send(response.encode())
            except json.JSONDecodeError:
                client.send("Error decoding JSON output.".encode())
        else:
            client.send("No valid JSON data found in script output.".encode())
    else:
        print("Error:", result.stderr)
        client.send(f"Error: {result.stderr}".encode())

    client.close()

# CMD
# 
# cd C:\Users\guzel\OneDrive\Documents\thesis\thesis_project\ngrok -> 1
# 
# ngrok.exe http 9999
#
# ngrok http --domain=redbird-free-literally.ngrok-free.app 80 -> 2
# 
# ngrok.exe tcp 9999

# ----------------------------------------------------------------------------------------------------

# ANACONDA PROMPT
# 
# conda activate pt_gpu
# 
# cd C:\Users\guzel\OneDrive\Documents\thesis\thesis_project\ngrok
# 
# python -m http.server 9999
