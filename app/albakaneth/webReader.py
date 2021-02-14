import requests
import urllib.request
import time
import logging
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from ..initApi import start_api

url = 'https://www.albakeneth.gob.gt/boletines'
filename = 'temp.jpg'
history =  set()

lastHtml = ""
def save_image(image, api):
    res = requests.get(image, headers={'User-Agent': 'Chrome'}, stream=True)
    if res.status_code == 200:
        title = image.rfind('/')
        if title not in history:
            im = Image.open(BytesIO(res.content))
            crop_image(im)
            im.save(filename, quality=95)
            api.update_with_media(filename, status=message)



    pass

def crop_image(imageSource):
    im1 =  imageSource.crop((0, 500, 1785, 1750))
    date = imageSource.crop((1170,100,
                    1710,400))
    logo =  imageSource.crop((100, 1750, 1785/2, 2150))
    logo.thumbnail((600,700), Image.ANTIALIAS)
    print(im1.size)
    im1.thumbnail((1700,786), Image.ANTIALIAS)
    #date.thumbnail((100,400), Image.ANTIALIAS)
    newImage =  Image.new('RGB', (1700,786),(255,255,255,255))
    newImage.paste(im1, (-50,0))

    newImage.paste(logo, (1100,300))
    newImage.paste(date, (1100,10))
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
        lastHtml = soup
        for i in table:

            for l in i.find_all('img'):
                if l.has_key('src'):
                    save_image(l, api)
        del soup
                


    #pass

if __name__ == "__main__":

    readWebSite()
