import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from service.class_singleton import Singleton


class LoadDresses(Singleton):
    def __init__(self):
        self.im_array = None
        self.image_links = []

    def load(self):
        if not self.image_links:
            end_of_url = ['', ]
            for i in range(2, 25):
                end_of_url.append(f'?from={i}')
            for ending in end_of_url:
                url = f'https://www.apart.ru/odezhda/platya{ending}'
                print(url)
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                data = soup.find('div', attrs={'class': 'list'})
                imgs = data.find_all('img')
                self.image_links.append([f"https://www.apart.ru{each.get('src')}" for each in imgs])
            image_links_flatten = [img for sublist in self.image_links for img in sublist]
            im = [Image.open(requests.get(img_lnk, stream=True).raw) for img_lnk in image_links_flatten[1::2]]
            self.im_array = np.array([np.asarray(img.resize((280, 404))).flatten() for img in im])
            print('Done')
