radio=0
altura=0
volumen=0

import math

radio=int(input("ingrese el radio de un circulo:"))

def areacirculo(radio):
    return math.pi*radio**2
print(areacirculo(radio),"es la area de tu circulo")

altura=int(input("ingrese la altura de su circulo"))
volumen=areacirculo(radio)*altura

print("el volument de tu cilindro es: ",volumen)
