import requests
import urllib.request
import time
import logging
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from initApi import start_api

url = 'https://www.albakeneth.gob.gt/boletines'
filename = 'temp.jpg'
logging.basicConfig(level=logging.INFO)
history =  set()
logger = logging.getLogger()
lastHtml = ""
def save_image(image, webInfo, api):
    res = requests.get(image, headers={'User-Agent': 'Chrome'}, stream=True)
    if res.status_code == 200:
        title = image.rfind('/')
        if title not in history:
            im = Image.open(BytesIO(res.content))
            crop = crop_image(im)
            crop.save(filename, quality=95)
            try:
                api.update_with_media(filename, status=f"#AlertaAlbaKeneth Ayuda a encontrar a esta persona compartiendo esta información: {webInfo}")
            except Exception as e:
                logger.error(e)

def crop_image(imageSource):
    im1 =  imageSource.crop((0, 500, 1785, 1750))
    date = imageSource.crop((1170,100,
                    1710,400))
    logo =  imageSource.crop((100, 1750, 1785/2, 2150))
    logo.thumbnail((350,450), Image.ANTIALIAS)
    print(im1.size)
    im1.thumbnail((1100,628), Image.ANTIALIAS)
    date.thumbnail((300,400), Image.ANTIALIAS)
    newImage =  Image.new('RGB', (1100,628),(255,255,255,255))
    newImage.paste(im1, (-50,0))

    newImage.paste(logo, (800,300))
    newImage.paste(date, (800,100))
    return newImage

def updateStatus(self, image):
    
    pass

def readWebSite():
    """
    read the website and extract the images
    """
    api = start_api()
    response = requests.get(url,headers={'User-Agent': 'Chrome'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('div',{'class':'col-lg-3 my-4 text-center'})
        for i in table:
            for l in i.find_all('img'):
                if l['src'].__contains__('.jpg'):
                    save_image(l['src'], l['alt'], api)
        del soup
                


    #pass

if __name__ == "__main__":

    readWebSite()

