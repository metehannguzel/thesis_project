import requests

response = requests.get("https://redbird-free-literally.ngrok-free.app")
print(response.text)

####################################################################################################

"""import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect("68a9-31-223-46-159.ngrok-free.app")

print(client.recv(1024).decode())
client.send("Client is running!".encode())"""