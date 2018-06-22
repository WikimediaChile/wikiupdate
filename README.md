# Update
Este es un microscript que permite actualizar los datos de una categoría de Wikimedia Commons en un documento de Google Sheets, con el fin de hacer seguimiento o análisis de datos.

Para ejecutar se debe crear el archivo `config.ini` con los valores indicados en el archivo `config.ini.dist`. Al ejecutarse, se creará un archivo de `dump.csv` como memoria intermedia para evitar que se añada nuevamente un archivo va incluido en la lista de Google.

## Requisitos
* Python 3
* requests `pip3 install --user requests`

Algunas funciones son tomadas desde [lahitools](https://github.com/lahire/wiki-imagefinder) para simplificar el volcado de datos.

## Licencia
GPL (o GNU General Public License) para todos los efectos.
