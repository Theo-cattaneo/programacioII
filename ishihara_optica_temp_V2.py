# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
from io import BytesIO
import random

class IshiharaTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Agudeza Visual")
        
        # --- Configuración de la ventana ---
        self.root.minsize(1024, 580)
        self.root.state('zoomed')
        self.root.configure(bg="#1a1a2e")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # --- Paleta de Colores Moderna y Atractiva ---
        self.BG_COLOR = '#1a1a2e'
        self.FRAME_COLOR = '#16213e'
        self.ACCENT_COLOR_1 = '#58a6ff'
        self.ACCENT_COLOR_2 = '#ff6ec7'
        self.BUTTON_COLOR = '#4a235a'
        self.BUTTON_HOVER_COLOR = '#7307A5'
        self.TEXT_COLOR = '#c9d1d9'
        self.ERROR_COLOR = '#e74c3c'
        self.SUCCESS_COLOR = '#4CAF50'
        
        self.root.configure(bg=self.BG_COLOR)

        # --- Variables para el juego ---
        self.aciertos = 0
        self.errores = 0
        self.game_over = False
        self.time_left = 15
        self.timer_job = None
        self.imagen_actual = 0
        self.tiempo_limite = 15
        
        # --- Configuración de fuentes ---
        self.title_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.timer_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        self.imagenes = [
            {"url": "https://z-cdn-media.chatglm.cn/files/1a5c7ae0-dddf-4521-9f5a-6fd0b8d339ed_45.jpg?auth_key=1793024034-32e60631a7d44e25b9fc1cc97b90f45a-0-d9e94551954d1eab16a0ffeac53a433b", "respuesta": "45", "nombre": "45.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/ba042b7a-3d0e-4e94-b31f-dbf90bb96df3_74.jpg?auth_key=1793024034-d065bc43c16546d8b6e69d4f5734dfb5-0-0cbc7db1df4097d4eb969afef11e9f2b", "respuesta": "74", "nombre": "74.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/13cfcd70-d9be-4ee6-affa-0190f27a5c60_20.jpg?auth_key=1793024034-fa58c906e8744be488eedffa0f345546-0-5ab5e544c34e552f35bb3346dc3631ac", "respuesta": "20", "nombre": "20.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/91867a48-979b-48fb-94ed-b8d28c98908d_78.jpg?auth_key=1793024034-3fba2502242149f3a30342e01c329301-0-5df7422d788c14ab70ebfaa5042b92a8", "respuesta": "78", "nombre": "78.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/24ecf2c3-8c5c-49ac-bf1d-cefbf63387e9_8.jpg?auth_key=1793024034-335197524f654bcd8786a4ad5274bdec-0-b3a2c1cd55ca7ad9475f42550b3d2a95", "respuesta": "8", "nombre": "8.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/4089b402-c072-41ab-9421-858c5e489fe4_96.jpg?auth_key=1793024034-2aefac8cd1474d30ba5cf0f22ef35568-0-e9076100163405c097c18938b54e10f7", "respuesta": "96", "nombre": "96.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/f40ca8ff-aee2-4512-8c1f-78d3d5172475_42.jpg?auth_key=1793024034-5c2d84ccb41a4924ac1f94c96c1cb647-0-4d65a9b51c06b87ae77bf456c5515df1", "respuesta": "42", "nombre": "42.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/d119f591-e8c3-45bc-bf96-275aa255b82d_5.jpg?auth_key=1793245299-4f06b48a214d43b094d92a8987e1e383-0-defa771b242ce24dc4b19c0278f036a4", "respuesta": "5", "nombre": "5.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/e2ab36b4-0394-440e-8472-c26965d0dc44_7.jpg?auth_key=1793245299-02f057ebfa714cb580f7954afa77a3ee-0-30bb03d51079954305ad74fd5cd65dd1", "respuesta": "7", "nombre": "7.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/2253b404-7702-4b6b-9527-1a6043a3a2ce_2.jpg?auth_key=1793245299-4b4edf34f42149d7bd2ed53d70a902e6-0-1d5cfe8e5821bc32cbc844100a2ca6b5", "respuesta": "2", "nombre": "2.jpg"},
            

            # --- Imágenes de Patrones (Lineas) ---
            {"url": "https://z-cdn-media.chatglm.cn/files/72c37382-3b51-484d-9553-93fbf728fc4b_lineas.jpg?auth_key=1793244246-c8294d1c4d344700bc8cb26fcbc4bf5b-0-d1dc642278a8825a09ca6c5c5998fc5a", "respuesta": "lineas", "nombre": "lineas.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/b836cffa-25e9-425e-995b-9cf6da6e1346_lineas2.jpg?auth_key=1793244246-ee5b99a3f9cb4ad6b5ff3a4471a03417-0-3f9d1c31a7f7d8f98022f7f40a0f2fc8", "respuesta": "lineas", "nombre": "lineas2.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/8c4342fc-9d27-4db4-85d3-6e8ec5ff7daf_lineas3.jpg?auth_key=1793244246-3113d3f9d91b46aab931222064df0c23-0-243d645f227754e8243cf5d8b571a4a8", "respuesta": "lineas", "nombre": "lineas3.jpg"},
            
            # --- IMAGEN CON RESPUESTA CORREGIDA ---
            {"url": "https://z-cdn-media.chatglm.cn/files/9299c7f4-25e5-419a-a46b-df4c960348f7_12.jpg?auth_key=1793244246-4c6252ec9dc941a1957712e161f69352-0-b5bf6f508dca7e7e62e3bab76d93fb27", "respuesta": "12", "nombre": "12.jpg"},
        ]
        
        random.shuffle(self.imagenes)
        self.imagenes_descargadas = []
        self.descargar_imagenes()
        self.crear_menu_inicio()

    def crear_menu_inicio(self):
        """Crea la pantalla de bienvenida con un diseño moderno."""
        self.menu_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Título principal
        title_label = tk.Label(
            self.menu_frame,
            text="Bienvenido al Test de Ishihara",
            font=self.title_font,
            fg=self.ACCENT_COLOR_1,
            bg=self.BG_COLOR
        )
        title_label.pack(pady=(50, 10))

        # Subtítulo con animación de color
        subtitle_label = tk.Label(
            self.menu_frame,
            text="Prepárate tus sentidos para una prueba de agudeza visual.",
            font=self.normal_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        subtitle_label.pack(pady=10)
        
        # Marco para el botón
        button_frame = tk.Frame(self.menu_frame, bg=self.BG_COLOR)
        button_frame.pack(pady=40)

        # Botón de inicio con efecto hover
        self.start_button = tk.Button(
            button_frame,
            text="Empecemos",
            command=self.iniciar_juego,
            font=self.button_font,
            bg=self.BUTTON_COLOR,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2",
            activebackground=self.BUTTON_HOVER_COLOR,
            borderwidth=0
        )
        self.start_button.pack()

        # --- Efecto de animación de texto ---
        self.animate_text_color(subtitle_label, self.TEXT_COLOR, self.ACCENT_COLOR_1, 2000)

    def animate_text_color(self, widget, color1, color2, duration_ms):
        """Cambia gradualmente el color de un widget de un color a otro."""
        widget.config(fg=color1)
        self.root.after(duration_ms, lambda: widget.config(fg=color2))

    def iniciar_juego(self):
        """Oculta el menú y muestra la interfaz del juego."""
        self.menu_frame.pack_forget()
        
        # --- CORRECCIÓN: Se crean los widgets solo una vez ---
        if not hasattr(self, 'game_frame'):
            self.crear_widgets_juego()
        
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.frame_info.pack(fill=tk.X, pady=(10, 0))
        self.frame_contenido.pack(fill=tk.BOTH, expand=True)
        self.canvas_imagen.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.frame_interaccion.pack(fill=tk.X, pady=(0, 20))
        self.label_resultado.pack(fill=tk.X, pady=(0, 20))

        self.reset_game_state()
        self.mostrar_imagen()

    def crear_widgets_juego(self):
        """Crea todos los widgets necesarios para el juego."""
        self.game_frame = tk.Frame(self.root, bg=self.FRAME_COLOR)
        
        self.frame_info = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, borderwidth=1)
        self.frame_info.pack(fill=tk.X, pady=(10, 0))
        
        self.label_temporizador = tk.Label(self.frame_info, text=f"Tiempo: {self.tiempo_limite}s", font=self.timer_font, bg="white", fg=self.TEXT_COLOR)
        self.label_temporizador.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.label_aciertos = tk.Label(self.frame_info, text=f"Aciertos: {self.aciertos}", font=self.normal_font, bg="white", fg=self.SUCCESS_COLOR)
        self.label_aciertos.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.label_errores = tk.Label(self.frame_info, text=f"Errores: {self.errores}", font=self.normal_font, bg="white", fg=self.ERROR_COLOR)
        self.label_errores.pack(side=tk.LEFT, padx=20, pady=10)

        self.label_progreso = tk.Label(self.frame_info, text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}", font=self.normal_font, bg="white", fg=self.TEXT_COLOR)
        self.label_progreso.pack(side=tk.RIGHT, padx=20, pady=10)

        self.frame_contenido = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        self.frame_contenido.rowconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(0, weight=1)
        
        self.canvas_imagen = tk.Canvas(self.frame_contenido, bg="white", highlightthickness=0)
        self.canvas_imagen.bind('<Configure>', self.on_canvas_resize)

        self.frame_interaccion = tk.Frame(self.frame_contenido, bg="white")
        self.frame_interaccion.pack(fill=tk.X, pady=(0, 20))
        
        self.label_pregunta = tk.Label(self.frame_interaccion, text="¿Qué ves en la imagen? (Número o 'lineas')", font=self.normal_font, bg="white")
        self.label_pregunta.pack(pady=5)
        
        self.entry_respuesta = tk.Entry(self.frame_interaccion, font=self.normal_font, width=15, justify='center', relief=tk.FLAT, borderwidth=2, bg="#F5F5F5")
        self.entry_respuesta.pack(pady=5)
        self.entry_respuesta.bind("<KeyRelease>", self.verificar_entrada)
        self.entry_respuesta.bind("<Return>", lambda event: self.verificar_respuesta())
        
        self.boton_verificar = tk.Button(self.frame_interaccion, text="Verificar", command=self.verificar_respuesta, font=self.button_font, bg=self.BUTTON_COLOR, fg=self.TEXT_COLOR, relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.boton_verificar.pack(pady=10)

        self.label_resultado = tk.Label(self.frame_contenido, text="", font=self.result_font, bg="white", height=2)
        self.label_resultado.pack(fill=tk.X, pady=(0, 20))

    def reset_game_state(self):
        """Reinicia las variables del juego a su estado inicial y actualiza las etiquetas."""
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        self.game_over = False
        self.time_left = self.tiempo_limite
        
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_errores.config(text=f"Errores: {self.errores}")
        self.label_resultado.config(text="")

    def descargar_imagenes(self):
        for img_data in self.imagenes:
            try:
                response = requests.get(img_data["url"], timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                self.imagenes_descargadas.append({
                    "pil_image": img,
                    "respuesta": img_data["respuesta"],
                    "nombre": img_data["nombre"]
                })
            except Exception as e:
                print(f"Error al descargar {img_data['nombre']}. Creando imagen de respaldo.")
                self.imagenes_descargadas.append(self.crear_imagen_respaldo(img_data))

    def crear_imagen_respaldo(self, img_data):
        """Crea una imagen de respaldo si la descarga falla."""
        respuesta = img_data["respuesta"]
        img = Image.new('RGB', (400, 400), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except IOError:
            font = ImageFont.load_default()
        
        text_color = '#333333'
        draw.text((200, 160), respuesta, font=font, fill=text_color, anchor="mm")
        
        return {
            "pil_image": img,
            "respuesta": respuesta,
            "nombre": img_data["nombre"]
        }

    def on_canvas_resize(self, event):
        if self.game_over:
            return
        if self.imagen_actual < len(self.imagenes_descargadas):
            self.mostrar_imagen_en_canvas(event.width, event.height)

    def mostrar_imagen_en_canvas(self, canvas_width, canvas_height):
        pil_img = self.imagenes_descargadas[self.imagen_actual]["pil_image"]
        
        img_ratio = pil_img.width / pil_img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width - 40
            new_height = int(new_width / img_ratio)
        else:
            new_height = canvas_height - 40
            new_width = int(new_height * img_ratio)
        
        resized_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
        self.current_photo = ImageTk.PhotoImage(resized_img)

        self.canvas_imagen.delete("all")
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas_imagen.create_image(x, y, anchor="nw", image=self.current_photo)

    def mostrar_imagen(self):
        if self.game_over:
            return
            
        self.game_over = False
        
        if self.imagen_actual < len(self.imagenes_descargadas):
            self.canvas_imagen.update_idletasks()
            self.mostrar_imagen_en_canvas(self.canvas_imagen.winfo_width(), self.canvas_imagen.winfo_height())
            
            self.entry_respuesta.delete(0, tk.END)
            self.entry_respuesta.focus()
            
            self.label_resultado.config(text="")
            self.label_progreso.config(text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}")
            
            self.iniciar_temporizador()
        else:
            self.mostrar_resultado_final()

    def iniciar_temporizador(self):
        self.time_left = self.tiempo_limite
        self.actualizar_label_temporizador()
        
        self.entry_respuesta.config(state=tk.NORMAL)
        self.boton_verificar.config(state=tk.DISABLED)

        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.contar_hacia_atras()

    def contar_hacia_atras(self):
        if self.time_left > 0 and not self.game_over:
            self.time_left -= 1
            self.actualizar_label_temporizador()
            self.timer_job = self.root.after(1000, self.contar_hacia_atras)
        else:
            self.tiempo_agotado()

    def actualizar_label_temporizador(self):
        color = self.TEXT_COLOR
        if self.time_left <= 5:
            color = self.ERROR_COLOR
        self.label_temporizador.config(text=f"Tiempo: {self.time_left}s", fg=color)

    def verificar_entrada(self, event):
        if self.entry_respuesta.get().strip():
            self.boton_verificar.config(state=tk.NORMAL)
        else:
            self.boton_verificar.config(state=tk.DISABLED)

    def verificar_respuesta(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        respuesta_usuario = self.entry_respuesta.get().strip()
        respuesta_correcta = self.imagenes_descargadas[self.imagen_actual]["respuesta"]
        
        self.entry_respuesta.delete(0, tk.END)
        self.entry_respuesta.config(state=tk.DISABLED)
        self.boton_verificar.config(state=tk.DISABLED)
        
        if self.es_respuesta_valida(respuesta_usuario, respuesta_correcta):
            self.aciertos += 1
            self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
            self.label_resultado.config(text="✓ Correcto", fg=self.SUCCESS_COLOR)
            self.animate_text_color(self.label_resultado, self.SUCCESS_COLOR, self.TEXT_COLOR, 500)
        else:
            self.errores += 1
            self.label_errores.config(text=f"Errores: {self.errores}")
            self.label_resultado.config(text=f"✗ Incorrecto. La respuesta correcta era: {respuesta_correcta}", fg=self.ERROR_COLOR)
            self.animate_text_color(self.label_resultado, self.ERROR_COLOR, self.TEXT_COLOR, 500)
        
        self.root.after(1500, self.siguiente_imagen)

    def es_respuesta_valida(self, usuario, correcta):
        """Verifica si la respuesta del usuario es válida, aceptando 'linea'/'lineas' para 'lineas'."""
        if correcta.lower() == "lineas":
            return usuario.lower() in ["linea", "lineas"]
        return usuario.lower() == correcta.lower()

    def tiempo_agotado(self):
        self.entry_respuesta.delete(0, tk.END)
        self.errores += 1
        self.label_errores.config(text=f"Errores: {self.errores}")
        self.label_resultado.config(text=f"¡Tiempo agotado! La respuesta correcta era: {self.imagenes_descargadas[self.imagen_actual]['respuesta']}", fg=self.ERROR_COLOR)
        self.animate_text_color(self.label_resultado, self.ERROR_COLOR, self.TEXT_COLOR, 500)
        
        self.root.after(1500, self.siguiente_imagen)
    
    def siguiente_imagen(self):
        self.imagen_actual += 1
        self.mostrar_imagen()
    
    def mostrar_resultado_final(self):
        self.game_over = True
        
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        self.frame_contenido.pack_forget()
        self.frame_interaccion.pack_forget()
        self.label_resultado.pack_forget()

        self.frame_resultado_final = tk.Frame(self.root, bg=self.BG_COLOR)
        self.frame_resultado_final.pack(fill=tk.BOTH, expand=True)

        total = self.aciertos + self.errores
        porcentaje_aciertos = (self.aciertos / total) * 100 if total > 0 else 0
        
        resultado_texto = f"Test completado\n\n"
        resultado_texto += f"Aciertos: {self.aciertos}\n"
        resultado_texto += f"Errores: {self.errores}\n"
        resultado_texto += f"Porcentaje de aciertos: {porcentaje_aciertos:.1f}%\n\n"
        
        if porcentaje_aciertos >= 80:
            resultado_texto += "¡Excelente! Tu visión del color parece ser normal."
        elif porcentaje_aciertos >= 50:
            resultado_texto += "Podrías tener alguna dificultad para percibir ciertos colores."
        else:
            resultado_texto += "Es posible que tengas algún tipo de daltonismo. Te recomendamos consultar con un especialista."
        
        self.label_resultado_final = tk.Label(self.frame_resultado_final, text=resultado_texto, font=self.result_font, bg=self.BG_COLOR, justify=tk.CENTER)
        self.label_resultado_final.pack(pady=20, expand=True)
        
        self.frame_botones_finales = tk.Frame(self.frame_resultado_final, bg=self.BG_COLOR)
        self.frame_botones_finales.pack(pady=10)
        
        menu_button = tk.Button(self.frame_botones_finales, text="Volver al Menú", command=self.mostrar_menu_inicio, font=self.button_font, bg=self.ACCENT_COLOR_1, fg=self.BG_COLOR, relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        menu_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(self.frame_botones_finales, text="Cerrar", command=self.root.quit, font=self.button_font, bg=self.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        close_button.pack(side=tk.LEFT, padx=10)
    
    def mostrar_menu_inicio(self):
        # --- CORRECCIÓN: Se verifica si el widget existe antes de intentar ocultarlo ---
        if hasattr(self, 'game_frame'):
            self.game_frame.pack_forget()
        if hasattr(self, 'frame_resultado_final'):
            self.frame_resultado_final.pack_forget()

        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.reset_game_state()

# --- Ejecución del Programa ---
if __name__ == "__main__":
    root = tk.Tk()
    app = IshiharaTestApp(root)
    root.mainloop()