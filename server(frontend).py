# Server code
import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Sample question-answer database
questions = {
    "What does TCP stand for in computer networking?": "Transmission Control Protocol",
    "What does IP stand for in computer networking?": "Internet Protocol",
    "What is the full form of HTTP in web addresses?": "Hypertext Transfer Protocol"
}

def calculate_score(answers):
    score = 0
    for question, answer in answers.items():
        if question in questions and questions[question].lower() == answer.lower():
            score += 1
    return score

def handle_client(client_socket, address):
    try:
        answers = {}
        for i, question in enumerate(questions.keys()):
            if i >= 3:
                break
            client_socket.sendall(question.encode())
            answer = client_socket.recv(1024).decode()
            answers[question] = answer

        score = calculate_score(answers)
        print(f"Score for {address}: {score}")
        client_socket.sendall(str(score).encode())
    except Exception as e:
        print("An error occurred for", address, ":", e)
    finally:
        client_socket.close()

def serve():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.5.152.132', 12345))
    server_socket.listen(5)

    print("Server listening...")

    while True:
        try:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()
        except Exception as e:
            print("An error occurred:", e)

def start_server():
    server_thread = threading.Thread(target=serve)
    server_thread.start()

def main():
    start_server()

if __name__ == "__main__":
    main()
