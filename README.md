# 📟 NeonCalc-pro

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> *:: SYSTEM READY :: STREAM_ACTIVE*

**NeonCalc-pro** is a fully functional, high-fidelity arithmetic interface built with Python and Tkinter. Designed for high-contrast visibility and a retro-futuristic aesthetic, it mimics the interface of a sci-fi terminal or cyberdeck.

---

## 📸 Interface Visualization

![CyberDeck Screenshot](https://github.com/user-attachments/assets/96997473-c745-4716-a609-1f571fce08d1)

---

## ⚡ System Capabilities (Features)

* **Neon Wireframe Aesthetic:** Custom-drawn styling using nested frames to create neon borders that glow against a void-black background.
* **Reactive UX:** Buttons feature a "hacker-style" hover effect, instantly filling with neon light (Cyan, Pink, Yellow, or Green) upon interaction.
* **Dual-Line Display:**
    * **History Line:** Shows the current equation string in dim green.
    * **Result Line:** Shows the active input or calculated result in high-vis matrix green.
* **Full Keyboard Support:** operate the deck entirely via Numpad or standard keyboard keys.
* **Error Handling:** Graces syntax errors with a standard `ERR:SYNTAX` message rather than crashing.

---

## 🛠️ Deployment (Installation)

No external dependencies are required. This calculator runs on the standard Python library.

### Prerequisites
* Python 3.x installed.
* Tkinter (Usually included with Python).

*Note for Linux users: If you are on a minimal install, you may need to run `sudo apt-get install python3-tk`.*

### Running the Deck
1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/calculator.git](https://github.com/YOUR_USERNAME/calculator.git)
    ```
2.  Navigate to the directory:
    ```bash
    cd calculator
    ```
3.  Execute the mainframe:
    ```bash
    python main.py
    ```

---

## ⌨️ Controls

| Input | Action |
| :--- | :--- |
| **0-9** | Enter Numbers |
| **+, -, *, /** | Operators |
| **Enter / Return** | Calculate Result (=) |
| **Backspace** | Delete last character (DEL) |
| **Esc** | Clear All (CLR) |

---

## 🎨 Customization

The color palette is centralized in the `__init__` method. You can easily modify the hex codes to change the theme from **Cyberpunk** to **Synthwave** or **Monochrome**.

Look for the `self.colors` dictionary in the code:

```python
self.colors = {
    'bg': '#050505',            # Background
    'text_result': '#00ff41',   # Matrix Green
    'neon_op': '#ff0055',       # Operator Pink
    ...
}
