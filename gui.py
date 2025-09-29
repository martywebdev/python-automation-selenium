import tkinter as tk


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Web Automation Gui")
        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)
        
        tk.Label(self.login_frame, text='Username').grid(row=0, column=0, sticky='w')
        self.entry_username = tk.Entry(self.login_frame).grid(row=0, column=1, sticky="ew") #this is the input
        
        tk.Label(self.login_frame, text='Password').grid(row=1, column=0, sticky='w')
        self.entry_password = tk.Entry(self.login_frame).grid(row=1, column=1, sticky="ew")
        

    def submit_data(self):
        pass

    def close_browser(self):
        pass


root = tk.Tk()
app = App(root)
root.mainloop()
