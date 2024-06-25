import socket
import threading
import os
CAMINHO_ARQUIVO = "D:/Faculdade/Redes/"

# Função para lidar com a requisição do cliente
def handle_client(client_socket):
    try:
        # Recebe a requisição do cliente
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Recebido: {request}")

        # Processa a linha de requisição HTTP
        lines = request.split("\r\n")
        if len(lines) > 0:
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) == 3 and parts[0] == 'GET':
                file_path = parts[1][1:]  # Remove a barra inicial

                if not file_path:
                    file_path = 'index.html'  # Arquivo padrão
                file_path = CAMINHO_ARQUIVO + file_path
                # Verifica se o arquivo requisitado existe
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as file:
                        response_body = file.read()

                    # Determina o tipo de conteúdo
                    if file_path.endswith('.html'):
                        content_type = 'text/html'
                    elif file_path.endswith('.jpeg') or file_path.endswith('.jpg'):
                        content_type = 'image/jpeg'
                    else:
                        content_type = 'application/octet-stream'

                    # Constrói a resposta HTTP
                    response = f"HTTP/1.0 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode('utf-8')
                    response += response_body
                else:
                    # Arquivo não encontrado
                    response = "HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode('utf-8')
                    response += b"<html><body><h1>404 Not Found</h1></body></html>"

                # Envia a resposta ao cliente
                client_socket.send(response)
            else:
                # Requisição HTTP mal formatada
                response = "HTTP/1.0 400 Bad Request\r\nContent-Type: text/html\r\n\r\n".encode('utf-8')
                response += b"<html><body><h1>400 Bad Request</h1></body></html>"
                client_socket.send(response)
    finally:
        # Fecha a conexão com o cliente
        client_socket.close()


# Função principal do servidor
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escutando em {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão aceita de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 8080  # Pode ajustar a porta conforme necessário
    start_server(HOST, PORT)