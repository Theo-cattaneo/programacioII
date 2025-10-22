import tkinter as tk
from random import randint

# Ventana
app = tk.Tk()
app.geometry("400x500")
app.configure(bg="black")
app.title("Adivina el número")

# Variables
entrada = tk.StringVar(app)
salida = tk.StringVar(app)
vidas_sv = tk.StringVar(app)

secreto = randint(1, 20)  # Número secreto
vidas = 6
vidas_sv.set("Vidas: " + str(vidas))


def adivina():
    global vidas, secreto
    try:
        intento = int(entrada.get())
    except ValueError:
        salida.set("⚠️ Ingrese un número válido")
        return

    if intento < 1 or intento > 20:
        salida.set("❌ Error, ingrese un número del 1 al 20")
        return

    if intento == secreto:
        salida.set("🎉 ¡Felicidades, ganaste! 🎉")
    else:
        vidas -= 1
        vidas_sv.set("Vidas: " + str(vidas))
        if vidas == 0:
            salida.set(f"❌ Perdiste... El número era {secreto}")
        elif intento < secreto:
            salida.set("El número secreto es más grande 🔼")
        else:
            salida.set("El número secreto es más chico 🔽")


# Widgets
tk.Label(
    app,
    text="Adivina el número secreto (1 a 20)",
    bg="black",
    fg="white",
    font=("Arial", 14)
).pack(pady=10)

tk.Label(
    app,
    textvariable=vidas_sv,
    bg="black",
    fg="white",
    font=("Arial", 12)
).pack(pady=5)

tk.Entry(
    app,
    textvariable=entrada,
    font=("Arial", 12)
).pack(pady=10)

tk.Label(
    app,
    textvariable=salida,
    bg="black",
    fg="white",
    font=("Arial", 12)
).pack(pady=10)

tk.Button(
    app,
    text="Adivinar",
    command=adivina,
    font=("Arial", 12),
    bg="green",
    fg="white"
).pack(pady=20)

app.mainloop()
