import tkinter as tk
from tkinter import ttk
import random
import time

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Number Generator")
        self.root.geometry("400x300")
        
        # Configure root to center its children
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame to center its children
        self.main_frame.grid_rowconfigure(0, weight=3)  
        self.main_frame.grid_rowconfigure(1, weight=1)  
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create number display label
        self.number_label = ttk.Label(
            self.main_frame,
            text="Click to Start",
            font=("Arial", 50),  # Font size for initial text
            anchor="center"
        )
        self.number_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Create button container frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        # Create generate button with fixed width
        self.generate_button = ttk.Button(
            self.button_frame,
            text="Generate",
            command=self.generate_number,
            width=15  #  button width 
        )
        self.generate_button.grid(row=0, column=0, pady=20)
        
        # Initialize variables
        self.is_animating = False
        self.animation_count = 0
        self.final_number = None
        
    def generate_number(self):
        if not self.is_animating:
            self.is_animating = True
            self.animation_count = 0
            self.final_number = random.randint(1, 99)
            self.animate_number()
            
    def animate_number(self):
        if self.is_animating:
            if self.animation_count < 30:  # Animation lasts for 30 changes
                random_num = random.randint(1, 99)
                self.number_label.config(
                    text=str(random_num),
                    font=("Arial", 72)  # numbers font
                )
                
                self.animation_count += 1
                self.root.after(60, self.animate_number)  # Update every 60ms
            else:
                # Display final result
                self.number_label.config(
                    text=str(self.final_number),
                    font=("Arial", 72)  # final number font
                )
                self.is_animating = False

def main():
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
