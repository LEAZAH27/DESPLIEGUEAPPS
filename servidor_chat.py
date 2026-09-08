import socket

HOST = "0.0.0.0"  # Escucha en todas las interfaces
PORT = 5000       # Puerto libre

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Esperando conexión en {HOST}:{PORT}...")

client, addr = server.accept()
print(f"Conectado con {addr}")

while True:
    # Recibir mensaje del cliente
    data = client.recv(1024)
    if not data:
        break
    print(f"[Cliente]: {data.decode().strip()}")

    # Responder
    msg = input("Tú: ")
    if msg.lower() in ("salir", "exit"):
        break
    client.sendall(msg.encode())

client.close()
server.close()