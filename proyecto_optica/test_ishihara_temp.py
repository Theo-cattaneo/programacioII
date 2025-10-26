import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random

class IshiharaTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test de Ishihara")
        self.root.geometry("850x800")
        self.root.configure(bg="#E8EAF6") # Fondo lila/gris claro

        # --- Variables para el juego ---
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        
        # --- Variables para el temporizador (15 segundos) ---
        self.tiempo_limite = 15
        self.tiempo_restante = self.tiempo_limite
        self.id_temporizador = None

        # Configuración de fuentes
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=13, weight="bold")
        self.timer_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        self.imagenes = [
            {"url": "https://z-cdn-media.chatglm.cn/files/1a5c7ae0-dddf-4521-9f5a-6fd0b8d339ed_45.jpg?auth_key=1793024034-32e60631a7d44e25b9fc1cc97b90f45a-0-d9e94551954d1eab16a0ffeac53a433b", "respuesta": "45", "nombre": "45.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/ba042b7a-3d0e-4e94-b31f-dbf90bb96df3_74.jpg?auth_key=1793024034-d065bc43c16546d8b6e69d4f5734dfb5-0-0cbc7db1df4097d4eb969afef11e9f2b", "respuesta": "74", "nombre": "74.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/13cfcd70-d9be-4ee6-affa-0190f27a5c60_20.jpg?auth_key=1793024034-fa58c906e8744be488eedffa0f345546-0-5ab5e544c34e552f35bb3346dc3631ac", "respuesta": "20", "nombre": "20.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/91867a48-979b-48fb-94ed-b8d28c98908d_78.jpg?auth_key=1793024034-3fba2502242149f3a30342e01c329301-0-5df7422d788c14ab70ebfaa5042b92a8", "respuesta": "78", "nombre": "78.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/24ecf2c3-8c5c-49ac-bf1d-cefbf63387e9_8.jpg?auth_key=1793024034-335197524f654bcd8786a4ad5274bdec-0-b3a2c1cd55ca7ad9475f42550b3d2a95", "respuesta": "8", "nombre": "8.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/4089b402-c072-41ab-9421-858c5e489fe4_96.jpg?auth_key=1793024034-2aefac8cd1474d30ba5cf0f22ef35568-0-e9076100163405c097c18938b54e10f7", "respuesta": "96", "nombre": "96.jpg"},
            {"url": "https://z-cdn-media.chatglm.cn/files/f40ca8ff-aee2-4512-8c1f-78d3d5172475_42.jpg?auth_key=1793024034-5c2d84ccb41a4924ac1f94c96c1cb647-0-4d65a9b51c06b87ae77bf456c5515df1", "respuesta": "42", "nombre": "42.jpg"}
        ]
        
        random.shuffle(self.imagenes)
        self.imagenes_descargadas = []
        self.descargar_imagenes()
        self.crear_widgets()
        self.mostrar_imagen()
    
    def descargar_imagenes(self):
        for img_data in self.imagenes:
            try:
                response = requests.get(img_data["url"])
                img = Image.open(BytesIO(response.content))
                img = img.resize((400, 400), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.imagenes_descargadas.append({
                    "photo": photo,
                    "respuesta": img_data["respuesta"],
                    "nombre": img_data["nombre"]
                })
            except Exception as e:
                print(f"Error al descargar la imagen {img_data['nombre']}: {e}")
                img = Image.new('RGB', (400, 400), color='white')
                photo = ImageTk.PhotoImage(img)
                self.imagenes_descargadas.append({
                    "photo": photo,
                    "respuesta": img_data["respuesta"],
                    "nombre": img_data["nombre"]
                })
    
    def crear_widgets(self):
        self.titulo = tk.Label(self.root, text="Test de Ishihara", font=self.title_font, bg="#E8EAF6", fg="#3F51B5")
        self.titulo.pack(pady=(20, 10))
        
        self.main_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, borderwidth=2)
        self.main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.frame_imagen = tk.Frame(self.main_frame, bg="white")
        self.frame_imagen.pack(pady=20)
        self.label_imagen = tk.Label(self.frame_imagen, bg="white")
        self.label_imagen.pack()
        
        self.frame_interaccion = tk.Frame(self.main_frame, bg="white")
        self.frame_interaccion.pack(pady=10)
        
        self.label_pregunta = tk.Label(self.frame_interaccion, text="¿Qué número ves en la imagen?", font=self.normal_font, bg="white")
        self.label_pregunta.pack(pady=5)
        
        self.entry_respuesta = tk.Entry(self.frame_interaccion, font=self.normal_font, width=10, justify='center', relief=tk.FLAT, borderwidth=2, bg="#F5F5F5")
        self.entry_respuesta.pack(pady=5)
        self.entry_respuesta.bind("<KeyRelease>", self.verificar_entrada)
        self.entry_respuesta.bind("<Return>", lambda event: self.verificar_respuesta())
        
        self.boton_verificar = tk.Button(self.frame_interaccion, text="Verificar", command=self.verificar_respuesta, font=self.button_font, bg="#4CAF50", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.boton_verificar.pack(pady=10)

        self.label_temporizador = tk.Label(self.main_frame, text=f"Tiempo restante: {self.tiempo_limite}s", font=self.timer_font, bg="white", fg="#3F51B5")
        self.label_temporizador.pack(pady=5)

        self.label_resultado = tk.Label(self.main_frame, text="", font=self.result_font, bg="white", height=2)
        self.label_resultado.pack(pady=10)
        
        self.frame_contadores = tk.Frame(self.main_frame, bg="white")
        self.frame_contadores.pack(pady=10)
        
        self.label_aciertos = tk.Label(self.frame_contadores, text=f"Aciertos: {self.aciertos}", font=self.normal_font, bg="white", fg="#4CAF50")
        self.label_aciertos.pack(side=tk.LEFT, padx=30)
        
        self.label_errores = tk.Label(self.frame_contadores, text=f"Errores: {self.errores}", font=self.normal_font, bg="white", fg="#F44336")
        self.label_errores.pack(side=tk.LEFT, padx=30)
        
        self.label_progreso = tk.Label(self.main_frame, text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}", font=self.normal_font, bg="white", fg="#757575")
        self.label_progreso.pack(pady=(10, 20))

    def mostrar_imagen(self):
        if self.imagen_actual < len(self.imagenes_descargadas):
            self.label_imagen.config(image=self.imagenes_descargadas[self.imagen_actual]["photo"])
            
            # Se limpia y enfoca el campo de texto al mostrar una nueva imagen
            self.entry_respuesta.delete(0, tk.END)
            self.entry_respuesta.focus()
            
            self.label_resultado.config(text="")
            self.label_progreso.config(text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}")
            
            self.iniciar_temporizador()
        else:
            self.mostrar_resultado_final()

    def iniciar_temporizador(self):
        self.tiempo_restante = self.tiempo_limite
        self.actualizar_label_temporizador()
        
        self.entry_respuesta.config(state=tk.NORMAL)
        self.boton_verificar.config(state=tk.DISABLED)

        if self.id_temporizador:
            self.root.after_cancel(self.id_temporizador)
        
        self.contar_hacia_atras()

    def contar_hacia_atras(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.actualizar_label_temporizador()
            self.id_temporizador = self.root.after(1000, self.contar_hacia_atras)
        else:
            self.tiempo_agotado()

    def actualizar_label_temporizador(self):
        color = "#3F51B5"
        if self.tiempo_restante <= 5:
            color = "#F44336"
        self.label_temporizador.config(text=f"Tiempo restante: {self.tiempo_restante}s", fg=color)

    def verificar_entrada(self, event):
        if self.entry_respuesta.get().strip():
            self.boton_verificar.config(state=tk.NORMAL)
        else:
            self.boton_verificar.config(state=tk.DISABLED)

    def verificar_respuesta(self):
        if self.id_temporizador:
            self.root.after_cancel(self.id_temporizador)
            self.id_temporizador = None

        respuesta_usuario = self.entry_respuesta.get().strip()
        respuesta_correcta = self.imagenes_descargadas[self.imagen_actual]["respuesta"]
        
        # --- CORRECCIÓN CLAVE: Limpiar el campo de texto INMEDIATAMENTE después de obtener la respuesta ---
        self.entry_respuesta.delete(0, tk.END)

        self.entry_respuesta.config(state=tk.DISABLED)
        self.boton_verificar.config(state=tk.DISABLED)
        
        if respuesta_usuario.lower() == respuesta_correcta.lower():
            self.aciertos += 1
            self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
            self.label_resultado.config(text="✓ ¡Correcto! Has acertado el número.", fg="#4CAF50")
        else:
            self.errores += 1
            self.label_errores.config(text=f"Errores: {self.errores}")
            self.label_resultado.config(text=f"✗ Incorrecto. El número correcto era: {respuesta_correcta}", fg="#F44336")
        
        self.root.after(1500, self.siguiente_imagen)

    def tiempo_agotado(self):
        # --- CORRECCIÓN CLAVE: También limpiar el campo si el tiempo se agota ---
        self.entry_respuesta.delete(0, tk.END)

        self.errores += 1
        self.label_errores.config(text=f"Errores: {self.errores}")
        respuesta_correcta = self.imagenes_descargadas[self.imagen_actual]["respuesta"]
        self.label_resultado.config(text=f"⏱ ¡Tiempo agotado! El número correcto era: {respuesta_correcta}", fg="#FF9800")
        
        self.entry_respuesta.config(state=tk.DISABLED)
        self.boton_verificar.config(state=tk.DISABLED)
        
        self.root.after(1500, self.siguiente_imagen)
    
    def siguiente_imagen(self):
        self.imagen_actual += 1
        self.mostrar_imagen()
    
    def mostrar_resultado_final(self):
        if self.id_temporizador:
            self.root.after_cancel(self.id_temporizador)

        self.frame_imagen.pack_forget()
        self.frame_interaccion.pack_forget()
        self.label_resultado.pack_forget()
        self.label_temporizador.pack_forget()
        self.frame_contadores.pack_forget()
        self.label_progreso.pack_forget()

        self.frame_resultado_final = tk.Frame(self.main_frame, bg="white")
        self.frame_resultado_final.pack(pady=20, expand=True)

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
        
        self.label_resultado_final = tk.Label(self.frame_resultado_final, text=resultado_texto, font=self.normal_font, bg="white", justify=tk.CENTER)
        self.label_resultado_final.pack(pady=20)
        
        self.frame_botones_finales = tk.Frame(self.frame_resultado_final, bg="white")
        self.frame_botones_finales.pack(pady=10)
        
        self.boton_reiniciar = tk.Button(self.frame_botones_finales, text="Reiniciar Test", command=self.reiniciar_test, font=self.button_font, bg="#2196F3", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.boton_reiniciar.pack(side=tk.LEFT, padx=10)
        
        self.boton_cerrar = tk.Button(self.frame_botones_finales, text="Cerrar", command=self.root.quit, font=self.button_font, bg="#F44336", fg="white", relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.boton_cerrar.pack(side=tk.LEFT, padx=10)
    
    def reiniciar_test(self):
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        
        random.shuffle(self.imagenes_descargadas)
        
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_errores.config(text=f"Errores: {self.errores}")
        
        self.frame_resultado_final.pack_forget()
        self.frame_imagen.pack(pady=20)
        self.frame_interaccion.pack(pady=10)
        self.label_resultado.pack(pady=10)
        self.label_temporizador.pack(pady=5)
        self.frame_contadores.pack(pady=10)
        self.label_progreso.pack(pady=(10, 20))

        self.mostrar_imagen()

# Crear la ventana principal
root = tk.Tk()
app = IshiharaTestApp(root)
root.mainloop()