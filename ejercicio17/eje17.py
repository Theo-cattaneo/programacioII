from PIL import Image, ImageFilter

# Cargar imagen
img = Image.open("paisaje.jpg") 

#Definir kernel 3x3 de desenfoque promedio
kernel = [
    4, 0, 0,
    0, 1, 0,
    0, 0, -4
]

#Aplicar filtro de desenfoque
img_blur = img.filter(ImageFilter.Kernel(
    size=(3, 3),
    kernel=kernel,
    scale=None,
    offset=0
))

#Mostrar la imagen desenfocada en una ventana del sistema
img_blur.show(title="Imagen desenfocada")
