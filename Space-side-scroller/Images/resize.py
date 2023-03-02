from PIL import Image

image = Image.open('Space-side-scroller/Images/enemy1.png')
new_image = image.resize((100, 100))
new_image = new_image.rotate(90)
new_image.save('Space-side-scroller/Images/enemy1_new.png')
