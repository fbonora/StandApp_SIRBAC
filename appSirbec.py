import csv
import json
import traceback

import image_collector

sirbac_url = 'https://www.dati.lombardia.it/resource/4mr7-hfsh.json'
sirbac_preview_url = 'http://www.bellalombardia.regione.lombardia.it/lbltext/?tipoVista=01&tipoRicerca=01&categoria=LDC%2CA1%2CA2%2CA3%2CA4%2CB%2CSA%2CSU&x=1103190.699&y=5726800.294&locale=en'
image_list = []


def get_json_data(url):
    # open with GET method
    import requests
    resp = requests.get(url)

    jsonData = json.loads(resp.content)
    return jsonData


def loadData(jsonList):
    with open('template.csv', 'r') as csv_colmuns_file:
        csv_columns_reader = csv.DictReader(csv_colmuns_file, delimiter="\t")
        print(csv_columns_reader.fieldnames)

        with open('convertedSirbac.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns_reader.fieldnames)
            writer.writeheader()
            for row in csv_columns_reader:
                if row['category'].find('church') > -1:
                    target = {'name': row['name'], 'city': row['addressMunicipalities'],
                              'province': row['addressProvince']}
                    image = get_image_from_set(target)
                    if image:
                        row['photo'] = image
                    else:
                        print('No image for: ' + row['name'] + ', ' + row['addressMunicipalities'])
                writer.writerow(row)


def remap_category(param):
    if param == 'Chiese e Abbazie':
        return 'church'
    if param == 'Capolavori' or param == 'Collezioni' or param == 'Apparati Decorativi':
        return 'art'
    if param == 'Musei':
        return 'museums'
    if param == 'Castelli e Fortificazioni' or param == 'Ville, palazzi e altri edifici civili' \
            or param == 'Cascine e Opere Rurali' or param == 'Architetture':
        return 'buildings'
    if param == 'Piazze e Borghi':
        return 'history'
    return param


def find_missing_image(param):
    import missingimages as mi
    for img in mi.missing_image_list:
        if param in img.keys():
            return img[param]
    return ''


def json_row_CSV(row):
    if 'categoria' in row:
        print(row)
        image = get_image_from_set(row)
        if image is None or image == '':
            print('No image for: ' + row['idbene'] + ', ' + row['comune'])

        category = remap_category(row['categoria'])
        if 'location' not in row:
            print('location not found for  ' + row['idbene'] + ' categoria ' + row['categoria'])
            image = image_collector.get_capolavoro_image(row)
            print(image)
        latitude = row['wgs84_x'] if 'wgs84_x' in row else ''
        longitude = row['wgs84_y'] if 'wgs84_y' in row else ''
        cap = row['cap'] if ('cap' in row.keys()) else ''
        website = row['website'] if 'website' in row else ''
        indirizzo = row['indirizzo'] if 'indirizzo' in row else ''
        denominazione = row['denominazione'] if 'denominazione' in row else ''
        abstract = row['abstract'] if 'abstract' in row else ''
        if indirizzo == '':
            indirizzo = row['comune'] if 'comune' in row else ''
        address_text = ' '.join([indirizzo, cap, row['siglaprovincia']])
        csv_row = {'category': category, 'name': denominazione, 'description': abstract,
                   'addressCap': cap, 'addressMunicipalities': row['comune'], 'addressProvince': row['siglaprovincia'],
                   'addressText': address_text, 'website': website,
                   'latitude': latitude, 'longitude': longitude, 'photo': image,
                   'visibleCopy': 'SIRBEC'}
        return csv_row


def jsonToCsv(jsonList):
    with open('template.csv', 'r') as csv_colmuns_file:
        csv_columns_reader = csv.DictReader(csv_colmuns_file, delimiter="\t")
        print(csv_columns_reader.fieldnames)

        with open('convertedSirbec.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns_reader.fieldnames)
            writer.writeheader()
            for row in jsonList:
                # print(row)
                csv_row = json_row_CSV(row)
                if csv_row is not None:
                    writer.writerow(csv_row)


def get_image_from_set(sirbac_entry):
    for el in image_list:
        if sirbac_entry.get('idbene') in el:
            return el[sirbac_entry.get('idbene')]
    print('Image not found for idbene: ' + sirbac_entry['idbene'])


if __name__ == "__main__":
    # Get all preview images from sirbec url
    #image_list = image_collector.get_preview_images(sirbac_preview_url)
    image_list = []

    # Get json data
    json_source = get_json_data(sirbac_url)

    # Generate CSV file
    try:
        jsonToCsv(json_source)
    except Exception as err:
        print("type error: " + str(err))
        print(traceback.format_exc())

