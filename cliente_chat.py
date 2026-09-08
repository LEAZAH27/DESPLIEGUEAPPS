import socket

HOST = "192.168.1.35"  # IP de la computadora con el servidor
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Conectado a {HOST}:{PORT}")

while True:
    # Enviar mensaje
    msg = input("Tú: ")
    if msg.lower() in ("salir", "exit"):
        break
    client.sendall(msg.encode())

    # Recibir respuesta
    data = client.recv(1024)
    if not data:
        break
    print(f"[Servidor]: {data.decode().strip()}")

client.close()