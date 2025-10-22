from PIL import Image

#Abrir la imagen y convertir a RGB
imagen = Image.open("edificio.jpg").convert("RGB")


# Crear imagen en escala de grises
ancho, alto = imagen.size
blancoNegro = Image.new("L", (ancho, alto)) # el "L" significa que va a se Blanco o Negro puro(1 bit por pixel) 

for x in range(ancho):
    for y in range(alto):
        r, g, b = imagen.getpixel((x, y))
        gris = int((r + g + b) / 3)
        blancoNegro.putpixel((x, y), gris)

# Rotar horizontalmente
blancoNegro_rotada = Image.new("L", (ancho, alto))
for x in range(ancho):
    for y in range(alto):
        
        #Copiamos el pixel del lado opuesto
        pixel = blancoNegro.getpixel((x, y))
        blancoNegro_rotada.putpixel((ancho - 1 - x, y), pixel)

# Mostrar la imagen en escala de grises y rotada
blancoNegro_rotada.show(title="Escala de grises y rotada horizontalmente")

