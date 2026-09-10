import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
lock = threading.Lock()

def broadcast(message_bytes, sender_socket):
    with lock:
        for client in clients[:]:
            if client != sender_socket:
                try:
                    client.sendall(message_bytes)
                except:
                    clients.remove(client)
                    client.close()

def handle_client(client_socket, addr):
    print(f"[+] Conectado: {addr}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            msg = data.decode("utf-8").strip()
            if not msg:
                continue
                
            formatted_msg = f"[{addr[0]}]: {msg}\n".encode("utf-8")
            broadcast(formatted_msg, client_socket)
        except ConnectionResetError:
            break
        except Exception:
            break

    print(f"[-] Desconectado: {addr}")
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor escuchando en {HOST}:{PORT}...")

while True:
    client_sock, addr = server.accept()
    with lock:
        clients.append(client_sock)
    
    thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
    thread.start()
