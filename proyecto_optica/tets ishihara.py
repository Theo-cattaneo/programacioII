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
        self.root.geometry("800x750")
        self.root.configure(bg="#f0f0f0")
        
        # Configuración de fuentes
        self.title_font = font.Font(family="Arial", size=20, weight="bold")
        self.normal_font = font.Font(family="Arial", size=14)
        self.button_font = font.Font(family="Arial", size=12)
        self.result_font = font.Font(family="Arial", size=12, weight="bold")
        
        # Variables para el juego
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        
        # Datos de las imágenes (URL y respuesta correcta)
        self.imagenes = [
            {
                "url": "https://z-cdn-media.chatglm.cn/files/1a5c7ae0-dddf-4521-9f5a-6fd0b8d339ed_45.jpg?auth_key=1793024034-32e60631a7d44e25b9fc1cc97b90f45a-0-d9e94551954d1eab16a0ffeac53a433b",
                "respuesta": "45",
                "nombre": "45.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/ba042b7a-3d0e-4e94-b31f-dbf90bb96df3_74.jpg?auth_key=1793024034-d065bc43c16546d8b6e69d4f5734dfb5-0-0cbc7db1df4097d4eb969afef11e9f2b",
                "respuesta": "74",
                "nombre": "74.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/13cfcd70-d9be-4ee6-affa-0190f27a5c60_20.jpg?auth_key=1793024034-fa58c906e8744be488eedffa0f345546-0-5ab5e544c34e552f35bb3346dc3631ac",
                "respuesta": "20",  # Corregido: muestra el número 76 según la descripción
                "nombre": "20.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/91867a48-979b-48fb-94ed-b8d28c98908d_78.jpg?auth_key=1793024034-3fba2502242149f3a30342e01c329301-0-5df7422d788c14ab70ebfaa5042b92a8",
                "respuesta": "78",
                "nombre": "78.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/24ecf2c3-8c5c-49ac-bf1d-cefbf63387e9_8.jpg?auth_key=1793024034-335197524f654bcd8786a4ad5274bdec-0-b3a2c1cd55ca7ad9475f42550b3d2a95",
                "respuesta": "8",
                "nombre": "8.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/4089b402-c072-41ab-9421-858c5e489fe4_96.jpg?auth_key=1793024034-2aefac8cd1474d30ba5cf0f22ef35568-0-e9076100163405c097c18938b54e10f7",
                "respuesta": "96",  # Corregido: muestra el número 76 según la descripción
                "nombre": "96.jpg"
            },
            {
                "url": "https://z-cdn-media.chatglm.cn/files/f40ca8ff-aee2-4512-8c1f-78d3d5172475_42.jpg?auth_key=1793024034-5c2d84ccb41a4924ac1f94c96c1cb647-0-4d65a9b51c06b87ae77bf456c5515df1",
                "respuesta": "42",
                "nombre": "42.jpg"
            }
        ]
        
        # Mezclar las imágenes para que aparezcan en orden aleatorio
        random.shuffle(self.imagenes)
        
        # Descargar las imágenes
        self.imagenes_descargadas = []
        self.descargar_imagenes()
        
        # Crear los widgets de la interfaz
        self.crear_widgets()
        
        # Mostrar la primera imagen
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
                # Crear una imagen de error
                img = Image.new('RGB', (400, 400), color='white')
                photo = ImageTk.PhotoImage(img)
                self.imagenes_descargadas.append({
                    "photo": photo,
                    "respuesta": img_data["respuesta"],
                    "nombre": img_data["nombre"]
                })
    
    def crear_widgets(self):
        # Título
        self.titulo = tk.Label(
            self.root, 
            text="Test de Ishihara", 
            font=self.title_font,
            bg="#f0f0f0"
        )
        self.titulo.pack(pady=10)
        
        # Frame para la imagen
        self.frame_imagen = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_imagen.pack(pady=10)
        
        # Etiqueta para mostrar la imagen
        self.label_imagen = tk.Label(self.frame_imagen, bg="#f0f0f0")
        self.label_imagen.pack()
        
        # Frame para la respuesta
        self.frame_respuesta = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_respuesta.pack(pady=10)
        
        # Etiqueta para la pregunta
        self.label_pregunta = tk.Label(
            self.frame_respuesta, 
            text="¿Qué número ves en la imagen?", 
            font=self.normal_font,
            bg="#f0f0f0"
        )
        self.label_pregunta.pack(pady=5)
        
        # Campo de entrada para la respuesta
        self.entry_respuesta = tk.Entry(
            self.frame_respuesta, 
            font=self.normal_font,
            width=10
        )
        self.entry_respuesta.pack(pady=5)
        self.entry_respuesta.bind("<Return>", lambda event: self.verificar_respuesta())
        
        # Botón para verificar la respuesta
        self.boton_verificar = tk.Button(
            self.frame_respuesta, 
            text="Verificar", 
            command=self.verificar_respuesta,
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        self.boton_verificar.pack(pady=5)
        
        # Etiqueta para mostrar el resultado (en lugar de messagebox)
        self.label_resultado = tk.Label(
            self.root, 
            text="", 
            font=self.result_font,
            bg="#f0f0f0",
            height=2
        )
        self.label_resultado.pack(pady=5)
        
        # Frame para los contadores
        self.frame_contadores = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_contadores.pack(pady=10)
        
        # Contador de aciertos
        self.label_aciertos = tk.Label(
            self.frame_contadores, 
            text=f"Aciertos: {self.aciertos}", 
            font=self.normal_font,
            bg="#f0f0f0",
            fg="green"
        )
        self.label_aciertos.pack(side=tk.LEFT, padx=20)
        
        # Contador de errores
        self.label_errores = tk.Label(
            self.frame_contadores, 
            text=f"Errores: {self.errores}", 
            font=self.normal_font,
            bg="#f0f0f0",
            fg="red"
        )
        self.label_errores.pack(side=tk.LEFT, padx=20)
        
        # Etiqueta para mostrar el progreso
        self.label_progreso = tk.Label(
            self.root, 
            text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}", 
            font=self.normal_font,
            bg="#f0f0f0"
        )
        self.label_progreso.pack(pady=5)
    
    def mostrar_imagen(self):
        if self.imagen_actual < len(self.imagenes_descargadas):
            # Actualizar la imagen
            self.label_imagen.config(image=self.imagenes_descargadas[self.imagen_actual]["photo"])
            
            # Limpiar el campo de respuesta y el resultado
            self.entry_respuesta.delete(0, tk.END)
            self.entry_respuesta.focus()
            self.label_resultado.config(text="")
            
            # Actualizar el progreso
            self.label_progreso.config(text=f"Imagen {self.imagen_actual + 1} de {len(self.imagenes_descargadas)}")
        else:
            # Mostrar el resultado final
            self.mostrar_resultado_final()
    
    def verificar_respuesta(self):
        respuesta_usuario = self.entry_respuesta.get().strip()
        respuesta_correcta = self.imagenes_descargadas[self.imagen_actual]["respuesta"]
        
        if respuesta_usuario.lower() == respuesta_correcta.lower():
            self.aciertos += 1
            self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
            self.label_resultado.config(
                text="✓ ¡Correcto! Has acertado el número.", 
                fg="green"
            )
        else:
            self.errores += 1
            self.label_errores.config(text=f"Errores: {self.errores}")
            self.label_resultado.config(
                text=f"✗ Incorrecto. El número correcto era: {respuesta_correcta}", 
                fg="red"
            )
        
        # Deshabilitar el botón y el campo de entrada temporalmente
        self.boton_verificar.config(state=tk.DISABLED)
        self.entry_respuesta.config(state=tk.DISABLED)
        
        # Esperar 1.5 segundos antes de pasar a la siguiente imagen
        self.root.after(1500, self.siguiente_imagen)
    
    def siguiente_imagen(self):
        # Pasar a la siguiente imagen
        self.imagen_actual += 1
        
        # Rehabilitar el botón y el campo de entrada
        self.boton_verificar.config(state=tk.NORMAL)
        self.entry_respuesta.config(state=tk.NORMAL)
        
        # Mostrar la siguiente imagen
        self.mostrar_imagen()
    
    def mostrar_resultado_final(self):
        # Ocultar los widgets de respuesta
        self.frame_respuesta.pack_forget()
        self.frame_imagen.pack_forget()
        self.label_resultado.pack_forget()
        
        # Mostrar el resultado final
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
        
        self.label_resultado_final = tk.Label(
            self.root, 
            text=resultado_texto, 
            font=self.normal_font,
            bg="#f0f0f0",
            justify=tk.CENTER
        )
        self.label_resultado_final.pack(pady=20)
        
        # Frame para los botones finales
        self.frame_botones_finales = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_botones_finales.pack(pady=10)
        
        # Botón para reiniciar el test
        self.boton_reiniciar = tk.Button(
            self.frame_botones_finales, 
            text="Reiniciar Test", 
            command=self.reiniciar_test,
            font=self.button_font,
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        )
        self.boton_reiniciar.pack(side=tk.LEFT, padx=10)
        
        # Botón para cerrar la aplicación
        self.boton_cerrar = tk.Button(
            self.frame_botones_finales, 
            text="Cerrar", 
            command=self.root.quit,
            font=self.button_font,
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5
        )
        self.boton_cerrar.pack(side=tk.LEFT, padx=10)
    
    def reiniciar_test(self):
        # Restablecer las variables
        self.aciertos = 0
        self.errores = 0
        self.imagen_actual = 0
        
        # Mezclar las imágenes de nuevo
        random.shuffle(self.imagenes_descargadas)
        
        # Actualizar los contadores
        self.label_aciertos.config(text=f"Aciertos: {self.aciertos}")
        self.label_errores.config(text=f"Errores: {self.errores}")
        
        # Ocultar el resultado final
        self.label_resultado_final.pack_forget()
        self.frame_botones_finales.pack_forget()
        
        # Mostrar los widgets de respuesta
        self.frame_imagen.pack(pady=10)
        self.frame_respuesta.pack(pady=10)
        self.label_resultado.pack(pady=5)
        
        # Mostrar la primera imagen
        self.mostrar_imagen()

# Crear la ventana principal
root = tk.Tk()
app = IshiharaTestApp(root)
root.mainloop()