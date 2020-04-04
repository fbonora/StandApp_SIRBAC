import csv
import sys
from pykml import parser

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def loadData(file):
    with open('template.csv','r') as csv_colmuns_file:
        csv_columns_reader = csv.DictReader(csv_colmuns_file, delimiter="\t")
        print(csv_columns_reader.fieldnames)
        photoLink = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Infinito.jpg/290px-Infinito.jpg'

        with open('converted.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns_reader.fieldnames)
            writer.writeheader()
            with open(file,'r',encoding="UTF-8") as file_kml:
                kml_parser = parser.parse(file_kml)
                root = kml_parser.getroot()
                print(root.Document.Folder.Placemark)
                for folder in root.Document.Folder:
                    print("Folder: " + folder.name)
                    for p in folder.Placemark:
                        descritipn_with_html = p.description.text
                        description = remove_html_tags(descritipn_with_html)
                        latitude = p.Point.coordinates.text.split(',')[0].replace('\n', '')
                        latitude = latitude.replace(' ', '')
                        longitude = p.Point.coordinates.text.split(',')[1]
                        writer.writerow({'category': 'literature', 'name': p.name, 'description': description,'latitude': latitude,'longitude': longitude, 'photo': photoLink})


if __name__ == "__main__":
    file_to_load = sys.argv[1]
    loadData(file_to_load)