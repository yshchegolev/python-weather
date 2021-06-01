from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import requests
import json
import time
import os
import logging

BASE_URL = 'https://api.openweathermap.org/data/2.5/'
API_TOKEn = os.getenv('API_TOKEN')
CITY_NAME = os.getenv('CITY_NAME')
PUSH_GATEWAY = os.getenv('PUSH_GATEWAY')

def get_city_id():
    try:
        current_url = BASE_URL + 'find'
        response = requests.get(current_url, params={'q': CITY_NAME, 'appid':  API_TOKEn})
        json_response = json.loads(response.text)
        return json_response['list'][0]['id']
    except Exception as ex:
        logging.error(ex)
        pass

def get_weather(city_id):
    try:
        current_url = BASE_URL + 'weather'
        response = requests.get(current_url, params={'id': city_id, 'units': 'metric', 'appid': API_TOKEn})
        json_response = json.loads(response.text)
        return float(json_response['main']['temp'])
    except Exception as ex:
        logging.error(ex)
        pass

def push_temp(city_temp):
    job = CITY_NAME
    registry = CollectorRegistry()
    metric = Gauge(job, 'Temp in ' + CITY_NAME, registry=registry)
    metric.set(city_temp)
    push_to_gateway(PUSH_GATEWAY, job=job, registry=registry)
if __name__ == '__main__':
    while True:
        try:
            city_id = get_city_id()
            city_temp = get_weather(city_id)
            push_temp(city_temp)
            logging.info("Pushed %s", city_temp)
            time.sleep(10)
        except Exception as ex:
            logging.error(ex)
            continue