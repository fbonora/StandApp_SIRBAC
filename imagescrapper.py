

def extractImages():
    with open('chiese_lombardia.html') as html:
        content = html.read()
        import lxml.html as LH

        allData = []
        root = LH.fromstring(content)
        for el in root.iter('img'):
            #print(el.attrib)
            if el.attrib['src'].find('jpg') > -1:
                if el.attrib['alt'].find(',') > -1:
                    imageData = el.attrib['alt'].split(',')
                    name = imageData[0]
                    city = imageData[1].split('(')[0].strip(' ')
                    province = imageData[1].split('(')[1].split(')')[0]
                    row = {'name': name, 'city': city, 'province': province, 'imageurl': el.attrib['src']}
                    allData.append(row)
        return allData

extractImages()
