from flask import Flask, request, jsonify
import logging
from random import choice
from waitress import serve
import os
from copy import deepcopy

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

cities = {
    'москва': ['1540737/daa6e420d33102bf6947', '213044/7df73ae4cc715175059e'],
    'нью-йорк': ['1652229/728d5c86707054d4745f', '1030494/aca7ed7acefde2606bdc'],
    'париж': ['1652229/f77136c2364eb90a3ea8', '3450494/aca7ed7acefde22341bdc']
}

sessionStorage = {}

last_response = []


@app.route('/')
def health_check():
    return ''


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return jsonify(response)


def handle_dialog(res, req):
    global last_response
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {'first_name': None}
        res['response']['text'] = 'Привет! Назови свое имя!'
        res['response']['buttons'] = [{'title': 'Помощь', 'hide': False}]  # кнопки пока пустые
        res['response']['end_session'] = False
        last_response = deepcopy(res)
        return

    if req['request']['command'].lower() == 'помощь':
        res['response']['text'] = 'Это игра "Угадай город". Я загадываю, вы - угадываете!'
        res['response']['buttons'] = last_response['response']['buttons'][:]

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Какой город хочешь увидеть?'
            res['response']['buttons'] = [{'title': city.title(), 'hide': True} for city in cities] + res['response'][
                'buttons']
            last_response = deepcopy(res)
        return

    city = get_city(req)
    if city in cities:
        res['response']['card'] = {
            'type': 'BigImage',
            'title': 'Этот город я знаю.',
            'image_id': choice(cities[city])
        }
        res['response']['text'] = 'Я угадал!'
    else:
        res['response']['text'] = 'Первый раз слышу об этом городе. Попробуй еще разок!'

    last_response = deepcopy(res)


def get_city(req):
    if req['request']['nlu']['entities']:
        for entity in req['request']['nlu']['entities']:
            if entity['type'] == 'YANDEX.GEO':
                return entity['value'].get('city', None)


def get_first_name(req):
    if req['request']['nlu']['entities']:
        for entity in req['request']['nlu']['entities']:
            if entity['type'] == 'YANDEX.FIO':
                return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    serve(app, host='0.0.0.0', port=port)
