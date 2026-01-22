import tkinter as tk
from tkinter import font
import math

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, color, hover_color, command, text, text_color, font):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.font = font
        self.corner_radius = corner_radius

        # Bind events
        self.bind("<Button-1>", self._on_press)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._draw)

    def _draw(self, event=None):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Skip drawing if too small
        if width < 5 or height < 5: return
        
        r = self.corner_radius
        # Dynamic radius adjustment if button is small
        if r * 2 > width: r = width // 2
        if r * 2 > height: r = height // 2

        # Draw rounded rectangle (4 arcs + 2 rectangles)
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=self.color, outline="", tags="shape")
        self.create_arc(width-2*r, 0, width, 2*r, start=0, extent=90, fill=self.color, outline="", tags="shape")
        self.create_arc(width-2*r, height-2*r, width, height, start=270, extent=90, fill=self.color, outline="", tags="shape")
        self.create_arc(0, height-2*r, 2*r, height, start=180, extent=90, fill=self.color, outline="", tags="shape")
        
        self.create_rectangle(r, 0, width-r, height, fill=self.color, outline="", tags="shape")
        self.create_rectangle(0, r, width, height-r, fill=self.color, outline="", tags="shape")
        
        # Draw centered text
        self.create_text(width/2, height/2, text=self.text, fill=self.text_color, font=self.font, tags="text")
        
        # Ensure clicks on shape/text trigger command
        self.tag_bind("shape", "<Button-1>", self._on_press)
        self.tag_bind("text", "<Button-1>", self._on_press)

    def _on_hover(self, event):
        self.itemconfig("shape", fill=self.hover_color)

    def _on_leave(self, event):
        self.itemconfig("shape", fill=self.color)

    def _on_press(self, event):
        if self.command:
            self.command()

