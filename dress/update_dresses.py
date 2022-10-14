from database.get_mongodb import get_mongodb
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pandas as pd
import numpy as np
import sys


def update_dresses():
    dresses = get_mongodb().dresses.objects
    dresses.drop()

    end_of_url = ['', ]
    for i in range(2, 25):
        end_of_url.append(f'?from={i}')
    image_links = []
    im = []
    for ending in end_of_url:
        url = f'https://www.apart.ru/odezhda/platya{ending}'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        data = soup.find('div', attrs={'class': 'list'})
        imgs = data.find_all('img')
        image_links.append([f"https://www.apart.ru{each.get('src')}" for each in imgs])
    image_links_flatten = [img for sublist in image_links for img in sublist]
    im = [Image.open(requests.get(img_lnk, stream=True).raw) for img_lnk in image_links_flatten[1::2]]

    # save this in table!!!!
    start_sizes = {}
    i = 1
    for img in im:
        start_sizes[i] = img.size
        i += 1
    df_start_size = pd.DataFrame(start_sizes).transpose().reset_index(drop=True)

    im_array = np.array([np.asarray(img.resize((280, 404))).flatten() for img in im], dtype=int)
    df_im = pd.DataFrame(im_array, dtype=int)
    df_im.index += 1
    for i in range(1, im_array.shape[0] + 1):
        dresses.insert_one({'id': f'{i}',
                            'values': f'{list(df_im.loc[i].values)}'})

    sys.stdout.write(
            "Successfully updated mongo dresses table with %d objects."
            % int(dresses.count_documents({}))
    )

