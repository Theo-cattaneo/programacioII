import tkinter as tk
import random
import requests
from PIL import Image, ImageTk

class VisualTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabajo de Seguimiento Visual")
        
        # --- Configuración de la Ventana ---
        self.root.state('zoomed')
        
        # --- NUEVA PALETA DE COLORES MODERNA ---
        self.BG_COLOR = '#0a0e27'          # Azul muy oscuro para el fondo
        self.FRAME_COLOR = '#151932'      # Azul un poco más claro para marcos
        self.TEXT_COLOR = '#e0e0e0'        # Blanco suave para el texto
        self.ACCENT_COLOR = '#00ffff'      # Cian brillante para acentos
        self.BUTTON_COLOR = '#1e90ff'      # Azul "Dodger Blue" para botones
        self.BUTTON_HOVER_COLOR = '#4169e1' # Azul "Royal Blue" para hover

        self.root.configure(bg=self.BG_COLOR)

        # --- Variables de Control ---
        self.flash_size = 50
        self.flash_speed = 5
        self.animation_delay_ms = 20
        self.animation_duration = 25
        
        self.color_map = {
            'Azul': '#4169e1',       # Azul consistente con el tema
            'Verde': '#32cd32',      # Verde lima brillante
            'Blanco': '#f0f8ff',     # Blanco aliceblue (suave)
            'Violeta': '#9370db',    # Violeta medio púrpura
            'Rojo': '#dc143c'        # Rojo carmín intenso
        }
        self.flash_color = self.color_map['Azul']
        
        self.is_animating = False
        self.time_left = self.animation_duration
        self.timer_job = None
        self.menu_image = None

        # --- Fuente Moderna ---
        try:
            self.default_font = ("Segoe UI", 12)
            self.title_font = ("Segoe UI", 40, "bold")
            self.button_font = ("Segoe UI", 16, "bold")
        except tk.TclError:
            self.default_font = ("Helvetica", 12)
            self.title_font = ("Helvetica", 40, "bold")
            self.button_font = ("Helvetica", 16, "bold")

        self.load_menu_image()
        self.create_menu()

    def load_menu_image(self):
        """Carga una imagen temática de óptica y programación."""
        # URL de una imagen de un ojo con estilo tecnológico
        image_url = "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        image_filename = "tech_eye_image.png"
        
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(image_filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            pil_image = Image.open(image_filename)
            # Redimensionar a un ancho máximo de 300 píxeles
            pil_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Crear un borde alrededor de la imagen
            border = Image.new('RGB', (pil_image.width + 10, pil_image.height + 10), self.ACCENT_COLOR)
            border.paste(pil_image, (5, 5))
            
            self.menu_image = ImageTk.PhotoImage(border)

        except Exception as e:
            print(f"No se pudo cargar la imagen. Error: {e}")
            self.menu_image = None

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.menu_frame,
            text="Trabajo de Seguimiento Visual",
            font=self.title_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=(80, 40))

        instruction_label = tk.Label(
            self.menu_frame,
            text="Elige un color para el destello:",
            font=self.default_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        instruction_label.pack(pady=20)

        button_frame = tk.Frame(self.menu_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=20)

        for color_name in self.color_map.keys():
            btn = tk.Button(
                button_frame,
                text=color_name,
                font=self.button_font,
                bg=self.BUTTON_COLOR,
                fg='white',
                width=18,
                relief=tk.RAISED,
                bd=2,
                cursor="hand2", # Cursor de mano al pasar el mouse
                activebackground=self.BUTTON_HOVER_COLOR,
                command=lambda c=color_name: self.start_animation(c)
            )
            btn.pack(pady=8)

        if self.menu_image:
            image_label = tk.Label(
                self.menu_frame, 
                image=self.menu_image, 
                bg=self.BG_COLOR
            )
            image_label.pack(pady=40)

    def start_animation(self, chosen_color_name):
        self.menu_frame.pack_forget()
        self.flash_color = self.color_map[chosen_color_name]

        self.animation_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.animation_frame.pack(fill=tk.BOTH, expand=True)

        self.timer_label = tk.Label(
            self.animation_frame,
            text=f"Tiempo: {self.time_left}",
            font=self.default_font,
            fg=self.ACCENT_COLOR,
            bg=self.BG_COLOR
        )
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.animation_frame, 
            bg=self.FRAME_COLOR, # Usar el color de marco para el canvas
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.is_animating = True
        self.time_left = self.animation_duration
        self.update_timer()
        self.root.after(100, self.setup_and_start_flash)

    def update_timer(self):
        if self.time_left > 0 and self.is_animating:
            self.time_left -= 1
            self.timer_label.config(text=f"Tiempo: {self.time_left}")
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.end_animation()

    def setup_and_start_flash(self):
        if not self.is_animating:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x = random.randint(self.flash_size, canvas_width - self.flash_size)
        y = random.randint(self.flash_size, canvas_height - self.flash_size)

        self.flash_item = self.canvas.create_oval(
            x - self.flash_size, y - self.flash_size,
            x + self.flash_size, y + self.flash_size,
            fill=self.flash_color,
            outline=self.ACCENT_COLOR, # Contorno con color de acento
            width=2
        )

        self.vx = random.uniform(-self.flash_speed, self.flash_speed)
        self.vy = random.uniform(-self.flash_speed, self.flash_speed)
        
        if abs(self.vx) < 1: self.vx = 1 if self.vx > 0 else -1
        if abs(self.vy) < 1: self.vy = 1 if self.vy > 0 else -1

        self.move_flash()

    def move_flash(self):
        if not self.is_animating:
            return
            
        coords = self.canvas.coords(self.flash_item)
        if not coords: return
        
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if cx <= self.flash_size or cx >= canvas_width - self.flash_size:
            self.vx = -self.vx

        if cy <= self.flash_size or cy >= canvas_height - self.flash_size:
            self.vy = -self.vy

        self.canvas.move(self.flash_item, self.vx, self.vy)

        self.root.after(self.animation_delay_ms, self.move_flash)

    def end_animation(self):
        self.is_animating = False
        
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        self.timer_label.pack_forget()
        
        if hasattr(self, 'flash_item'):
            self.canvas.delete(self.flash_item)
            
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Seguimiento Visual Terminado",
            fill=self.ACCENT_COLOR,
            font=self.title_font
        )

# --- Ejecución del Programa ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = VisualTrackingApp(main_root)
    main_root.mainloop()