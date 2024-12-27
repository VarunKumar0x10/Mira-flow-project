import os
from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
import tkinter as tk
from tkinter import ttk, messagebox

class StudyCompanionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Companion")
        self.client = self.initialize_client()
        self.create_main_menu()

    def initialize_client(self):
        load_dotenv()
        api = os.getenv("API_KEY")
        return MiraClient(config={"API_KEY": api})

    def create_main_menu(self):
        # Main menu
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Study Companion", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Study & Homework Help", command=self.handle_study_homework).grid(row=1, column=0, padx=10, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="Stress & Anxiety Management", command=self.handle_stress_anxiety).grid(row=2, column=0, padx=10, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="Astrology Guidance", command=self.handle_astrology).grid(row=3, column=0, padx=10, pady=5, sticky=tk.EW)
        ttk.Button(frame, text="What I Can Do", command=self.show_info_window).grid(row=4, column=0, padx=10, pady=5, sticky=tk.EW)

        self.output_text = tk.Text(frame, wrap=tk.WORD, height=20, width=70)
        self.output_text.grid(row=5, column=0, pady=10, columnspan=2)

    def display_output(self, output):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def show_error_message(self, error_message):
        messagebox.showerror("Error", error_message)

    def handle_study_homework(self):
        self.show_input_dialog(
            "Study & Homework Help",
            [("Class/Level", "input1"), ("Topic", "input2"), ("Query", "input3"), ("Desired Answer Length (Optional)", "input4")],
            "@varunkumar0x10/study-companion",
        )

    def handle_stress_anxiety(self):
        self.show_input_dialog(
            "Stress & Anxiety Management",
            [("Source of Stress/Anxiety", "stress_reason")],
            "@varunkumar0x10/stress-buster",
        )

    def handle_astrology(self):
        self.show_input_dialog(
            "Astrology Guidance",
            [("Astrological Query", "question"), ("Birth Details", "birth_details")],
            "@cosmic-labs/ai-astrologer",
        )

    def show_input_dialog(self, title, input_fields, flow_name):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        inputs = {}

        ttk.Label(dialog, text=title, font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        for idx, (label, key) in enumerate(input_fields):
            ttk.Label(dialog, text=label).grid(row=idx + 1, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(dialog, width=40)
            entry.grid(row=idx + 1, column=1, padx=5, pady=5)
            inputs[key] = entry

        def submit():
            input_data = {key: entry.get() for key, entry in inputs.items()}
            self.display_loading_message()
            self.root.after(100, lambda: self.run_flow(flow_name, input_data))  # Execute flow after showing the message
            dialog.destroy()

        ttk.Button(dialog, text="Submit", command=submit).grid(row=len(input_fields) + 1, column=0, columnspan=2, pady=10)

    def display_loading_message(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Loading, please wait...")

    def run_flow(self, flow_name, input_data):
        try:
            response = self.client.flow.execute(flow_name, input_data)
            output = response["result"]
            self.display_output(output)
        except Exception as e:
            self.show_error_message(str(e))

    def show_info_window(self):
        info_text = """
        This program can assist you in various ways:

        Academic Support:
        - Get help with your studies and homework:
          - Ask questions about specific concepts in your textbooks.
          - Receive explanations for challenging problems in mathematics, 
            science, and other subjects.
          - Get help with essay writing, research, and project ideas.

        Stress Management:
        - Find effective ways to cope with stress and anxiety:
          - Receive personalized stress-management tips based on your specific 
            concerns.
          - Explore calming techniques such as deep breathing, mindfulness, and 
            meditation.
          - Get suggestions for relaxation exercises and healthy lifestyle 
            habits.

        Astrology Guidance:
        - Seek insights into your astrological chart:
          - Explore your strengths, weaknesses, and personality traits based on 
            your birth date and time.
          - Gain insights into your career potential and future prospects.
          - Ask questions like: "When will I get a job/college?", "Do I have the 
            potential for IIT?", or "What are my career options based on my 
            astrology?"

        This program aims to be a helpful resource for your academic, emotional, 
         and personal growth.

        Sample inputs:
        1. Study & Homework Help:

            Class/Level: 8th Grade
            Topic: Biology
            Query: What is photosyntesis?
            Desired Answer Length (Optional): Short
        2. Stress & Anxiety Management:

            Source of Stress/Anxiety: Upcoming exams and feeling overwhelmed by 
            the workload.
        3. Astrology Guidance:

            Astrological Query: When can I expect to find a stable job in my 
            career?
            Birth Details: 05/12/1998, 10:30 AM, Mumbai, India

        Developed by Varun Kumar
        """
        info_window = tk.Toplevel(self.root)
        info_window.title("What I Can Do")

        ttk.Label(info_window, text="What I Can Do", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, padx=10)

        text_box = tk.Text(info_window, wrap=tk.WORD, height=25, width=80)
        text_box.insert(1.0, info_text)
        text_box.config(state=tk.DISABLED)
        text_box.grid(row=1, column=0, padx=10, pady=10)

# Initialize the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyCompanionApp(root)
    root.mainloop()
