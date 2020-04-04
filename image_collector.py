from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from time import sleep


def get_preview_images(url):
    if(url == ''):
        url ='http://www.bellalombardia.regione.lombardia.it/lbltext/?tipoVista=01&tipoRicerca=01&categoria=LDC%2CA1%2CA2%2CA3%2CA4%2CB%2CSA%2CSU&x=1103190.699&y=5726800.294&locale=en'

    html = get_html_source(url)

    # Create a BeautifulSoup object
    complete_soup = BeautifulSoup(html, 'html.parser')

    id_to_image_list = []
    div_elements = complete_soup.find_all('div', {'class': 'GK101NXDMIC'})
    for div_elem in div_elements:
        img = div_elem.find('img', {'class': 'gwt-Image'})
        id_to_image_list.append({div_elem.get('id'): img.get('src')})
    return id_to_image_list


def get_html_source(url):
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['marionette'] = False
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(1)  # Time in seconds
    html = driver.page_source
    driver.quit()
    return html


def get_capolavoro_image(json_row):
    site_url = 'http://www.bellalombardia.regione.lombardia.it/lbltext/?tipoVista=02&tipoRicerca=02&categoria=CAP&listaId='

    html = get_html_source(site_url + json_row.get('idbene'))
    complete_soup = BeautifulSoup(html, 'html.parser')
    img = complete_soup.find('img', {'class': 'slide-content', 'draggable': 'false'})
    return img.get('src') if img is not None else ''

#get_preview_images('')

