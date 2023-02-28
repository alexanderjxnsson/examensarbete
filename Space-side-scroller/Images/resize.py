from PIL import Image

image = Image.open('Space-side-scroller/Images/player.png')
new_image = image.resize((64, 81))
new_image.save('Space-side-scroller/Images/player_new.png')
