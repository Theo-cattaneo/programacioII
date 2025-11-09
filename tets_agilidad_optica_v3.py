import tkinter as tk
from tkinter import font
import random

class AgilidadVisualApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Test de Agilidad Visual")
        self.geometry("800x600")
        # CAMBIO: La ventana ahora se puede redimensionar
        self.config(bg="#2c3e50") # Color de fondo oscuro y moderno

        # --- Variables del Juego ---
        self.aciertos = 0
        self.fallos = 0
        self.no_presionado = 0
        self.puntos_rojos_generados = 0
        self.total_puntos_rojos = 50
        
        self.punto_rojo_actual = None
        self.punto_rojo_activo = False

        # --- Iniciar la primera pantalla ---
        self.crear_pantalla_inicio()

    def limpiar_ventana(self):
        """Destruye todos los widgets en la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def crear_pantalla_inicio(self):
        """Crea y muestra la pantalla de bienvenida con un diseño mejorado."""
        self.limpiar_ventana()

        # --- Frame principal con estilo de "tarjeta" ---
        frame_card = tk.Frame(self, bg="#ecf0f1", relief="solid", bd=1, padx=50, pady=40)
        frame_card.pack(expand=True, pady=50)

        # Título
        fuente_titulo = font.Font(family="Arial", size=28, weight="bold")
        titulo_label = tk.Label(
            frame_card,
            text="Test de Agilidad Visual",
            font=fuente_titulo,
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        titulo_label.pack(pady=(0, 20))

        # Instrucciones
        fuente_instrucciones = font.Font(family="Arial", size=13)
        instrucciones_texto = (
            "Cada vez que aparezca un punto rojo, presiona la barra espaciadora.\n\n"
            "• Aciertos: Presionas cuando el punto rojo es visible.\n"
            "• Fallos: Presionas cuando no hay ningún punto.\n"
            "• No presionado: Dejas pasar un punto rojo.\n\n"
            "¡Prepárate y pon a prueba tus reflejos!"
        )
        instrucciones_label = tk.Label(
            frame_card,
            text=instrucciones_texto,
            font=fuente_instrucciones,
            bg="#ecf0f1",
            fg="#34495e",
            justify="center"
        )
        instrucciones_label.pack(pady=10)

        # Botón de Inicio con estilo moderno
        fuente_boton = font.Font(family="Arial", size=16, weight="bold")
        boton_iniciar = tk.Button(
            frame_card,
            text="Iniciar Test",
            font=fuente_boton,
            bg="#3498db", # Azul atractivo
            fg="white",
            activebackground="#2980b9", # Azul más oscuro al hacer clic
            activeforeground="white",
            padx=30,
            pady=12,
            relief="flat",
            command=self.iniciar_juego,
            cursor="hand2" # Cursor de mano al pasar el ratón
        )
        boton_iniciar.pack(pady=(30, 0))

    def iniciar_juego(self):
        """Prepara y comienza la partida."""
        self.limpiar_ventana()
        
        # Resetear variables del juego
        self.aciertos = 0
        self.fallos = 0
        self.no_presionado = 0
        self.puntos_rojos_generados = 0

        # --- Crear la interfaz del juego ---
        # Frame para el marcador
        frame_marcador = tk.Frame(self, bg="#34495e", pady=10)
        frame_marcador.pack(fill="x")
        
        fuente_marcador = font.Font(family="Arial", size=14, weight="bold")
        self.label_aciertos = tk.Label(frame_marcador, text=f"Aciertos: {self.aciertos}", font=fuente_marcador, bg="#34495e", fg="#2ecc71")
        self.label_aciertos.pack(side="left", padx=40)
        
        self.label_fallos = tk.Label(frame_marcador, text=f"Fallos: {self.fallos}", font=fuente_marcador, bg="#34495e", fg="#e74c3c")
        self.label_fallos.pack(side="left", padx=40)

        self.label_no_presionado = tk.Label(frame_marcador, text=f"No presionado: {self.no_presionado}", font=fuente_marcador, bg="#34495e", fg="#f1c40f")
        self.label_no_presionado.pack(side="left", padx=40)
        
        # Canvas para el juego
        self.canvas_juego = tk.Canvas(self, bg="#ecf0f1", highlightthickness=0)
        self.canvas_juego.pack(fill="both", expand=True, padx=20, pady=20)

        # Punto negro en el centro (se dibujará después de que el canvas tenga tamaño)
        self.dibujar_punto_negro()
        
        # Asociar la tecla espaciadora a la función de manejo
        self.bind("<space>", self.manejar_espacio)

        # Iniciar el ciclo del juego
        self.after(1500, self.programar_siguiente_punto_rojo)

    def dibujar_punto_negro(self):
        """Dibuja el punto negro en el centro del canvas."""
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()
        self.canvas_juego.delete("punto_negro") # Borrar el anterior si existe
        self.canvas_juego.create_oval(
            canvas_width // 2 - 15, canvas_height // 2 - 15,
            canvas_width // 2 + 15, canvas_height // 2 + 15,
            fill="#2c3e50", tags="punto_negro"
        )
        # Si la ventana se redimensiona, volvemos a dibujar el punto negro
        self.bind("<Configure>", lambda e: self.dibujar_punto_negro())


    def programar_siguiente_punto_rojo(self):
        """Programa la aparición del siguiente punto rojo si el juego no ha terminado."""
        if self.puntos_rojos_generados < self.total_puntos_rojos:
            tiempo_espera = random.randint(2000, 4000)
            self.after(tiempo_espera, self.mostrar_punto_rojo)
        else:
            self.after(2000, self.finalizar_juego)

    def mostrar_punto_rojo(self):
        """Muestra un punto rojo en una posición aleatoria."""
        if self.puntos_rojos_generados >= self.total_puntos_rojos:
            return

        self.puntos_rojos_generados += 1
        
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()

        # CAMBIO: Lógica de tamaño dinámico para el punto rojo
        # A partir del punto 25, el tamaño se reduce aún más
        if self.puntos_rojos_generados >= 25:
            size = 2 # Tamaño muy pequeño para mayor dificultad
        else:
            size = 4 # Tamaño pequeño inicial
        
        x = random.randint(size, canvas_width - size)
        y = random.randint(size, canvas_height - size)

        self.punto_rojo_actual = self.canvas_juego.create_oval(
            x - size, y - size, x + size, y + size,
            fill="#e74c3c", outline="#e74c3c", tags="punto_rojo"
        )
        self.punto_rojo_activo = True

        self.after(2000, self.ocultar_punto_rojo)

    def ocultar_punto_rojo(self):
        """Oculta el punto rojo y comprueba si no fue presionado."""
        if self.punto_rojo_actual:
            self.canvas_juego.delete(self.punto_rojo_actual)
            self.punto_rojo_actual = None

        if self.punto_rojo_activo:
            self.no_presionado += 1
            self.actualizar_marcador()

        self.punto_rojo_activo = False
        self.programar_siguiente_punto_rojo()

    def manejar_espacio(self, event):
        """Maneja el evento de presionar la barra espaciadora."""
        if self.punto_rojo_activo:
            self.aciertos += 1
            self.punto_rojo_activo = False
        else:
            self.fallos += 1
        
        self.actualizar_marcador()

    def actualizar_marcador(self):
        """Actualiza las etiquetas del marcador en pantalla."""
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_fallos.config(text=f"Fallos: {self.fallos}")
        self.label_no_presionado.config(text=f"No presionado: {self.no_presionado}")

    def finalizar_juego(self):
        """Muestra la pantalla final con los resultados y las nuevas opciones."""
        self.unbind("<space>")
        self.unbind("<Configure>") # Dejar de redibujar el punto negro
        self.limpiar_ventana()

        # --- Frame final con estilo de "tarjeta" ---
        frame_final_card = tk.Frame(self, bg="#ecf0f1", relief="solid", bd=1, padx=50, pady=40)
        frame_final_card.pack(expand=True, pady=50)

        fuente_titulo_final = font.Font(family="Arial", size=26, weight="bold")
        fuente_resultados = font.Font(family="Arial", size=18)

        tk.Label(frame_final_card, text="¡Test Finalizado!", font=fuente_titulo_final, bg="#ecf0f1", fg="#2c3e50").pack(pady=(0, 20))
        
        resultados_texto = (
            f"Aciertos: {self.aciertos}\n"
            f"Fallos: {self.fallos}\n"
            f"No presionado: {self.no_presionado}"
        )
        tk.Label(frame_final_card, text=resultados_texto, font=fuente_resultados, bg="#ecf0f1", fg="#34495e", justify="center").pack(pady=10)
        
        # Frame para contener los botones
        frame_botones = tk.Frame(frame_final_card, bg="#ecf0f1")
        frame_botones.pack(pady=20)

        # Botón para volver al menú
        boton_menu = tk.Button(
            frame_botones,
            text="Volver al Menú",
            font=fuente_resultados,
            bg="#27ae60", # Verde para acción positiva
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.crear_pantalla_inicio,
            cursor="hand2"
        )
        boton_menu.pack(side="left", padx=10)

        # Botón para cerrar el programa
        boton_cerrar = tk.Button(
            frame_botones,
            text="Cerrar Programa",
            font=fuente_resultados,
            bg="#c0392b", # Rojo para acción de salida
            fg="white",
            activebackground="#a93226",
            activeforeground="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.destroy,
            cursor="hand2"
        )
        boton_cerrar.pack(side="left", padx=10)


if __name__ == "__main__":
    app = AgilidadVisualApp()
    app.mainloop()