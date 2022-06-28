from flask import Flask, jsonify, request
import requests
from datetime import datetime
import hashlib
import json

app =  Flask(__name__)
def getDate(dates):
    onsaleDate = ''
    for date in dates:
        if date['type'] == 'onsaleDate':
            onsaleDate = date['date']
    return onsaleDate

@app.route('/searchComics/', methods = ['GET'])
def get_comics():
    #validar que tenga el filtro de comic
    titulo_filtro = request.args.get('titulo_comic')
    nombre_personaje = request.args.get('nombre_personaje')
    now = datetime.now()
    ts = now.strftime("%m%d%Y%H%M%S")
    cpb = 'c1d13a3edb994f0731e0a3d38b032a4d'
    cpv = 'abe489414a3c3b1f0282f294d6452b6530422a51'
    hash = ts + cpv + cpb
    hash_encoded = hashlib.md5(hash.encode())
    try:
        if titulo_filtro is not None:
            print("Tiene filtro de titulo de comic.")
            url = 'http://gateway.marvel.com/v1/public/comics?titleStartsWith='+titulo_filtro+'&ts=' + ts + '&apikey=' + cpb + '&hash=' + hash_encoded.hexdigest()
            print(url)
            x = requests.get(
                'http://gateway.marvel.com/v1/public/comics?titleStartsWith=A&ts=' + ts + '&apikey=' + cpb + '&hash=' + hash_encoded.hexdigest())
            data = json.loads(x.content)
            comics = data['data']['results']
            response = []
            for item in comics:
                response.append({
                    "id": item['id'],
                    "title": item['title'],
                    "image": item['thumbnail']['path'] + '.' + item['thumbnail']['extension'],
                    "onsaleDate": getDate(item['dates'])
                })
            finalResponse = {
            "code": 200,
            "message": 'succes',
            "data": response
            }
            return jsonify(finalResponse)
        elif nombre_personaje is not None:
            print('Tiene filtro de nombre de personaje.')
            url = 'http://gateway.marvel.com/v1/public/characters?nameStartsWith=' + nombre_personaje + '&ts=' + ts + '&apikey=' + cpb + '&hash=' + hash_encoded.hexdigest()
            print(url)
            x = requests.get(url)
            data = json.loads(x.content)
            comics = data['data']['results']
            response = []
            for item in comics:
                response.append({
                    "id": item['id'],
                    "name": item['name'],
                    "image": item['thumbnail']['path'] + '.' + item['thumbnail']['extension'],
                    "appearances": item['comics']['available']
                })
            finalResponse = {
            "code": 200,
            "message": 'succes',
            "data": response
            }
            return jsonify(finalResponse)
        else:
            print('Sin filtros.')
            url = 'http://gateway.marvel.com/v1/public/characters?orderBy=name&ts=' + ts + '&apikey=' + cpb + '&hash=' + hash_encoded.hexdigest()
            print(url)
            x = requests.get(url)
            data = json.loads(x.content)
            comics = data['data']['results']
            response = []
            for item in comics:
                response.append({
                    "id": item['id'],
                    "name": item['name'],
                    "image": item['thumbnail']['path'] + '.' + item['thumbnail']['extension'],
                    "appearances": item['comics']['available']
                })
            finalResponse = {
            "code": 200,
            "message": 'succes',
            "data": response
            }
            return jsonify(finalResponse)
    except Exception as e:
        print(e)
        response = {
            "code": 500,
            "message": 'Error en la petición'
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 4000, debug = True)