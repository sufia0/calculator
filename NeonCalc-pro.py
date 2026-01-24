import tkinter as tk
from tkinter import font as tkfont
import math

class CyberDeckCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("NeonCalc-pro")
        self.geometry("400x620")
        self.resizable(False, False)
        
        # --- Color Palette (Neon / Cyberpunk) ---
        self.colors = {
            'bg': '#050505',            # Deep Void Black
            'display_bg': '#0a0a0a',    # Slightly lighter black
            'border_default': '#333333',# Dim border
            
            # Text Colors
            'text_result': '#00ff41',   # Matrix Green
            'text_hist': '#008F11',     # Dimmer Green
            'text_header': '#ff0055',   # Cyber Pink
            
            # Button Accents (Neon Wireframes)
            'neon_num': '#00f3ff',      # Cyan for numbers
            'neon_op': '#ff0055',       # Pink for operators
            'neon_act': '#fcee0a',      # Yellow for clear/action
            'neon_eq': '#00ff41',       # Green for equals
            
            'btn_bg': '#000000'         # Button inner color
        }

        self.configure(bg=self.colors['bg'])

        # --- State Management ---
        self.total_expression = ""
        self.current_expression = ""
        
        # --- UI Layout ---
        self._create_header()
        self._create_display_labels()
        self._create_buttons()
        self._bind_keys()

    def _create_header(self):
        """Decorative header for that sci-fi terminal look."""
        header_frame = tk.Frame(self, bg=self.colors['bg'], pady=5)
        header_frame.pack(fill="x", padx=20)
        
        label = tk.Label(
            header_frame, 
            text=":: SYSTEM READY :: STREAM_ACTIVE", 
            fg=self.colors['text_header'], 
            bg=self.colors['bg'],
            font=("Consolas", 8),
            anchor="w"
        )
        label.pack(fill="x")

    def _create_display_labels(self):
        """Creates the dual-line display resembling a terminal output."""
        display_frame = tk.Frame(
            self, 
            bg=self.colors['display_bg'], 
            highlightbackground=self.colors['border_default'], 
            highlightthickness=1
        )
        display_frame.pack(expand=False, fill="both", padx=15, pady=(0, 15))

        # Upper Label: History
        self.lbl_equation = tk.Label(
            display_frame, 
            text="", 
            anchor="e", 
            bg=self.colors['display_bg'], 
            fg=self.colors['text_hist'], 
            padx=15, 
            pady=5,
            font=("Consolas", 12)
        )
        self.lbl_equation.pack(fill="x", pady=(10, 0))

        # Lower Label: Main Result
        self.lbl_result = tk.Label(
            display_frame, 
            text="0", 
            anchor="e", 
            bg=self.colors['display_bg'], 
            fg=self.colors['text_result'], 
            padx=15, 
            pady=10,
            font=("Consolas", 36, "bold")
        )
        self.lbl_result.pack(fill="x")

    def _create_buttons(self):
        """Generates the grid of 'Wireframe' buttons."""
        buttons_frame = tk.Frame(self, bg=self.colors['bg'])
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Configure Grid
        for x in range(4):
            buttons_frame.columnconfigure(x, weight=1)
        for y in range(5):
            buttons_frame.rowconfigure(y, weight=1)

        # Layout: (Text, Row, Col, Type, Command)
        buttons = [
            ("CLR", 0, 0, 'action', self.clear),
            ("(", 0, 1, 'op', lambda: self.append_operator("(")),
            (")", 0, 2, 'op', lambda: self.append_operator(")")),
            ("÷", 0, 3, 'op', lambda: self.append_operator("/")),
            
            ("7", 1, 0, 'num', lambda: self.add_to_expression(7)),
            ("8", 1, 1, 'num', lambda: self.add_to_expression(8)),
            ("9", 1, 2, 'num', lambda: self.add_to_expression(9)),
            ("×", 1, 3, 'op', lambda: self.append_operator("*")),
            
            ("4", 2, 0, 'num', lambda: self.add_to_expression(4)),
            ("5", 2, 1, 'num', lambda: self.add_to_expression(5)),
            ("6", 2, 2, 'num', lambda: self.add_to_expression(6)),
            ("-", 2, 3, 'op', lambda: self.append_operator("-")),
            
            ("1", 3, 0, 'num', lambda: self.add_to_expression(1)),
            ("2", 3, 1, 'num', lambda: self.add_to_expression(2)),
            ("3", 3, 2, 'num', lambda: self.add_to_expression(3)),
            ("+", 3, 3, 'op', lambda: self.append_operator("+")),
            
            (".", 4, 0, 'num', lambda: self.add_to_expression(".")),
            ("0", 4, 1, 'num', lambda: self.add_to_expression(0)),
            ("DEL", 4, 2, 'num', self.backspace),
            ("EXEC", 4, 3, 'equal', self.evaluate)
        ]

        for (text, r, c, btn_type, cmd) in buttons:
            self._create_neon_button(buttons_frame, text, r, c, btn_type, cmd)

    def _create_neon_button(self, parent, text, row, col, btn_type, cmd):
        """
        Creates a button wrapped in a frame to simulate a 'Neon Border'.
        The button fills with color on hover (Hacker style).
        """
        
        # Determine Neon Accent Color
        if btn_type == 'num':
            neon_color = self.colors['neon_num']
        elif btn_type == 'op':
            neon_color = self.colors['neon_op']
        elif btn_type == 'action':
            neon_color = self.colors['neon_act']
        elif btn_type == 'equal':
            neon_color = self.colors['neon_eq']
        
        # 1. The Container Frame (Acts as the border)
        # We give it padding to create the "gap" between buttons
        frame_wrapper = tk.Frame(parent, bg=self.colors['bg'], padx=5, pady=5)
        frame_wrapper.grid(row=row, column=col, sticky="nsew")

        # 2. The Border Frame (The actual colored line)
        border_frame = tk.Frame(frame_wrapper, bg=neon_color, padx=1, pady=1)
        border_frame.pack(expand=True, fill="both")

        # 3. The Button (Black center)
        btn = tk.Button(
            border_frame,
            text=text,
            bg=self.colors['btn_bg'],
            fg=neon_color,
            font=("Consolas", 14, "bold"),
            relief="flat",
            activebackground=neon_color,
            activeforeground=self.colors['btn_bg'],
            command=cmd,
            cursor="hand2"
        )
        btn.pack(expand=True, fill="both")

        # --- Unique Hover Effect: Fill the button with neon light ---
        def on_enter(e):
            btn.config(bg=neon_color, fg=self.colors['btn_bg']) # Invert colors
            
        def on_leave(e):
            btn.config(bg=self.colors['btn_bg'], fg=neon_color) # Revert

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _bind_keys(self):
        """Binds keyboard events."""
        self.bind("<Return>", lambda event: self.evaluate())
        self.bind("<KP_Enter>", lambda event: self.evaluate())
        self.bind("<BackSpace>", lambda event: self.backspace())
        self.bind("<Escape>", lambda event: self.clear())
        
        for char in "0123456789.":
            self.bind(char, lambda event, c=char: self.add_to_expression(c))
        
        operators = {"+": "+", "-": "-", "*": "*", "/": "/"}
        for key, val in operators.items():
            self.bind(key, lambda event, op=val: self.append_operator(op))

    # --- Logic Methods (Identical to previous version) ---

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            expression = self.total_expression
            display_expr = expression.replace('*', '×').replace('/', '÷')
            self.lbl_equation.config(text=display_expr)
            result = str(eval(expression))
            if result.endswith(".0"):
                result = result[:-2]
            self.current_expression = result
            self.total_expression = ""
        except Exception:
            self.current_expression = "ERR:SYNTAX"
            self.total_expression = ""
        self.update_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in [('*', '×'), ('/', '÷')]:
            expression = expression.replace(operator, symbol)
        self.lbl_equation.config(text=expression)

    def update_label(self):
        display_text = self.current_expression[:14]
        if display_text == "":
            display_text = "0"
        self.lbl_result.config(text=display_text)

if __name__ == "__main__":
    app = CyberDeckCalculator()
    app.mainloop()
