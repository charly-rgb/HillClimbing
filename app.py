from flask import Flask, jsonify, render_template
import math
import random

app = Flask(__name__)

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def hill_climbing():
    ruta = list(coord.keys())
    random.shuffle(ruta)
    mejora = True

    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta)
        for i in range(len(ruta)):
            for j in range(len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp)
                    if dist < dist_actual:
                        mejora = True
                        ruta = ruta_tmp
                        dist_actual = dist
                        break
            if mejora:
                break
    return ruta, evalua_ruta(ruta)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta-optima', methods=['GET'])
def obtener_ruta():
    ruta_optima, distancia_total = hill_climbing()
    coordenadas = [coord[ciudad] for ciudad in ruta_optima]
    return jsonify({
        'ruta': ruta_optima,
        'distancia_total': distancia_total,
        'coordenadas': coordenadas
    })

if __name__ == '__main__':
    app.run(debug=True)
