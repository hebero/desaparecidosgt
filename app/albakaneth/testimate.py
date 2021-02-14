from PIL.Image import new
import requests
import urllib.request
import time
import logging
from bs4 import BeautifulSoup
from PIL import Image

image1 = Image.open('/home/heber/Documentos/albakenetsample/Alba-Keneth | Buscar una alerta_files/1588-2020_Jose_Estuardo_Aguilar_Linares.jpg')
newImage  = Image.new('RGB', (1200,628), (250,250,250))
cropImage = image1.crop((100,500,100,1725))
cropImage.show()
newImage.paste(cropImage, (0,0))
newImage.save("merged_image.jpg","JPEG")
newImage.show()