import redis
import socket
import threading

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            continue

# Function to handle a client's connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                clients.remove(client)
                client.close()
                break
            else:
                redis_client.lpush('chat', message)
                broadcast(message)
        except:
            continue

# Function to listen for incoming client connections
def accept_connections():
    while True:
        client, _ = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

# Create a socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

# List to keep track of connected clients
clients = []

# Start a thread to accept incoming connections
threading.Thread(target=accept_connections).start()

# Continuously retrieve and print messages from Redis
while True:
    message = redis_client.rpop('chat')
    if message:
        print(message.decode('utf-8'))
