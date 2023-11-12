import urllib.request
import logging.config
import pandas as pd
import pyshorteners
import pdb

logging.config.fileConfig(fname='logging.ini', disable_existing_loggers=False)
log = logging.getLogger('image')


def download_image(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


def create_caption(data):
    short = pyshorteners.Shortener()
    # TODO change release date to mm-dd-yyyy or range format
    # TODO change description to get rid of authenticity
    # released =
    # description =
    model = data['model']
    google_search_url = short.tinyurl.short(f'https://www.google.com/search?q={model}')
    goat_search_url = short.tinyurl.short(f'{data["goat_url"]}')
    stockx_search_url = short.tinyurl.short(f'https://stockx.com/search?s={model}')
    ebay_search_url = short.tinyurl.short(f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={model.replace(' ','+')}")

    caption = f"""{data['model']} | SKU: {data['sku']} | Released: {data['release_date']}\n\n\n{data['description']}\n\n\nGoogle Search: {google_search_url}\nGOAT URL: {goat_search_url}\nStockX URL: {stockx_search_url}\nEbay URL: {ebay_search_url}\n.\n=> FOLLOW ME @slinsanity / @slinsanity_kicks FOR MORE CONTENT <=\n\n\n#kobe #kobeshoes #kobebryant #mamba #{data['brand']} #nba #basketball #lakers #kicks #sneakers #sneakerdictionary #{data['model_sub_line'].replace(' ','').replace('-','').lower()} #{data['model_line'].replace('-','').replace(' ','').lower()}"""

    with open(f"./results/kobe/caption/{data['slug']}.txt","w") as f:
        f.write(caption)


if __name__ == "__main__":
    sneaker = 'kobe'
    df = pd.read_csv(f'{sneaker}-final-data.csv')
    for i in range(len(df)):
        logging.info(f"{i}/{len(df)} slug: {df.iloc[i]['slug']} {df.iloc[i]['image_url']}")
        data = df.iloc[i]
        # TODO create the slug directory
        try:
            download_image(data['image_url'], f'results/{sneaker}/images/', data['slug'])
            create_caption(data)
        except Exception as e:
            logging.error(e)
            continue
