from PIL import Image

# importar la imagen
imagen = Image.open("edificio.jpg").convert("RGB")

# definir función para convertir a escala de grises
def convertir_a_gris(img):
    ancho, alto = img.size
    blanconegro = Image.new("L", (ancho, alto))  #crear imagen en escala de grises
    for x in range(ancho):
        for y in range(alto):
            r, g, b = img.getpixel((x, y))
            # Usar la fórmula proporcionada
            gris = int(r*0.2989 + g*0.5870 + b*0.1140)
            blanconegro.putpixel((x, y), gris)
    return blanconegro

# Convertir la imagen
imagen_gris = convertir_a_gris(imagen)

imagen_gris.show(title="Imagen en escala de grises")
