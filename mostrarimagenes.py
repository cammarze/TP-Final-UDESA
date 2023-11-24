import matplotlib.pyplot as plt
import matplotlib.image as mpimg

im1 = 'cat.webp'
im2 = 'sex.jpg'
im3 = 'descarga.jpg'
im4 = 'kuchau.webp'

# lee las imagenes 
image1 = mpimg.imread(im1)
image2 = mpimg.imread(im2)
image3 = mpimg.imread(im3)
image4 = mpimg.imread(im4)


fig, axs = plt.subplots(2, 2) #crea cuadricula 2x2

#muestra las imágenes en cada uno de los subplots
axs[0, 0].imshow(image1) #fila 0, col 0, primer eje
axs[0, 0].set_title('Imagen 1')

axs[0, 1].imshow(image2)
axs[0, 1].set_title('Imagen 2')

axs[1, 0].imshow(image3) 
axs[1, 0].set_title('Imagen 3')

axs[1, 1].imshow(image4)
axs[1, 1].set_title('Imagen 4')

plt.tight_layout()

plt.show()
