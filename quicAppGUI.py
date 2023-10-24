import tkinter as tk
from tkinter import messagebox
import json

# Define a class QuizApp
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz")
        
        # Load questions from a JSON file
        self.questions = self.load_questions("data.json")
        
        # Initialize variables
        self.current_question = 0
        self.score = 0
        self.selected_option = tk.StringVar(value=None)
        self.wrong_answers = []
        self.score_window = None
        self.timer = 30
        self.timer_id = None

        # Set the initial window geometry to full screen
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        # Create and pack the question label
        self.question_label = tk.Label(root, text="", font=("Arial", 14))
        self.question_label.pack()

        # Create and pack the option buttons
        self.option_buttons = []
        for i in range(4):
            option_button = tk.Radiobutton(root, text="", variable=self.selected_option, value=str(i+1))
            self.option_buttons.append(option_button)
            option_button.pack()

        # Create and pack the "Next" button
        self.next_button = tk.Button(root, text="Next", command=self.check_answer, fg="black")
        self.next_button.pack()

        # Create and pack the "Finish Test" button
        self.finish_button = tk.Button(root, text="Finish Test", command=self.finish_test, fg="black")
        self.finish_button.pack()

        # Create and pack the score label
        self.score_label = tk.Label(root, text="")
        self.score_label.pack()

        # Create and pack the timer label
        self.timer_label = tk.Label(root, text="", font=("Arial", 14), fg="black")
        self.timer_label.pack(side=tk.RIGHT)

        # Load the first question and start the timer
        self.load_next_question()
        self.update_timer()

    # Function to load questions from a JSON file
    def load_questions(self, filename):
        with open(filename, 'r') as file:
            questions = json.load(file)
        return questions

    # Function to load the next question
    def load_next_question(self):
        if 0 <= self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            question_text = question_data["question"]
            options = question_data["options"]
            self.correct_answer = question_data["correct_answer"]
            self.question_label.config(text=f"Q{self.current_question + 1}: {question_text}")
            for i, option_button in enumerate(self.option_buttons):
                option_button.config(text=options[i])
            self.selected_option.set(None)
        else:
            self.submit_quiz()

    # Function to check the selected answer
    def check_answer(self):
        if self.selected_option.get():
            selected_answer = int(self.selected_option.get())
            if selected_answer == self.correct_answer:
                self.score += 1
            else:
                self.wrong_answers.append(self.current_question + 1)
            self.current_question += 1
            self.load_next_question()

    # Function to submit the quiz
    def submit_quiz(self):
        self.show_score_and_wrong_answers()
        self.next_button.config(state="disabled")
        self.finish_button.config(state="disabled")
        self.timer_label.config(text="Time's up!")
        self.stop_timer()

    # Function to display the score and wrong answers
    def show_score_and_wrong_answers(self):
        score_text = f"Your score: {self.score}/{len(self.questions)}"
        wrong_answers_text = ""
        if self.wrong_answers:
            wrong_answers_text = "\nWrong Answers:\n"
            for question_number in self.wrong_answers:
                question_data = self.questions[question_number - 1]
                question_text = question_data["question"]
                correct_answer = question_data["options"][question_data["correct_answer"] - 1]
                wrong_answers_text += f"Q{question_number}: {question_text}\nCorrect Answer: {correct_answer}\n"

        # Create a new window to display the score
        self.score_window = tk.Toplevel(self.root)
        self.score_window.title("Quiz Score")
        score_label = tk.Label(self.score_window, text=score_text + wrong_answers_text, font=("Arial", 14))
        score_label.pack()

        # Create a button to retake the quiz
        retry_button = tk.Button(self.score_window, text="Retake Quiz", command=self.restart_quiz)
        retry_button.pack()

    # Function to restart the quiz
    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []
        self.next_button.config(state="active")
        self.finish_button.config(state="active")
        self.score_label.config(text="")
        self.timer = 30
        self.load_next_question()
        self.update_timer()

        # Hide the score window (if it exists) without closing it
        if self.score_window and self.score_window.winfo_exists():
            self.score_window.withdraw()

    # Function to finish the quiz
    def finish_test(self):
        self.submit_quiz()

    # Function to update the timer
    def update_timer(self):
        if self.timer > 0:
            timer_color = "red" if self.timer < 10 else "black"
            self.timer_label.config(text=f"Time Left: {self.timer} sec", fg=timer_color)
            next_button_color = "green" if self.timer > 10 else "black"
            finish_button_color = "red" if self.timer <= 10 else "black"
            
            self.next_button.config(fg=next_button_color)
            self.finish_button.config(fg=finish_button_color)
            
            self.timer -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.timer == 0:
            self.submit_quiz()
            self.timer = -1

    # Function to stop the timer
    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

if __name__ == "__main__":
    # Create a Tkinter window and initialize the QuizApp
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
