from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import requests
import json
import time
import os

base_url = 'https://api.openweathermap.org/data/2.5/'
api_token = os.getenv('API_TOKEN')
city_name = os.getenv('CITY_NAME')
push_gateway = os.getenv('PUSH_GATEWAY')

def get_city_id():
    try:
        current_url = base_url + 'find'
        response = requests.get(current_url, params={'q': city_name, 'appid':  api_token})
        json_response = json.loads(response.text)
        return json_response['list'][0]['id']
    except Exception as ex:
        print('Exception(city_id):', ex)
        pass

def get_weather(city_id):
    try:
        current_url = base_url + 'weather'
        response = requests.get(current_url, params={'id': city_id, 'units': 'metric', 'appid': api_token})
        json_response = json.loads(response.text)
        return float(json_response['main']['temp'])
    except Exception as ex:
        print('Exceptions(temp)', ex)
        pass

def push_temp(city_temp):
    job = city_name
    registry = CollectorRegistry()
    metric = Gauge(job, 'Temp in ' + city_name, registry=registry)
    metric.set(city_temp)
    push_to_gateway(push_gateway, job=job,  registry=registry)
if __name__ == '__main__':
    while True:
        try:
            city_id = get_city_id()
            city_temp = get_weather(city_id)
            push_temp(city_temp)
            print(city_temp)
            time.sleep(10)
        except Exception as ex:
            print(ex)
            continue