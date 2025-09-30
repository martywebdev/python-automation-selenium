import tkinter as tk
import threading
from tkinter import messagebox

from demo_qa_bot import DemoQABot


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Automation GUI")

        # Login section
        login_frame = tk.LabelFrame(self.root, text="Login")
        login_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(login_frame, text="Username").grid(
            row=0, column=0, sticky="w")
        self.entry_username = tk.Entry(login_frame)
        self.entry_username.grid(row=0, column=1, sticky="ew")

        tk.Label(login_frame, text="Password").grid(
            row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(login_frame, show="*")
        self.entry_password.grid(row=1, column=1, sticky="ew")

        # Form section
        form_frame = tk.LabelFrame(self.root, text="Form Data")
        form_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(form_frame, text="Full Name").grid(
            row=0, column=0, sticky="w")
        self.entry_fullname = tk.Entry(form_frame)
        self.entry_fullname.grid(row=0, column=1, sticky="ew")

        tk.Label(form_frame, text="Email").grid(row=1, column=0, sticky="w")
        self.entry_email = tk.Entry(form_frame)
        self.entry_email.grid(row=1, column=1, sticky="ew")

        tk.Label(form_frame, text="Current Address").grid(
            row=2, column=0, sticky="w")
        self.entry_current_address = tk.Entry(form_frame)
        self.entry_current_address.grid(row=2, column=1, sticky="ew")

        tk.Label(form_frame, text="Permanent Address").grid(
            row=3, column=0, sticky="w")
        self.entry_permanent_address = tk.Entry(form_frame)
        self.entry_permanent_address.grid(row=3, column=1, sticky="ew")

        # Make columns expand properly
        for frame in (login_frame, form_frame):
            frame.grid_columnconfigure(1, weight=1)

        # Buttons section
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Run Automation",
                  command=self.run_automation).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", command=self.root.quit).pack(
            side="left", padx=5)
        self.bot = None

    def run_automation(self):
        # Gather inputs
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        fullname = self.entry_fullname.get().strip()
        email = self.entry_email.get().strip()
        current_address = self.entry_current_address.get().strip()
        permanent_address = self.entry_permanent_address.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Error", "Username and Password are required.")
            return

        # Run Selenium in background thread so GUI stays responsive
        def worker():
            try:
                self.bot = DemoQABot(username, password)
                self.bot.login()
                # Optional: use GUI form inputs instead of hardcoded values
                self.bot.fill_text_box_form(
                    fullname=fullname or "John Smith",
                    email=email or "john@gmail.com",
                    current_address=current_address or "Matatag Street Pinyahan Quezon City",
                    permanent_address=permanent_address or "Matatag Street Pinyahan Quezon City",
                )
                self.bot.download_file()
                messagebox.showinfo(
                    "Success", "Automation completed successfully.")
            except Exception as e:
                messagebox.showerror("Automation Failed", str(e))
            finally:
                if self.bot:
                    self.bot.close()

        threading.Thread(target=worker, daemon=True).start()

    def submit_data(self):
        # Example of retrieving values
        data = {
            "username": self.entry_username.get(),
            "password": self.entry_password.get(),
            "fullname": self.entry_fullname.get(),
            "email": self.entry_email.get(),
            "current_address": self.entry_current_address.get(),
            "permanent_address": self.entry_permanent_address.get(),
        }
        print("Submitted data:", data)  # replace with real logic

    def close_browser(self):
        print("Browser closed.")  # replace with real logic


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
