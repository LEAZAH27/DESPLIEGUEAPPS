import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

public class ChatClient {
    private static final String HOST = "192.168.1.35"; // Cambia por la IP del servidor
    private static final int PORT = 5000;

    public static void main(String[] args) {
        try {
            Socket socket = new Socket(HOST, PORT);
            System.out.println("Conectado al servidor en " + HOST + ":" + PORT);

            // Hilo receptor: escucha mensajes entrantes del servidor
            Thread receiverThread = new Thread(() -> {
                try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"))) {
                    String line;
                    while ((line = in.readLine()) != null) {
                        System.out.println("\n" + line);
                        System.out.print("Tú: ");
                    }
                } catch (IOException e) {
                    System.out.println("\nConexión cerrada por el servidor.");
                }
            });
            receiverThread.setDaemon(true);
            receiverThread.start();

            // Hilo emisor: envía texto ingresado en consola
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in);

            System.out.print("Tú: ");
            while (scanner.hasNextLine()) {
                String message = scanner.nextLine();
                if (message.equalsIgnoreCase("salir") || message.equalsIgnoreCase("exit")) {
                    break;
                }
                out.println(message); // Envía texto con terminación \n
                System.out.print("Tú: ");
            }

            socket.close();
            scanner.close();
        } catch (IOException e) {
            System.err.println("Error de conexión: " + e.getMessage());
        }
    }
}
