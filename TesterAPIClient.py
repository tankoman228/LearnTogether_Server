import socket
import threading
import json
import base64

print("client start")

# подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.3.73', 9540))

# функция для чтения сообщений от сервера
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # если возникла ошибка, то выходим из цикла
            print('An error occurred!')
            client_socket.close()
            break

# функция для отправки сообщений на сервер
def send():
    while True:
        message = input()
        if message == '@':
        
            with open(input("file: "), 'rb') as f:
                file_data = f.read()
                file_data_base64 = base64.b64encode(file_data).decode('utf-8')

                # Отправка файла в виде строки JSON
                data = {'file': file_data_base64}
                client_socket.sendall(json.dumps(data).encode('utf-8'))
        
            #file1 = open(input('choose file'), "rb")
            
            #message = file1.read()
                
            #data = {"file": message}    
            #client_socket.sendall(json.dumps(data))        
        else:
            client_socket.sendall(message.encode())


#потоки для получения сообщений от сервера и отправки

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()