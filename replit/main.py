from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

cities = {
    'РјРѕСЃРєРІР°': ['1540737/daa6e420d33102bf6947', '213044/7df73ae4cc715175059e'],
    'РЅСЊСЋ-Р№РѕСЂРє': ['1652229/728d5c86707054d4745f', '1030494/aca7ed7acefde2606bdc'],
    'РїР°СЂРёР¶': ["1652229/f77136c2364eb90a3ea8", '123494/aca7ed7acefd12e606bdc']
}

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'РџСЂРёРІРµС‚! РќР°Р·РѕРІРё СЃРІРѕС‘ РёРјСЏ!'
        sessionStorage[user_id] = {
            'first_name': None,  # Р·РґРµСЃСЊ Р±СѓРґРµС‚ С…СЂР°РЅРёС‚СЊСЃСЏ РёРјСЏ
            'game_started': False  # Р·РґРµСЃСЊ РёРЅС„РѕСЂРјР°С†РёСЏ Рѕ С‚РѕРј, С‡С‚Рѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РЅР°С‡Р°Р» РёРіСЂСѓ. РџРѕ СѓРјРѕР»С‡Р°РЅРёСЋ False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'РќРµ СЂР°СЃСЃР»С‹С€Р°Р»Р° РёРјСЏ. РџРѕРІС‚РѕСЂРё, РїРѕР¶Р°Р»СѓР№СЃС‚Р°!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            # СЃРѕР·РґР°С‘Рј РїСѓСЃС‚РѕР№ РјР°СЃСЃРёРІ, РІ РєРѕС‚РѕСЂС‹Р№ Р±СѓРґРµРј Р·Р°РїРёСЃС‹РІР°С‚СЊ РіРѕСЂРѕРґР°, РєРѕС‚РѕСЂС‹Рµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ СѓР¶Рµ РѕС‚РіР°РґР°Р»
            sessionStorage[user_id]['guessed_cities'] = []
            # РєР°Рє РІРёРґРЅРѕ РёР· РїСЂРµРґС‹РґСѓС‰РµРіРѕ РЅР°РІС‹РєР°, СЃСЋРґР° РјС‹ РїРѕРїР°Р»Рё, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РЅР°РїРёСЃР°Р» СЃРІРѕРµРј РёРјСЏ.
            # РџСЂРµРґР»Р°РіР°РµРј РµРјСѓ СЃС‹РіСЂР°С‚СЊ Рё РґРІР° РІР°СЂРёР°РЅС‚Р° РѕС‚РІРµС‚Р° "Р”Р°" Рё "РќРµС‚".
            res['response']['text'] = f'РџСЂРёСЏС‚РЅРѕ РїРѕР·РЅР°РєРѕРјРёС‚СЊСЃСЏ, {first_name.title()}. РЇ РђР»РёСЃР°. РћС‚РіР°РґР°РµС€СЊ РіРѕСЂРѕРґ РїРѕ С„РѕС‚Рѕ?'
            res['response']['buttons'] = [
                {
                    'title': 'Р”Р°',
                    'hide': True
                },
                {
                    'title': 'РќРµС‚',
                    'hide': True
                }
            ]
    else:
        # РЈ РЅР°СЃ СѓР¶Рµ РµСЃС‚СЊ РёРјСЏ, Рё С‚РµРїРµСЂСЊ РјС‹ РѕР¶РёРґР°РµРј РѕС‚РІРµС‚ РЅР° РїСЂРµРґР»РѕР¶РµРЅРёРµ СЃС‹РіСЂР°С‚СЊ.
        # Р’ sessionStorage[user_id]['game_started'] С…СЂР°РЅРёС‚СЃСЏ True РёР»Рё False РІ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ С‚РѕРіРѕ,
        # РЅР°С‡Р°Р» РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ РёРіСЂСѓ РёР»Рё РЅРµС‚.
        if not sessionStorage[user_id]['game_started']:
            # РёРіСЂР° РЅРµ РЅР°С‡Р°С‚Р°, Р·РЅР°С‡РёС‚ РјС‹ РѕР¶РёРґР°РµРј РѕС‚РІРµС‚ РЅР° РїСЂРµРґР»РѕР¶РµРЅРёРµ СЃС‹РіСЂР°С‚СЊ.
            if 'РґР°' in req['request']['nlu']['tokens']:
                # РµСЃР»Рё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ СЃРѕРіР»Р°СЃРµРЅ, С‚Рѕ РїСЂРѕРІРµСЂСЏРµРј РЅРµ РѕС‚РіР°РґР°Р» Р»Рё РѕРЅ СѓР¶Рµ РІСЃРµ РіРѕСЂРѕРґР°.
                # РџРѕ СЃС…РµРјРµ РјРѕР¶РЅРѕ СѓРІРёРґРµС‚СЊ, С‡С‚Рѕ Р·РґРµСЃСЊ РѕРєР°Р¶СѓС‚СЃСЏ Рё РїРѕР»СЊР·РѕРІР°С‚РµР»Рё, РєРѕС‚РѕСЂС‹Рµ СѓР¶Рµ РѕС‚РіР°РґС‹РІР°Р»Рё РіРѕСЂРѕРґР°
                if len(sessionStorage[user_id]['guessed_cities']) == 3:
                    # РµСЃР»Рё РІСЃРµ С‚СЂРё РіРѕСЂРѕРґР° РѕС‚РіР°РґР°РЅС‹, С‚Рѕ Р·Р°РєР°РЅС‡РёРІР°РµРј РёРіСЂСѓ
                    res['response']['text'] = 'РўС‹ РѕС‚РіР°РґР°Р» РІСЃРµ РіРѕСЂРѕРґР°!'
                    res['end_session'] = True
                else:
                    # РµСЃР»Рё РµСЃС‚СЊ РЅРµРѕС‚РіР°РґР°РЅРЅС‹Рµ РіРѕСЂРѕРґР°, С‚Рѕ РїСЂРѕРґРѕР»Р¶Р°РµРј РёРіСЂСѓ
                    sessionStorage[user_id]['game_started'] = True
                    # РЅРѕРјРµСЂ РїРѕРїС‹С‚РєРё, С‡С‚РѕР±С‹ РїРѕРєР°Р·С‹РІР°С‚СЊ С„РѕС‚Рѕ РїРѕ РїРѕСЂСЏРґРєСѓ
                    sessionStorage[user_id]['attempt'] = 1
                    # С„СѓРЅРєС†РёСЏ, РєРѕС‚РѕСЂР°СЏ РІС‹Р±РёСЂР°РµС‚ РіРѕСЂРѕРґ РґР»СЏ РёРіСЂС‹ Рё РїРѕРєР°Р·С‹РІР°РµС‚ С„РѕС‚Рѕ
                    play_game(res, req)
            elif 'РЅРµС‚' in req['request']['nlu']['tokens']:
                res['response']['text'] = 'РќСѓ Рё Р»Р°РґРЅРѕ!'
                res['end_session'] = True
            else:
                res['response']['text'] = 'РќРµ РїРѕРЅСЏР»Р° РѕС‚РІРµС‚Р°! РўР°Рє РґР° РёР»Рё РЅРµС‚?'
                res['response']['buttons'] = [
                    {
                        'title': 'Р”Р°',
                        'hide': True
                    },
                    {
                        'title': 'РќРµС‚',
                        'hide': True
                    }
                ]
        else:
            play_game(res, req)


def play_game(res, req):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        # РµСЃР»Рё РїРѕРїС‹С‚РєР° РїРµСЂРІР°СЏ, С‚Рѕ СЃР»СѓС‡Р°Р№РЅС‹Рј РѕР±СЂР°Р·РѕРј РІС‹Р±РёСЂР°РµРј РіРѕСЂРѕРґ РґР»СЏ РіР°РґР°РЅРёСЏ
        city = random.choice(list(cities))
        # РІС‹Р±РёСЂР°РµРј РµРіРѕ РґРѕ С‚РµС… РїРѕСЂ РїРѕРєР° РЅРµ РІС‹Р±РёСЂР°РµРј РіРѕСЂРѕРґ, РєРѕС‚РѕСЂРѕРіРѕ РЅРµС‚ РІ sessionStorage[user_id]['guessed_cities']
        while city in sessionStorage[user_id]['guessed_cities']:
            city = random.choice(list(cities))
        # Р·Р°РїРёСЃС‹РІР°РµРј РіРѕСЂРѕРґ РІ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ РїРѕР»СЊР·РѕРІР°С‚РµР»Рµ
        sessionStorage[user_id]['city'] = city
        # РґРѕР±Р°РІР»СЏРµРј РІ РѕС‚РІРµС‚ РєР°СЂС‚РёРЅРєСѓ
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Р§С‚Рѕ СЌС‚Рѕ Р·Р° РіРѕСЂРѕРґ?'
        res['response']['card']['image_id'] = cities[city][attempt - 1]
        res['response']['text'] = 'РўРѕРіРґР° СЃС‹РіСЂР°РµРј!'
    else:
        # СЃСЋРґР° РїРѕРїР°РґР°РµРј, РµСЃР»Рё РїРѕРїС‹С‚РєР° РѕС‚РіР°РґР°С‚СЊ РЅРµ РїРµСЂРІР°СЏ
        city = sessionStorage[user_id]['city']
        # РїСЂРѕРІРµСЂСЏРµРј РµСЃС‚СЊ Р»Рё РїСЂР°РІРёР»СЊРЅС‹Р№ РѕС‚РІРµС‚ РІ СЃРѕРѕР±С‰РµРЅРёРµ
        if get_city(req) == city:
            # РµСЃР»Рё РґР°, С‚Рѕ РґРѕР±Р°РІР»СЏРµРј РіРѕСЂРѕРґ Рє sessionStorage[user_id]['guessed_cities'] Рё
            # РѕС‚РїСЂР°РІР»СЏРµРј РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ РЅР° РІС‚РѕСЂРѕР№ РєСЂСѓРі. РћР±СЂР°С‚РёС‚Рµ РІРЅРёРјР°РЅРёРµ РЅР° СЌС‚РѕС‚ С€Р°Рі РЅР° СЃС…РµРјРµ.
            res['response']['text'] = 'РџСЂР°РІРёР»СЊРЅРѕ! РЎС‹РіСЂР°РµРј РµС‰С‘?'
            sessionStorage[user_id]['guessed_cities'].append(city)
            sessionStorage[user_id]['game_started'] = False
            return
        else:
            # РµСЃР»Рё РЅРµС‚
            if attempt == 3:
                # РµСЃР»Рё РїРѕРїС‹С‚РєР° С‚СЂРµС‚СЊСЏ, С‚Рѕ Р·РЅР°С‡РёС‚, С‡С‚Рѕ РІСЃРµ РєР°СЂС‚РёРЅРєРё РјС‹ РїРѕРєР°Р·Р°Р»Рё.
                # Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ РіРѕРІРѕСЂРёРј РѕС‚РІРµС‚ РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ,
                # РґРѕР±Р°РІР»СЏРµРј РіРѕСЂРѕРґ Рє sessionStorage[user_id]['guessed_cities'] Рё РѕС‚РїСЂР°РІР»СЏРµРј РµРіРѕ РЅР° РІС‚РѕСЂРѕР№ РєСЂСѓРі.
                # РћР±СЂР°С‚РёС‚Рµ РІРЅРёРјР°РЅРёРµ РЅР° СЌС‚РѕС‚ С€Р°Рі РЅР° СЃС…РµРјРµ.
                res['response']['text'] = f'Р’С‹ РїС‹С‚Р°Р»РёСЃСЊ. Р­С‚Рѕ {city.title()}. РЎС‹РіСЂР°РµРј РµС‰С‘?'
                sessionStorage[user_id]['game_started'] = False
                sessionStorage[user_id]['guessed_cities'].append(city)
                return
            else:
                # РёРЅР°С‡Рµ РїРѕРєР°Р·С‹РІР°РµРј СЃР»РµРґСѓСЋС‰СѓСЋ РєР°СЂС‚РёРЅРєСѓ
                res['response']['card'] = {}
                res['response']['card']['type'] = 'BigImage'
                res['response']['card']['title'] = 'РќРµРїСЂР°РІРёР»СЊРЅРѕ. Р’РѕС‚ С‚РµР±Рµ РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅРѕРµ С„РѕС‚Рѕ'
                res['response']['card']['image_id'] = cities[city][attempt - 1]
                res['response']['text'] = 'Рђ РІРѕС‚ Рё РЅРµ СѓРіР°РґР°Р»!'
    # СѓРІРµР»РёС‡РёРІР°РµРј РЅРѕРјРµСЂ РїРѕРїС‹С‚РєРё РґРѕР»СЏ СЃР»РµРґСѓСЋС‰РµРіРѕ С€Р°РіР°
    sessionStorage[user_id]['attempt'] += 1


def get_city(req):
    # РїРµСЂРµР±РёСЂР°РµРј РёРјРµРЅРѕРІР°РЅРЅС‹Рµ СЃСѓС‰РЅРѕСЃС‚Рё
    for entity in req['request']['nlu']['entities']:
        # РµСЃР»Рё С‚РёРї YANDEX.GEO, С‚Рѕ РїС‹С‚Р°РµРјСЃСЏ РїРѕР»СѓС‡РёС‚СЊ РіРѕСЂРѕРґ(city), РµСЃР»Рё РЅРµС‚, С‚Рѕ РІРѕР·РІСЂР°С‰Р°РµРј None
        if entity['type'] == 'YANDEX.GEO':
            # РІРѕР·РІСЂР°С‰Р°РµРј None, РµСЃР»Рё РЅРµ РЅР°С€Р»Рё СЃСѓС‰РЅРѕСЃС‚Рё СЃ С‚РёРїРѕРј YANDEX.GEO
            return entity['value'].get('city', None)


def get_first_name(req):
    # РїРµСЂРµР±РёСЂР°РµРј СЃСѓС‰РЅРѕСЃС‚Рё
    for entity in req['request']['nlu']['entities']:
        # РЅР°С…РѕРґРёРј СЃСѓС‰РЅРѕСЃС‚СЊ СЃ С‚РёРїРѕРј 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Р•СЃР»Рё РµСЃС‚СЊ СЃСѓС‰РЅРѕСЃС‚СЊ СЃ РєР»СЋС‡РѕРј 'first_name', С‚Рѕ РІРѕР·РІСЂР°С‰Р°РµРј РµС‘ Р·РЅР°С‡РµРЅРёРµ.
            # Р’Рѕ РІСЃРµС… РѕСЃС‚Р°Р»СЊРЅС‹С… СЃР»СѓС‡Р°СЏС… РІРѕР·РІСЂР°С‰Р°РµРј None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()