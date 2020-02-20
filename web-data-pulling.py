import os
from bs4 import BeautifulSoup
import urllib.request
import urllib
import json

species = {"src": [], "label_en": [], "label_latin": []}

url = "https://www.wood-database.com/wood-finder/?fwp_paged="

#woodfinder 37 pages
for k in range(37):
    print("Pulling page {}...".format(k))
    response = urllib.request.urlopen(url+str(k))
    html = response.read()
    soup = BeautifulSoup(html, "html5lib")

    #get images url with en and latin labels
    images = soup.find_all("img", {"class": "attachment-banner size-banner wp-post-image"})
    for image in images:
        src = image["src"]
        label_en = image.find_next("strong").text
        label_latin = image.find_next("em").text
        label_en = "".join([ c if (c.isalpha() or " ") else "" for c in label_en]).lower().strip(".,()")
        label_latin = "".join([ c if (c.isalpha() or " ") else "" for c in label_latin]).lower().strip(".,()")
        species["src"].append(src)
        species["label_en"].append(label_en)
        species["label_latin"].append(label_latin)

#download images
datadir_name = "databases"
database_name = "woodfinder"
os.makedirs(os.path.join(datadir_name, database_name), exist_ok=True)
metadata = {}

for i, src in enumerate(species["src"]):
    name = "{:09d}.jpg".format(i)
    print("{} Downloading: {}".format(i, src))
    urllib.request.urlretrieve(src, os.path.join(datadir_name, database_name, name))
    metadata[name] = {"en": species["label_en"][i], "latin": species["label_latin"][i]}

#write labels
with open(os.path.join(datadir_name, database_name, "data.json"), "w") as fp:
    json.dump(metadata, fp)

print("done.")
