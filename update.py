import requests
import csv
import urllib.parse
import configparser


def read_csv(dump='dump.csv'):
    """
    getCacheDump(dump):
        Obtiene el elemento del cache según la especificación de CSV
    """
    try:
        dumpstring = []
        with open(dump, mode='rt', encoding='utf-8') as archivo:
            for row in csv.reader(archivo, delimiter='|'):
                dumpstring.append(row[0])
        return sorted(dumpstring)
    except FileNotFoundError:
        return []


def write_csv(line, archivo='dump.csv', separador='|'):
    """
    printToCsv(archivo='dump.csv',delimeter=';',line):
    Imprime en archivo la linea, separada por separador como csv
    Jara (Asunción)|Avenida brasilia asuncion paraguay.jpg|<URL>
    """
    with open(archivo, mode='a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=separador)
        writer.writerow(line)
    return None


def get_data():
    payload = {'action': 'query', 'format': 'json', 'generator': 'categorymembers',
               'prop': 'imageinfo', 'iiprop': 'user|timestamp',
               'gcmtitle': 'Category:Images from Wiki Loves Earth 2018 in Chile', 'gcmtype': 'file',
               'gcmlimit': 'max', 'gcmsort': 'timestamp'}
    continuar = True

    lista = []
    while continuar == True:
        data = requests.get(
            'https://commons.wikipedia.org/w/api.php', payload)
        datas = data.json()
        lista += datas.get('query').get('pages').values()
        if datas.get('continue'):
            payload['cmcontinue'] = datas.get('continue').get('cmcontinue')
        else:
            continuar = False
        print ("Artículos... {0}".format(len(lista)))

    return lista


def convert_element(element):
    url = urllib.parse.quote(element.get('title'))
    element['url'] = 'https://commons.wikimedia.org/wiki/{0}'.format(url)
    element['titulo'] = element.get('title').replace('File:', '')
    element['autor'] = element.get('imageinfo')[0].get('user', '?')
    element['timestamp'] = element.get('imageinfo')[0].get('timestamp', '?')
    return element


def add_docs(element):
    payload = {'Nombre': element.get('title'), 'URL': element.get('url'),
               'Fecha': element.get('timestamp'), 'Autor': element.get('autor'),
               'Identificable': '',
               'Calidad': '', 'Derechos': '', 'Veredicto': '',
               'Revisor': '', 'Comentarios': ''}
    data = requests.get(url, payload)


def run_elements(lista):
    elements = read_csv()
    for el in lista:
        el = convert_element(el)
        if el.get('title') not in elements:
            print ('Añadiendo {0}'.format(el.get('title')))
            add_docs(el)
            write_csv([el.get('title')])


def main():
    lista = get_data()
    run_elements(lista)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['default']['url']
    main()
