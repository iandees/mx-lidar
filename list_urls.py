import re
import requests
import sys


url = "http://en.www.inegi.org.mx/app/api/productos/interna_v1/slcComponente/obtenCartasBuscador"
params = {
    "entidad": '',
    "municipio": '',
    "localidad": '',
    "tema": 'MAP0701000000',
    "escala": '1:10 000',
    "formato": '',
    "edicion": '',
    "clave": '',
    "buscador": '',
    "tipoB": 2,
    "orden": 4,
    "ordenDesc": 'true',
    "pagina": 0,
    "tamano": 100,
}
url_re = re.compile(r'href=\"(http://[0-9a-zA-Z_\.\/]*Terreno[0-9a-zA-Z_\.\/]*_b\.zip)\"')

sess = requests.Session()
sess.headers.update({'Accept': 'application/json'})


while True:
    resp = sess.get(url, params=params)
    sys.stderr.write("{} - {}\n".format(resp.status_code, resp.request.url))
    resp.raise_for_status()

    data = resp.json()

    results = data.get('mapas')

    if not results:
        break

    for result in results:
        matches = url_re.search(result['formatos'])
        if matches:
            sys.stdout.write(matches.group(1) + '\n')
    sys.stdout.flush()

    params['pagina'] += 1
