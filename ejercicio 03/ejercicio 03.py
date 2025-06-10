#primero le decimos al usuario que ingrese un numero decimal
num=0
num=int(input("ingresa un numero en decimal: "))

#mostrar el numero en diferentes formas numericas (decimal,binario,hexadecimal)

print(f"Decimal: {num}")
print(f"Binario: {bin(num)}")
print(f"Hexadecimal: {hex(num).upper()}")
