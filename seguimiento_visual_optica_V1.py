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
        self.root.configure(bg='black')

        # --- Variables de Control ---
        self.flash_size = 50
        self.flash_speed = 5
        self.animation_delay_ms = 20
        self.animation_duration = 25  # Duración en segundos
        
        # --- Diccionario de Colores Actualizado ---
        self.color_map = {
            'Azul': 'blue',
            'Verde': 'lime',        # Cambiado a un verde más claro
            'Blanco': 'white',
            'Violeta': 'purple',    # Cambiado a un morado más oscuro
            'Rojo': 'firebrick'     # Cambiado a un rojo más intenso
        }
        self.flash_color = 'blue'
        
        # Variables para la animación y el temporizador
        self.is_animating = False
        self.time_left = self.animation_duration
        self.timer_job = None
        
        self.menu_image = None

        self.load_menu_image()
        self.create_menu()

    def load_menu_image(self):
        image_url = "https://www.pngegg.com/pngimages/918/918/png-egg-visual-perception-brain-optical-illusion-eye-thumbnail.png"
        image_filename = "visual_tracking_image.png"
        
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(image_filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            pil_image = Image.open(image_filename)
            pil_image.thumbnail((250, 250), Image.Resampling.LANCZOS)
            self.menu_image = ImageTk.PhotoImage(pil_image)

        except Exception as e:
            print(f"No se pudo cargar la imagen. Error: {e}")
            self.menu_image = None

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, bg='black')
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.menu_frame,
            text="Trabajo de Seguimiento Visual",
            font=('Helvetica', 36, 'bold'),
            fg='white',
            bg='black'
        )
        title_label.pack(pady=100)

        instruction_label = tk.Label(
            self.menu_frame,
            text="Elige un color para el destello:",
            font=('Helvetica', 18),
            fg='lightgray',
            bg='black'
        )
        instruction_label.pack(pady=20)

        button_frame = tk.Frame(self.menu_frame, bg='black')
        button_frame.pack(pady=30)

        for color_name in self.color_map.keys():
            btn = tk.Button(
                button_frame,
                text=color_name,
                font=('Helvetica', 16, 'bold'),
                bg='#333333',
                fg='white',
                width=25,
                relief=tk.FLAT,
                command=lambda c=color_name: self.start_animation(c)
            )
            btn.pack(pady=10)

        if self.menu_image:
            image_label = tk.Label(
                self.menu_frame, 
                image=self.menu_image, 
                bg='black'
            )
            image_label.pack(pady=20)

    def start_animation(self, chosen_color_name):
        self.menu_frame.pack_forget()
        self.flash_color = self.color_map[chosen_color_name]

        self.animation_frame = tk.Frame(self.root, bg='black')
        self.animation_frame.pack(fill=tk.BOTH, expand=True)

        # --- Contador de tiempo visible ---
        self.timer_label = tk.Label(
            self.animation_frame,
            text=f"Tiempo: {self.time_left}",
            font=('Helvetica', 20),
            fg='white',
            bg='black'
        )
        self.timer_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.animation_frame, 
            bg='black', 
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Iniciar el temporizador y la animación
        self.is_animating = True
        self.time_left = self.animation_duration
        self.update_timer()
        self.root.after(100, self.setup_and_start_flash)

    def update_timer(self):
        """Actualiza el contador de tiempo y verifica si la animación debe terminar."""
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
            outline='white'
        )

        self.vx = random.uniform(-self.flash_speed, self.flash_speed)
        self.vy = random.uniform(-self.flash_speed, self.flash_speed)
        
        if abs(self.vx) < 1: self.vx = 1 if self.vx > 0 else -1
        if abs(self.vy) < 1: self.vy = 1 if self.vy > 0 else -1

        self.move_flash()

    def move_flash(self):
        """Mueve el destello si la animación está activa."""
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
        """Detiene la animación y muestra el mensaje final."""
        self.is_animating = False
        
        # Cancelar cualquier tarea pendiente
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        # Ocultar el contador
        self.timer_label.pack_forget()
        
        # Borrar el destello
        if hasattr(self, 'flash_item'):
            self.canvas.delete(self.flash_item)
            
        # Mostrar mensaje final
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text="Seguimiento Visual Terminado",
            fill='white',
            font=('Helvetica', 40, 'bold')
        )

# --- Ejecución del Programa ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = VisualTrackingApp(main_root)
    main_root.mainloop()