# Weather-pusher
Simple python script to get weather from https://openweathermap.org/ API and push it to Prometheus

## How to use:
```
1. Clone this repo
2. pip install -r requirements.txt
3. Set enviroment variables:
   CITY_NAME - for example 'Tallinn'
   API_TOKEN - API token 
   PUSH_GATEWAY - for exaple '10.10.10.10:9091'
3. python weather.py 
```
