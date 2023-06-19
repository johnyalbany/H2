import socket
import threading

quiz_questions = {
    'Python is a case sensitive language True or False?': 't',
    'Python is object-oriented language True or False?': 't',
    'Python is a scripting language True or False?': 't',
    'Python is a open source language True or False?': 't',
    'Python is a compiled language True or False?': 'f',
    'Python is a cross platform language True or False?': 't',
    'Python is a dynamically typed language True or False?': 't',
    'Python runs on the chrome browser True or False?': 'f',
    'Python is a high level language True or False?': 't',
    'Python is a hard to learn language True or False?': 'f',
    'Python is a interpreted language True or False?': 't',
    'Python django library is used for game development True or False?': 'f',
    'Python is a machine language True or False?': 'f',
    'Python is developed by Guido van Rossum True or False?': 't',
    'Python is written in c language True or False?': 't',
    'Variable declaration is implicit in python?': 't',
    'split(), splits the string at the specificed separator, and returns a list true or false?': 't',
    'strip(), returns a trimmed version of the string true or false?': 't',
    'pop() removes the elements at random position?': 'f'
}

client_scores = {}

def handle_client(client_soc, client_address):
    try:
        client_soc.send(str(len(quiz_questions)).encode())

        for question in quiz_questions:
            client_soc.send(question.encode())

            client_ans = client_soc.recv(1024).decode().strip()

            if client_ans.lower() == quiz_questions[question].lower():
                client_scores[client_address] = client_scores.get(client_address, 0) + 1

        score = client_scores.get(client_address, 0)
        client_soc.send(f"Score: {score}/{len(quiz_questions)}\n".encode())

    except ConnectionAbortedError:
        print(f"The connection was aborted by the client.: {client_address}")

    client_soc.close()
    print(f"The client has been disconnected...: {client_address}")

def start_server():
    server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 4444)
    server_soc.bind(server_address)

    server_soc.listen(5)
    print("The server has been initialized and is now awaiting connections...")

    while True:
        client_socket, client_address = server_soc.accept()
        print(f"Connected to {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()

