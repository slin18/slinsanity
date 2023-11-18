import requests
import pdb
import pandas as pd
import math
import cloudscraper
import json
import logging.config
import asyncio
import os
import time
from bs4 import BeautifulSoup

# TODO reinstall new version of cloudscraper if not working
logging.config.fileConfig(fname='logging.ini', disable_existing_loggers=False)
log = logging.getLogger('goat')


def get_silhouette_data(sneaker):
	num_results_per_page = 24
	# Phase 1: extraction
	# query search
	url = f"https://ac.cnstrc.com/search/{sneaker.replace(' ', '%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=6&page=1&num_results_per_page=24&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674417243092"
	# men
	# url = f"https://ac.cnstrc.com/browse/silhouette/{sneaker.replace(' ','%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=6&page=1&num_results_per_page=24&filters%5Bgender%5D=men&filters%5Bgroup_id%5D=sneakers&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674416500388"
	# men + gs
	# url = f"https://ac.cnstrc.com/browse/silhouette/{sneaker.replace(' ','%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=5&page=1&num_results_per_page=24&filters%5Bgroup_id%5D=sneakers&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674374940261"
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
	silhouette_results = []

	try:
		log.info(f'EXTRACTION BEGIN\nFirst attempt of getting silhouette data for "{sneaker}"')
		response = requests.get(url=url, headers=headers)
		if response.ok:
			total_num_results = response.json()["response"]["total_num_results"]
			results = response.json()["response"]["results"]
			silhouette_results.extend(results)
		else:
			error = f'Error when retrieving silhouette data for "{sneaker}": {response.text}'
			log.error(error)
			raise Exception(error)
	except Exception as ex:
		error = f'Error when retrieving silhouette data for "{sneaker}": {ex}'
		log.error(error)
		raise Exception(error)

	pages = math.ceil(total_num_results/num_results_per_page) + 1
	if pages > 1:
		log.info(f'Getting silhouette data by scraping more {pages-1} pages for "{sneaker}"')
		for i in range(2, pages):
			page_num = i
			# query search
			url = f"https://ac.cnstrc.com/search/{sneaker.replace(' ', '%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=6&page={page_num}&num_results_per_page=24&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674417243092"
			# men
			# url = f"https://ac.cnstrc.com/browse/silhouette/{sneaker.replace(' ', '%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=6&page={page_num}&num_results_per_page={num_results_per_page}&filters%5Bgender%5D=men&filters%5Bgroup_id%5D=sneakers&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674416500388"
			# men + gs
			# url = f"https://ac.cnstrc.com/browse/silhouette/{sneaker.replace(' ', '%20')}?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=491d301a-38f2-4539-9191-765a076eb1ad&s=4&page={page_num}&num_results_per_page={num_results_per_page}&filters%5Bgroup_id%5D=sneakers&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1674367612171"
			try:
				response = requests.get(url=url, headers=headers)
				if response.ok:
					results = response.json()["response"]["results"]
					silhouette_results.extend(results)
				else:
					error = f'Error when retrieving silhouette data for {sneaker}: {response.text}'
					log.error(error)
					raise Exception(error)
			except Exception as ex:
				error = f'Error when retrieving silhouette data for {sneaker}: {ex}'
				log.error(error)
				raise Exception(error)

	log.info("EXTRACTION COMPLETED")

	# Phase 2: transformation
	df = pd.DataFrame(silhouette_results)
	# pdb.set_trace()
	# you can create your own schema definition
	# however, you never know if the schema changes
	for key in df['data'][0]:
		if '_cents' not in key:
			df[key] = df['data'].apply(lambda s: s[key] if key in s else "")

	cols = ['data', 'matched_terms', 'labels']
	df.drop(cols, axis=1, inplace=True)
	# df['silhouette'] = sneaker
	df['goat_url'] = df['slug'].apply(lambda s: "https://www.goat.com/sneakers/" + s)

	return df


def get_sneaker_data(goat_urls, sneaker):
	results = []
	output_path = f'{sneaker}-sneaker-data.csv'
	session = cloudscraper.create_scraper()
	for i, url in enumerate(goat_urls):
		print(i, url)
		for __ in range(3):
			response = session.get(url)
			response_html = BeautifulSoup(response.text, "html.parser")
			if response_html:
				# pdb.set_trace()
				break
			else:
				time.sleep(5)
				continue

		try:
			data = json.loads("".join(response_html.find("script", {"type": "application/ld+json"}).contents))
			data.pop('offers', None)
			data['brand'] = data['brand'].get('name')
			data['goat_url'] = url
			results.append(data)
		except Exception as ex:
			if 'story' in json.loads("".join(response_html.find("script", {'id': '__NEXT_DATA__',
																		   'type': 'application/json'}).contents))['props']['pageProps']['productTemplate']:
				story = json.loads("".join(response_html.find("script", {'id': '__NEXT_DATA__',
																		   'type': 'application/json'}).contents))['props']['pageProps']['productTemplate']['story']
			else:
				story = 'N/A'
			data = {
				'@context': 'http://schema.org',
				'@type': 'N/A',
				'name': 'N/A',
				'image': ['N/A'],
				'releaseDate': 'N/A',
				'brand': 'N/A',
				'model': 'N/A',
				'sku': 'N/A',
				'color': 'N/A',
				'description': response_html.find("meta", {"name": "description"})['content'],
				'goat_url': url,
				'story': story
			}
			results.append(data)

		if i % 50 == 0:
			pd.DataFrame(results).to_csv(output_path, index=False, mode='a', header=not os.path.exists(output_path))
			results = []

	pd.DataFrame(results).to_csv(output_path, index=False, mode='a', header=not os.path.exists(output_path))
	return results


if __name__ == "__main__":
	sneaker = 'kobe'
	# for sneaker in sneakers:
	# df = get_silhouette_data(sneaker)
	# Phase 3: Load
	file_name = f"{sneaker.replace(' ', '-')}-silhouette-data.csv"
	# df.to_csv(file_name, index=False)

	# TODO async
	df = pd.read_csv(file_name)
	goat_urls = df['goat_url'].values
	get_sneaker_data(goat_urls, sneaker)