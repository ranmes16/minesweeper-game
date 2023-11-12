import tkinter as tk

class CustomButton(tk.Button):
    def __init__(self, master, is_bomb, **kwargs):
        super().__init__(master, **kwargs)
        self.is_bomb = is_bomb
        self.bombs_around = 0
        self.is_disabled = False
        self.is_flagged = False
