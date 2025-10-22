from PIL import Image
opc=0
# Abrir la imagen
imagen = Image.open("paisaje.jpg")
imagen = imagen.convert("RGB")

ancho, alto = imagen.size  # dimensiones originales

print("Elige 1 si quieres rotar la imagen a 90°, 2 si la quieres a 180, 3 si la quieres a 90° pero al lado contrario")
opc=int(input())
if (opc==1):
    # Rotada a 90°
    rotada90 = Image.new("RGB", (alto, ancho))
    for x in range(ancho):
        for y in range(alto):
            pixel = imagen.getpixel((x, y))
            nuevo_x = y
            nuevo_y = ancho - 1 - x
            rotada90.putpixel((nuevo_x, nuevo_y), pixel)
            
    #muestra la imagen en 90°
    rotada90.show()
else:
    if (opc==2):
        #Rotada 180°
        rotada180 = Image.new("RGB", (ancho, alto))
        for x in range(ancho):
            for y in range(alto):
                pixel = imagen.getpixel((x, y))
                nuevo_x = ancho - 1 - x
                nuevo_y = alto - 1 - y
                rotada180.putpixel((nuevo_x, nuevo_y), pixel)
        # Mostrar imagen rotada 180°
        rotada180.show()
    
    if (opc==3):
        # Crear una nueva imagen vacía (invertimos dimensiones)
        rotada90_izq = Image.new("RGB", (alto, ancho))
        # Recorrer píxeles
        for x in range(ancho):
            for y in range(alto):
                pixel = imagen.getpixel((x, y))
                # Fórmula para girar a la izquierda (-90°)
                nuevo_x = alto - 1 - y
                nuevo_y = x
                
                rotada90_izq.putpixel((nuevo_x, nuevo_y), pixel)

    # Mostrar la imagen
    rotada90_izq.show()
