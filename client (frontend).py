import socket
import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Online Examination System")
        master.geometry("800x600")  # Larger display window
        
        self.questions_answered = 0  # Track number of questions answered
        self.total_questions = 3  # Total number of questions
        
        self.question_label = tk.Label(master, text="Question:", font=("Helvetica", 16))  # Increase font size
        self.question_label.pack()

        self.question_text = tk.StringVar()
        self.question_display = tk.Label(master, textvariable=self.question_text, font=("Helvetica", 14), wraplength=700)  # Increase font size and adjust wrap length for longer questions
        self.question_display.pack()

        self.answer_label = tk.Label(master, text="Your answer:", font=("Helvetica", 16))  # Increase font size
        self.answer_label.pack()

        self.answer_entry = tk.Entry(master, width=50, font=("Helvetica", 14))  # Increase width and font size of entry box
        self.answer_entry.pack()

        self.submit_button = tk.Button(master, text="Submit Answer", font=("Helvetica", 14), command=self.submit_answer)  # Increase font size
        self.submit_button.pack()

        self.score_label = tk.Label(master, text="", font=("Helvetica", 16))  # Increase font size
        self.score_label.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.0.111', 12345))

        self.receive_question()

    def receive_question(self):
        if self.questions_answered >= self.total_questions:
            self.question_text.set("No more questions. Exam is finished.")
            self.answer_entry.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.receive_score()  # Receive and display final score
            return

        question = self.client_socket.recv(1024).decode()
        if question == "":
            messagebox.showinfo("Exam Finished", "No more questions. Exam is finished.")
            self.receive_score()  # Receive and display final score
            return

        self.question_text.set(question)
        self.questions_answered += 1

    def submit_answer(self):
        answer = self.answer_entry.get().strip()
        if answer:
            self.client_socket.sendall(answer.encode())
            self.answer_entry.delete(0, tk.END)  # Clear answer entry
            self.receive_question()  # Get next question
        else:
            messagebox.showwarning("Invalid Answer", "Please enter your answer.")

    def receive_score(self):
        score = self.client_socket.recv(1024).decode()
        self.score_label.config(text=f"Your final score is: {score}")

def main():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
