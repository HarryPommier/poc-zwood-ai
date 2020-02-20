from PIL import Image, ImageOps
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt 
import os

SIZE = 400

datadir = "databases"
database_name = "woodfinder"
database_name_resized = database_name + "_resized"
os.makedirs(os.path.join(datadir, database_name_resized), exist_ok=True)

dirs, subdirs, files = os.walk(os.path.join(datadir, database_name)).__next__()
for name in files:
    if "json" not in name:
        image = Image.open(os.path.join(dirs, name))

        if image.mode in ('RGBA', 'LA'):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3]) # 3 is the alpha channel
            background = ImageOps.fit(background, (SIZE, SIZE), Image.ANTIALIAS)
            background.save(os.path.join(datadir, database_name_resized, name))
        else:
            resized_image = ImageOps.fit(image, (SIZE, SIZE), Image.ANTIALIAS)
            resized_image.save(os.path.join(datadir, database_name_resized, name))