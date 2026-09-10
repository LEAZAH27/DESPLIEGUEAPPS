import socket
import threading
import sys

HOST = "192.168.1.35"  # IP de la computadora con el servidor
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Conectado a {HOST}:{PORT}")

def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\nDesconectado del servidor.")
                break
            print(f"\n{data.decode('utf-8').strip()}\nTú: ", end="", flush=True)
        except:
            break
    client.close()
    sys.exit()

receiver_thread = threading.Thread(target=receive_messages, daemon=True)
receiver_thread.start()

while True:
    msg = input("Tú: ")
    if msg.lower() in ("salir", "exit"):
        break
    # Se añade \n para compatibilidad directa con BufferedReader en Java
    client.sendall((msg + "\n").encode("utf-8"))

client.close()
