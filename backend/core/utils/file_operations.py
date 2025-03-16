from PIL import Image
from os import path,getcwd

def compress(image_file):
    # Add a function to check the file extension and typel
    filepath = path.join(getcwd(), image_file)
    # Rename the file with possibly a "compressed prefix" so the image does not get recompressed, Either that or move the file to a diferent category all together
    image = Image.open(filepath)
    image.save("image-file-compressed",
                 "JPEG",
                 optimize = True,
                 quality = 10)
    return


import time
while True:
    print(i)
    time.sleep(.01)