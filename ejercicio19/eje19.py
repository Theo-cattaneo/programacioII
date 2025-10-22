import tkinter as tk
from tkinter import ttk, messagebox

class CesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cifrado César")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Configuración de colores
        self.bg_color = "#f0f4f8"
        self.button_bg = "#4a6fa5"
        self.button_fg = "white"
        self.entry_bg = "#ffffff"
        self.result_bg = "#eef2f7"
        
        self.root.configure(bg=self.bg_color)
        
        # Crear estilo para widgets
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", font=("Arial", 10), background=self.bg_color)
        self.style.configure("TEntry", font=("Arial", 10))
        
        # Crear componentes
        self.create_widgets()
        
    def create_widgets(self):
        # Título principal
        title_label = tk.Label(
            self.root,
            text="Cifrado César",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#2c3e50"
        )
        title_label.pack(pady=(20, 10))
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Entrada de mensaje
        msg_frame = tk.Frame(main_frame, bg=self.bg_color)
        msg_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            msg_frame,
            text="Mensaje:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        ).pack(anchor="w")
        
        self.msg_entry = tk.Text(
            msg_frame,
            height=4,
            width=50,
            wrap="word",
            font=("Arial", 10),
            bg=self.entry_bg,
            padx=10,
            pady=5,
            relief="solid",
            borderwidth=1
        )
        self.msg_entry.pack(fill="x")
        
        # Entrada de desplazamiento
        shift_frame = tk.Frame(main_frame, bg=self.bg_color)
        shift_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            shift_frame,
            text="Desplazamiento:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        ).pack(anchor="w")
        
        self.shift_entry = ttk.Entry(
            shift_frame,
            font=("Arial", 10),
            width=15
        )
        self.shift_entry.pack(anchor="w", pady=(5, 0))
        
        # Botones
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=15)
        
        self.cipher_button = tk.Button(
            button_frame,
            text="Cifrar",
            command=self.cipher_message,
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        self.cipher_button.pack(side="left", padx=10)
        
        self.decipher_button = tk.Button(
            button_frame,
            text="Descifrar",
            command=self.decipher_message,
            bg="#5a7fb5",
            fg=self.button_fg,
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        self.decipher_button.pack(side="left", padx=10)
        
        # Área de resultado
        result_frame = tk.Frame(main_frame, bg=self.bg_color)
        result_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(
            result_frame,
            text="Resultado:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        ).pack(anchor="w")
        
        self.result_text = tk.Text(
            result_frame,
            height=6,
            width=50,
            wrap="word",
            font=("Arial", 10),
            bg=self.result_bg,
            padx=10,
            pady=5,
            relief="solid",
            borderwidth=1,
            state="disabled"
        )
        self.result_text.pack(fill="both", expand=True)
        
        # Instrucciones
        instructions = tk.Label(
            self.root,
            text="Usa desplazamiento positivo para cifrar, negativo para descifrar",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg="#7f8c8d"
        )
        instructions.pack(pady=(10, 20))
        
    def cipher_message(self):
        self.process_cipher(encrypt=True)
        
    def decipher_message(self):
        self.process_cipher(encrypt=False)
        
    def process_cipher(self, encrypt=True):
        message = self.msg_entry.get("1.0", "end-1c").strip()
        
        if not message:
            messagebox.showwarning("Advertencia", "Por favor ingresa un mensaje")
            return
            
        try:
            shift = int(self.shift_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El desplazamiento debe ser un número entero")
            return
            
        # Procesar el mensaje
        result = ""
        for char in message:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                offset = (ord(char) - base + shift) % 26
                result += chr(base + offset)
            else:
                result += char
                
        # Mostrar resultado
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)
        self.result_text.config(state="disabled")
        
        # Animación de botón
        button = self.cipher_button if encrypt else self.decipher_button
        button.config(relief="sunken")
        self.root.after(100, lambda: button.config(relief="flat"))

if __name__ == "__main__":
    root = tk.Tk()
    app = CesarCipherApp(root)
    root.mainloop()