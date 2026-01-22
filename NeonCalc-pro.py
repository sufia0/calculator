import tkinter as tk
from tkinter import messagebox
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("NeonCalc-pro")
        self.root.geometry("320x500") 
        self.root.configure(bg="#000000") # Pure black background

        self.is_expanded = False
        self.expression = ""
        self.input_text = tk.StringVar()

        # --- MODERN FLAT COLOR PALETTE ---
        self.colors = {
            'bg': '#000000',        # Gap color (Black)
            'display_bg': '#000000',
            'text': '#FFFFFF',
            'btn_num': '#1c1c1c',   # Dark Grey (Numbers)
            'btn_op': '#ff9f0a',    # Modern Orange (Operators)
            'btn_sci': '#2c2c2c',   # Slightly lighter grey (Sci)
            'btn_top': '#a5a5a5',   # Light Grey (Top row like C, DEL)
            'text_dark': '#000000'  # Text color for light buttons
        }

        # --- MAIN CONTAINER ---
        main_frame = tk.Frame(root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Top Control (Sci Toggle)
        self.control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        self.control_frame.pack(side=tk.TOP, fill=tk.X, pady=(5,0), padx=5)
        
        self.toggle_btn = tk.Button(self.control_frame, text="◫ Scientific", 
                                    font=('Arial', 10, 'bold'), bg=self.colors['btn_num'], fg="white",
                                    bd=0, highlightthickness=0, activebackground="#333333", activeforeground="white",
                                    cursor="hand2", command=self.toggle_scientific)
        self.toggle_btn.pack(side=tk.LEFT)

        # 2. Display Area
        self.display_frame = tk.Frame(main_frame, bg=self.colors['display_bg'])
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=(20, 10))
        
        entry = tk.Entry(self.display_frame, textvariable=self.input_text, 
                         font=('Segoe UI', 40), bg=self.colors['display_bg'], 
                         fg=self.colors['text'], bd=0, highlightthickness=0, justify=tk.RIGHT)
        entry.pack(fill=tk.BOTH, padx=15)

        # 3. Buttons Area
        self.buttons_container = tk.Frame(main_frame, bg=self.colors['bg'])
        self.buttons_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Scientific Frame (Hidden by default)
        self.sci_frame = tk.Frame(self.buttons_container, bg=self.colors['bg'])
        
        # Standard Frame (Always visible)
        self.std_frame = tk.Frame(self.buttons_container, bg=self.colors['bg'])
        self.std_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_standard_buttons()
        self.create_scientific_buttons()

    def create_standard_buttons(self):
        # We define rows as lists of keys
        buttons = [
            ["C", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]  # 0 will span 2 columns
        ]

        # Grid weights to make buttons resize nicely
        for i in range(5): self.std_frame.rowconfigure(i, weight=1)
        for i in range(4): self.std_frame.columnconfigure(i, weight=1)

        for r, row in enumerate(buttons):
            # We use this counter to track which column we are currently in
            current_col = 0
            
            for char in row:
                # Determine how wide the button should be
                colspan = 2 if char == "0" else 1
                
                # Color & Style Selection
                bg_color = self.colors['btn_num']
                fg_color = "white"
                
                if char in ["/", "*", "-", "+", "="]:
                    bg_color = self.colors['btn_op']
                    fg_color = "white"
                elif char in ["C", "DEL", "%"]:
                    bg_color = self.colors['btn_top']
                    fg_color = "black" # Black text on light grey button

                btn = tk.Button(self.std_frame, text=char, font=('Segoe UI', 18), 
                                bg=bg_color, fg=fg_color, 
                                bd=0, highlightthickness=0, # No Outline
                                activebackground="white", activeforeground="black",
                                command=lambda t=char: self.on_click(t))
                
                # We grid using 'current_col' instead of the loop index
                btn.grid(row=r, column=current_col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
                
                # Move the column counter forward
                # If it was "0", we move 2 steps. Otherwise 1 step.
                current_col += colspan

    def create_scientific_buttons(self):
        sci_buttons = [
            ("sin", "cos", "tan"),
            ("ln", "log", "sqrt"),
            ("pi", "e", "^"),
            ("(", ")", "deg")
        ]

        for i in range(4): self.sci_frame.rowconfigure(i, weight=1)
        for i in range(3): self.sci_frame.columnconfigure(i, weight=1)

        for r, row in enumerate(sci_buttons):
            for c, char in enumerate(row):
                btn = tk.Button(self.sci_frame, text=char, font=('Segoe UI', 12), 
                                bg=self.colors['btn_sci'], fg="white", 
                                bd=0, highlightthickness=0,
                                activebackground="#444", activeforeground="white",
                                command=lambda t=char: self.on_click(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

    def toggle_scientific(self):
        if not self.is_expanded:
            self.root.geometry("550x500") 
            self.sci_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.toggle_btn.config(text="❮ Standard")
            self.is_expanded = True
        else:
            self.sci_frame.pack_forget()
            self.root.geometry("320x500")
            self.toggle_btn.config(text="◫ Scientific")
            self.is_expanded = False

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.input_text.set("")
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.input_text.set(self.expression)
        elif char == "=":
            try:
                if self.expression.count('(') > self.expression.count(')'):
                    self.expression += ')' * (self.expression.count('(') - self.expression.count(')'))

                calc_context = {
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
                    "pi": math.pi, "e": math.e
                }

                eval_expr = self.expression.replace("^", "**").replace("%", "/100")
                value = eval(eval_expr, {"__builtins__": None}, calc_context)
                
                value = round(value, 10)
                result = str(int(value)) if value == int(value) else str(value)
                
                self.input_text.set(result)
                self.expression = result
            except Exception:
                self.input_text.set("Error")
                self.expression = ""
        else:
            if char in ["sin", "cos", "tan", "sqrt", "log", "ln"]:
                self.expression += char + "("
            else:
                self.expression += str(char)
            self.input_text.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
