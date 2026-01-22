import tkinter as tk
from tkinter import messagebox
import math

# Kept the exact same structure and logic, only changed colors and fonts.
class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("320x520") # Slightly taller for modern spacing
        
        # --- NEW MODERN COLOR PALETTE ---
        self.colors = {
            'window_bg': '#101010',   # Deep soft black background
            'gap_color': '#000000',   # Pure black for sharp lines between tiles
            'display_text': '#FFFFFF',
            
            # Button Colors
            'btn_num': '#2d3436',     # Clean dark grey for numbers
            # THE REQUESTED GREEN COLORS:
            'btn_op': '#00b894',      # Vibrant Modern Mint Green for operators
            'btn_eq': '#00b894',      # Matches operators
            
            'btn_sci': '#222f3e',     # Darker blue-grey for scientific panel to recede visually
            'btn_top': '#636e72',     # sophisticated medium grey for C/DEL
            'text_white': '#FFFFFF'   # Standard white text
        }
        
        self.root.configure(bg=self.colors['window_bg'])

        self.is_expanded = False
        self.expression = ""
        self.input_text = tk.StringVar()

        # --- MAIN CONTAINER ---
        main_frame = tk.Frame(root, bg=self.colors['window_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Top Control (Sci Toggle)
        self.control_frame = tk.Frame(main_frame, bg=self.colors['window_bg'])
        self.control_frame.pack(side=tk.TOP, fill=tk.X, pady=(10,0), padx=10)
        
        # Updated toggle button style to match new theme
        self.toggle_btn = tk.Button(self.control_frame, text="◫ Scientific", 
                                    font=('Segoe UI Semibold', 10), 
                                    bg=self.colors['btn_sci'], fg=self.colors['text_white'],
                                    bd=0, highlightthickness=0, activebackground="#34495e", activeforeground="white",
                                    cursor="hand2", command=self.toggle_scientific)
        self.toggle_btn.pack(side=tk.LEFT)

        # 2. Display Area
        self.display_frame = tk.Frame(main_frame, bg=self.colors['window_bg'])
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=(20, 20))
        
        # Increased font size and weight for modern look
        entry = tk.Entry(self.display_frame, textvariable=self.input_text, 
                         font=('Segoe UI Semibold', 44), bg=self.colors['window_bg'], 
                         fg=self.colors['display_text'], bd=0, highlightthickness=0, justify=tk.RIGHT)
        entry.pack(fill=tk.BOTH, padx=15)

        # 3. Buttons Area Container (Uses gap color for background lines)
        self.buttons_container = tk.Frame(main_frame, bg=self.colors['gap_color'])
        self.buttons_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scientific Frame (Hidden by default)
        self.sci_frame = tk.Frame(self.buttons_container, bg=self.colors['gap_color'])
        
        # Standard Frame (Always visible)
        self.std_frame = tk.Frame(self.buttons_container, bg=self.colors['gap_color'])
        self.std_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_standard_buttons()
        self.create_scientific_buttons()

    def create_standard_buttons(self):
        buttons = [
            ["C", "DEL", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for i in range(5): self.std_frame.rowconfigure(i, weight=1)
        for i in range(4): self.std_frame.columnconfigure(i, weight=1)

        for r, row in enumerate(buttons):
            current_col = 0
            for char in row:
                colspan = 2 if char == "0" else 1
                
                # --- NEW COLOR ASSIGNMENT LOGIC ---
                bg_color = self.colors['btn_num'] # Default number color
                
                if char in ["/", "*", "-", "+", "="]:
                    bg_color = self.colors['btn_op'] # The new Green
                elif char in ["C", "DEL", "%"]:
                    bg_color = self.colors['btn_top'] # The new Darker Top Grey

                # Updated Font to Semibold for bolder look
                btn = tk.Button(self.std_frame, text=char, font=('Segoe UI Semibold', 20), 
                                bg=bg_color, fg=self.colors['text_white'], 
                                bd=0, highlightthickness=0,
                                activebackground="#ffffff", activeforeground=self.colors['gap_color'],
                                command=lambda t=char: self.on_click(t))
                
                btn.grid(row=r, column=current_col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
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
                # Updated font and color
                btn = tk.Button(self.sci_frame, text=char, font=('Segoe UI', 13), 
                                bg=self.colors['btn_sci'], fg=self.colors['text_white'], 
                                bd=0, highlightthickness=0,
                                activebackground="#444", activeforeground="white",
                                command=lambda t=char: self.on_click(t))
                btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

    # --- LOGIC REMAINS UNTOUCHED BELOW THIS LINE ---

    def toggle_scientific(self):
        if not self.is_expanded:
            self.root.geometry("550x520") 
            self.sci_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.toggle_btn.config(text="❮ Standard")
            self.is_expanded = True
        else:
            self.sci_frame.pack_forget()
            self.root.geometry("320x520")
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