class BlueCalculator:
    # --- Design System (Bold Neon Theme) ---
    COLORS = {
        'bg_main': '#020617',       # Ultra Dark Blue
        'display_bg': '#0f172a',    # Deep Slate
        'text_main': '#e2e8f0',     # Off-White
        'text_sec': '#64748b',      # Muted Slate
        'btn_num': '#1e293b',       # Slate 800
        'btn_op': '#3b82f6',        # Blue 500
        'btn_sci': '#334155',       # Slate 700
        'btn_eq': '#06b6d4',        # Cyan 500
        'btn_clear': '#f43f5e',     # Rose 500
        'hover_num': '#334155',     # Slate 700
        'hover_op': '#2563eb',      # Blue 600
        'hover_sci': '#475569',
        'hover_eq': '#0891b2',      # Cyan 600
        'hover_clear': '#e11d48'    # Rose 600
    }

    def __init__(self, root):
        self.root = root
        self.root.title("NeonCalc Pro")
        self.root.geometry("420x750") # Taller, wider for bold look
        self.root.configure(bg=self.COLORS['bg_main'])
        self.root.resizable(True, True)

        self.expression = ""
        self.input_text = tk.StringVar()
        self.history = []
        self.show_sci = False  # Toggle state for scientific keys

        self._setup_fonts()
        self._build_layout()
        self._bind_keys()

    def _setup_fonts(self):
        self.f_display = font.Font(family="Arial", size=40, weight="bold")
        self.f_btn = font.Font(family="Arial", size=18, weight="bold")
        self.f_small = font.Font(family="Arial", size=12, weight="bold")

    def _build_layout(self):
        # 1. Display Area (Result + History Preview)
        display_frame = tk.Frame(self.root, bg=self.COLORS['bg_main'], pady=30, padx=20)
        display_frame.pack(fill="x")

        # History Label (Small text above main display)
        self.lbl_history = tk.Label(
            display_frame, text="", 
            font=self.f_small, bg=self.COLORS['bg_main'], fg=self.COLORS['text_sec'], anchor="e"
        )
        self.lbl_history.pack(fill="x")

        # Main Entry
        self.entry = tk.Entry(
            display_frame, textvariable=self.input_text, font=self.f_display,
            bg=self.COLORS['bg_main'], fg=self.COLORS['text_main'],
            bd=0, justify="right", insertbackground=self.COLORS['text_main']
        )
        self.entry.pack(fill="x", pady=(10, 0))
        # Disable typing directly to force validation via buttons/bindings
        self.entry.bind("<Key>", lambda e: "break")

        # 2. Controls Bar (History Toggle / Sci Mode)
        ctrl_frame = tk.Frame(self.root, bg=self.COLORS['bg_main'])
        ctrl_frame.pack(fill="x", padx=15, pady=5)
        
        self.btn_sci_toggle = tk.Button(
            ctrl_frame, text="SHOW SCI ⚗️", bg=self.COLORS['bg_main'], fg=self.COLORS['btn_op'],
            font=self.f_small, bd=0, cursor="hand2", activebackground=self.COLORS['bg_main'],
            command=self._toggle_scientific
        )
        self.btn_sci_toggle.pack(side="right")

        # 3. Keypad Area
        self.keypad = tk.Frame(self.root, bg=self.COLORS['bg_main'], padx=15, pady=15)
        self.keypad.pack(expand=True, fill="both")

        self._render_standard_keypad()

    def _render_standard_keypad(self):
        # Clear existing buttons if switching modes
        for widget in self.keypad.winfo_children():
            widget.destroy()

        # Layout Configuration
        # Row 0: Clear & Mods
        btns = [
            ('C', 0, 0, 'clear'), ('⌫', 0, 1, 'clear'), ('%', 0, 2, 'sci'), ('÷', 0, 3, 'op'),
            ('7', 1, 0, 'num'),   ('8', 1, 1, 'num'),   ('9', 1, 2, 'num'), ('×', 1, 3, 'op'),
            ('4', 2, 0, 'num'),   ('5', 2, 1, 'num'),   ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
            ('1', 3, 0, 'num'),   ('2', 3, 1, 'num'),   ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
            ('0', 4, 0, 'num', 2),('.', 4, 2, 'num'),   ('=', 4, 3, 'eq')
        ]

        # Grid weights
        for i in range(5): self.keypad.rowconfigure(i, weight=1)
        for i in range(4): self.keypad.columnconfigure(i, weight=1)

        for item in btns:
            text = item[0]
            r, c = item[1], item[2]
            tag = item[3]
            colspan = item[4] if len(item) > 4 else 1
            self._create_btn(text, r, c, tag, colspan)

    def _render_scientific_keypad(self):
        # Scientific layout extends grid
        for widget in self.keypad.winfo_children():
            widget.destroy()

        btns = [
            ('sin', 0, 0, 'sci'), ('cos', 0, 1, 'sci'), ('tan', 0, 2, 'sci'), ('C', 0, 3, 'clear'), ('⌫', 0, 4, 'clear'),
            ('ln', 1, 0, 'sci'),  ('log', 1, 1, 'sci'), ('√', 1, 2, 'sci'),   ('(', 1, 3, 'sci'),   (')', 1, 4, 'sci'),
            ('^', 2, 0, 'sci'),   ('7', 2, 1, 'num'),   ('8', 2, 2, 'num'),   ('9', 2, 3, 'num'),   ('÷', 2, 4, 'op'),
            ('π', 3, 0, 'sci'),   ('4', 3, 1, 'num'),   ('5', 3, 2, 'num'),   ('6', 3, 3, 'num'),   ('×', 3, 4, 'op'),
            ('e', 4, 0, 'sci'),   ('1', 4, 1, 'num'),   ('2', 4, 2, 'num'),   ('3', 4, 3, 'num'),   ('-', 4, 4, 'op'),
            ('mod', 5, 0, 'sci'), ('0', 5, 1, 'num'),   ('.', 5, 2, 'num'),   ('=', 5, 3, 'eq'),    ('+', 5, 4, 'op')
        ]

        for i in range(6): self.keypad.rowconfigure(i, weight=1)
        for i in range(5): self.keypad.columnconfigure(i, weight=1)

        for item in btns:
            text = item[0]
            r, c = item[1], item[2]
            tag = item[3]
            colspan = item[4] if len(item) > 4 else 1
            self._create_btn(text, r, c, tag, colspan)

    def _create_btn(self, text, row, col, tag, colspan=1):
        # Color mapping
        bg_color = self.COLORS.get(f'btn_{tag}', self.COLORS['btn_num'])
        fg_color = self.COLORS['text_main']
        
        # Determine specific styling based on type
        hover_bg = self.COLORS.get(f'hover_{tag}', self.COLORS['hover_num'])
        
        if tag == 'eq':
            bg_color = self.COLORS['btn_eq']
            fg_color = '#ffffff'
            hover_bg = self.COLORS.get('hover_eq', '#0891b2')
        elif tag == 'clear':
            bg_color = self.COLORS['btn_clear']
            fg_color = '#ffffff'
            hover_bg = self.COLORS.get('hover_clear', '#e11d48')

        # Use the custom RoundedButton instead of standard tk.Button
        btn = RoundedButton(
            self.keypad, 
            width=1, height=1, # Initial size, grid resizes it
            corner_radius=25,  # High radius for rounded look
            color=bg_color, 
            hover_color=hover_bg,
            command=lambda: self._on_click(text),
            text=text, 
            text_color=fg_color, 
            font=self.f_btn
        )

        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

    def _toggle_scientific(self):
        self.show_sci = not self.show_sci
        if self.show_sci:
            self.btn_sci_toggle.config(text="HIDE SCI 🧪")
            self.root.geometry("600x750")
            self._render_scientific_keypad()
        else:
            self.btn_sci_toggle.config(text="SHOW SCI ⚗️")
            self.root.geometry("420x750")
            self._render_standard_keypad()

    def _bind_keys(self):
        self.root.bind('<Return>', lambda e: self._on_click('='))
        self.root.bind('<BackSpace>', lambda e: self._on_click('⌫'))
        self.root.bind('<Escape>', lambda e: self._on_click('C'))
        for key in '1234567890.+-*/%()^':
            self.root.bind(key, lambda e, k=key: self._on_click(self._map_key(k)))

    def _map_key(self, key):
        mapping = {'*': '×', '/': '÷'}
        return mapping.get(key, key)

    def _on_click(self, char):
        if char == 'C':
            self.expression = ""
            self.lbl_history.config(text="")
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '=':
            self._calculate()
            return
        elif char in ['sin', 'cos', 'tan', 'ln', 'log', '√']:
            self.expression += f"{char}("
        else:
            if self.input_text.get() == "Error": self.expression = ""
            self.expression += char
        
        self.input_text.set(self.expression)

    def _calculate(self):
        try:
            # Map UI symbols to math functions
            expr = self.expression
            expr = expr.replace('×', '*').replace('÷', '/')
            expr = expr.replace('^', '**').replace('√', 'math.sqrt')
            expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
            expr = expr.replace('ln', 'math.log').replace('log', 'math.log10')
            expr = expr.replace('π', 'math.pi').replace('e', 'math.e')

            # Evaluate
            result = eval(expr)
            
            # Format Result
            if isinstance(result, float):
                if result.is_integer():
                    res_str = str(int(result))
                else:
                    res_str = f"{result:.8f}".rstrip("0").rstrip(".")
            else:
                res_str = str(result)

            # Update History Label
            self.lbl_history.config(text=f"{self.expression} = ")
            
            self.expression = res_str
            self.input_text.set(res_str)

        except Exception:
            self.input_text.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueCalculator(root)
    root.mainloop()