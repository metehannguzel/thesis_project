import requests

response = requests.get('ngrok url')
print(response.text)

####################################################################################################

"""import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect("ngrok url")

print(client.recv(1024).decode())
client.send("Client is running!".encode())"""
