import tkinter as tk
from tkinter import font
import random

class AgilidadVisualApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Test de Agilidad Visual")
        self.geometry("800x600")
        self.config(bg="#2c3e50")

        # --- Variables del Juego ---
        self.aciertos = 0
        self.fallos = 0
        self.no_presionado = 0
        self.puntos_rojos_generados = 0
        self.total_puntos_rojos = 50
        
        self.punto_rojo_actual = None
        self.punto_rojo_activo = False
        self.punto_rojo_ya_acertado = False

        # Lista para guardar el historial de puntos con coordenadas relativas
        self.historial_puntos = []

        # --- Iniciar la primera pantalla ---
        self.crear_pantalla_inicio()

    def limpiar_ventana(self):
        """Destruye todos los widgets en la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def crear_pantalla_inicio(self):
        """Crea y muestra la pantalla de bienvenida."""
        self.limpiar_ventana()

        frame_card = tk.Frame(self, bg="#ecf0f1", relief="solid", bd=1, padx=50, pady=40)
        frame_card.pack(expand=True, pady=50)

        fuente_titulo = font.Font(family="Arial", size=28, weight="bold")
        titulo_label = tk.Label(
            frame_card,
            text="Test de Agilidad Visual",
            font=fuente_titulo,
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        titulo_label.pack(pady=(0, 20))

        fuente_instrucciones = font.Font(family="Arial", size=13)
        instrucciones_texto = (
            "¿Rápido para reaccionar?\n\n"
            "1. Aparecerán puntos rojos al azar en la pantalla.\n"
            "2. Presiona la BARRA ESPACIADORA tan pronto veas un punto rojo.\n"
            "   ¡Importante! Presiona solo UNA VEZ por punto.\n"
            "3. ¡No presiones si no hay nada!\n\n"
            "El test se vuelve más difícil a medida que avanzas.\n"
            "¡Mucha suerte!"
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

        fuente_boton = font.Font(family="Arial", size=16, weight="bold")
        boton_iniciar = tk.Button(
            frame_card,
            text="Iniciar Test",
            font=fuente_boton,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=30,
            pady=12,
            relief="flat",
            command=self.iniciar_juego,
            cursor="hand2"
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
        self.historial_puntos = []
        self.punto_rojo_activo = False
        self.punto_rojo_ya_acertado = False

        # --- Crear la interfaz del juego ---
        frame_marcador = tk.Frame(self, bg="#34495e", pady=10)
        frame_marcador.pack(fill="x")
        
        fuente_marcador = font.Font(family="Arial", size=14, weight="bold")
        self.label_aciertos = tk.Label(frame_marcador, text=f"Aciertos: {self.aciertos}", font=fuente_marcador, bg="#34495e", fg="#2ecc71")
        self.label_aciertos.pack(side="left", padx=40)
        
        self.label_fallos = tk.Label(frame_marcador, text=f"Fallos: {self.fallos}", font=fuente_marcador, bg="#34495e", fg="#e74c3c")
        self.label_fallos.pack(side="left", padx=40)

        self.label_no_presionado = tk.Label(frame_marcador, text=f"No presionado: {self.no_presionado}", font=fuente_marcador, bg="#34495e", fg="#f1c40f")
        self.label_no_presionado.pack(side="left", padx=40)
        
        self.canvas_juego = tk.Canvas(self, bg="#ecf0f1", highlightthickness=0)
        self.canvas_juego.pack(fill="both", expand=True, padx=20, pady=20)

        self.dibujar_punto_negro()
        
        self.bind("<space>", self.manejar_espacio)

        self.after(1500, self.programar_siguiente_punto_rojo)

    def dibujar_punto_negro(self):
        """Dibuja el punto negro en el centro del canvas."""
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()
        self.canvas_juego.delete("punto_negro")
        
        radio = 10
        self.canvas_juego.create_oval(
            canvas_width // 2 - radio, canvas_height // 2 - radio,
            canvas_width // 2 + radio, canvas_height // 2 + radio,
            fill="black", tags="punto_negro"
        )
        self.bind("<Configure>", lambda e: self.dibujar_punto_negro())

    def programar_siguiente_punto_rojo(self):
        """Programa la aparición del siguiente punto rojo si el juego no ha terminado."""
        if self.puntos_rojos_generados < self.total_puntos_rojos:
            tiempo_espera = random.randint(2000, 4000)
            self.after(tiempo_espera, self.mostrar_punto_rojo)
        else:
            self.after(2000, self.finalizar_juego)

    def mostrar_punto_rojo(self):
        """Muestra un punto rojo y guarda su posición relativa en el historial."""
        if self.puntos_rojos_generados >= self.total_puntos_rojos:
            return

        self.puntos_rojos_generados += 1
        
        self.canvas_juego.update_idletasks()
        canvas_width = self.canvas_juego.winfo_width()
        canvas_height = self.canvas_juego.winfo_height()

        if self.puntos_rojos_generados >= 15:
            size = 2 
        else:
            size = 4 
        
        x = random.randint(size, canvas_width - size)
        y = random.randint(size, canvas_height - size)

        self.punto_rojo_actual = self.canvas_juego.create_oval(
            x - size, y - size, x + size, y + size,
            fill="#e74c3c", outline="#e74c3c", tags="punto_rojo"
        )
        self.punto_rojo_activo = True
        self.punto_rojo_ya_acertado = False

        # --- CAMBIO CLAVE: Guardar coordenadas relativas ---
        # En lugar de guardar x, y, guardamos la proporción (entre 0.0 y 1.0)
        rel_x = x / canvas_width
        rel_y = y / canvas_height
        self.historial_puntos.append({'rx': rel_x, 'ry': rel_y, 'presionado': False})

        self.after(600, self.ocultar_punto_rojo)

    def ocultar_punto_rojo(self):
        """Oculta el punto rojo y comprueba si no fue presionado."""
        if self.punto_rojo_actual:
            self.canvas_juego.delete(self.punto_rojo_actual)
            self.punto_rojo_actual = None

        if self.punto_rojo_activo and not self.punto_rojo_ya_acertado:
            self.no_presionado += 1
            self.actualizar_marcador()

        self.punto_rojo_activo = False
        self.programar_siguiente_punto_rojo()

    def manejar_espacio(self, event):
        """Maneja el evento de presionar la barra espaciadora."""
        if self.punto_rojo_activo:
            if not self.punto_rojo_ya_acertado:
                self.aciertos += 1
                if self.historial_puntos:
                    self.historial_puntos[-1]['presionado'] = True
                self.punto_rojo_ya_acertado = True
            else:
                self.fallos += 1
        else:
            self.fallos += 1
        
        self.actualizar_marcador()

    def actualizar_marcador(self):
        """Actualiza las etiquetas del marcador en pantalla."""
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_fallos.config(text=f"Fallos: {self.fallos}")
        self.label_no_presionado.config(text=f"No presionado: {self.no_presionado}")

    def crear_pantalla_resultados_mapa(self):
        """Muestra el mapa de resultados escalando las coordenadas correctamente."""
        self.limpiar_ventana()
        self.unbind("<space>")
        self.unbind("<Configure>")

        frame_final = tk.Frame(self, bg="#2c3e50")
        frame_final.pack(fill="both", expand=True)

        fuente_titulo = font.Font(family="Arial", size=24, weight="bold")
        titulo = tk.Label(frame_final, text="Mapa de Resultados", font=fuente_titulo, bg="#2c3e50", fg="white")
        titulo.pack(pady=10)

        # Definir un tamaño fijo y adecuado para el mapa
        mapa_ancho = 700
        mapa_alto = 400
        canvas_mapa = tk.Canvas(frame_final, width=mapa_ancho, height=mapa_alto, bg="#ecf0f1", highlightthickness=1, highlightbackground="#34495e")
        canvas_mapa.pack(pady=10)

        # --- CAMBIO CLAVE: Dibujar usando coordenadas escaladas ---
        for punto in self.historial_puntos:
            # Recuperar las coordenadas relativas
            rel_x, rel_y = punto['rx'], punto['ry']
            
            # Escalarlas al tamaño del nuevo canvas del mapa
            final_x = rel_x * mapa_ancho
            final_y = rel_y * mapa_alto

            if punto['presionado']:
                # Punto verde para aciertos
                canvas_mapa.create_oval(final_x-5, final_y-5, final_x+5, final_y+5, fill="#2ecc71", outline="#27ae60")
            else:
                # X roja para no presionados
                canvas_mapa.create_line(final_x-6, final_y-6, final_x+6, final_y+6, fill="#e74c3c", width=3)
                canvas_mapa.create_line(final_x-6, final_y+6, final_x+6, final_y-6, fill="#e74c3c", width=3)

        frame_resumen = tk.Frame(frame_final, bg="#2c3e50")
        frame_resumen.pack(pady=10)

        fuente_resumen = font.Font(family="Arial", size=16)
        resumen_texto = f"Aciertos: {self.aciertos}  |  Fallos: {self.fallos}  |  No presionado: {self.no_presionado}"
        tk.Label(frame_resumen, text=resumen_texto, font=fuente_resumen, bg="#2c3e50", fg="white").pack(pady=5)

        fuente_boton = font.Font(family="Arial", size=14, weight="bold")
        boton_volver = tk.Button(
            frame_resumen,
            text="Volver al Menú",
            font=fuente_boton,
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            padx=20,
            pady=10,
            relief="flat",
            command=self.crear_pantalla_inicio,
            cursor="hand2"
        )
        boton_volver.pack(pady=10)

    def finalizar_juego(self):
        """Llama a la función que crea la pantalla de resultados con el mapa."""
        self.crear_pantalla_resultados_mapa()


if __name__ == "__main__":
    app = AgilidadVisualApp()
    app.mainloop()