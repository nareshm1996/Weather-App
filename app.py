from flask import Flask, request, jsonify, render_template, redirect
from requests import get
import json, folium

app = Flask(__name__)

weather_api_key = 'f797d0710db4ddfb926fdc08cb666a58'
ipinfo = get('https://ipinfo.io/').text

data = json.loads(ipinfo)

ip = data['ip']

city = data['city']
region = data['region']
country = data['country']
timezone = data['timezone']
latlong = data['loc'].split(',')

openweathermap = get(f'http://api.openweathermap.org/data/2.5/weather?lat={latlong[0]}&lon={latlong[1]}&appid={weather_api_key}').text
weather = json.loads(openweathermap)

climate = weather['weather'][0]['main']
wind_speed = weather['wind']['speed']
wind_degree = weather['wind']['deg']
humidity = weather['main']['humidity']

@app.route('/', methods=['GET'])
def main():
    return redirect('/app')

@app.route('/app')
def weather():
    return render_template('app.html', ip=ip, city=city, country_code=country, lat=latlong[0], long=latlong[1], climate=climate, wind_speed=wind_speed, wind_degree=wind_degree, humidity=humidity)


@app.route('/map')
def map():
    map = folium.Map(
        location=[latlong[0], latlong[1]],
        width='100%',
        height='50%',
        no_touch=True
    )
    folium.Marker(
        location=[latlong[0], latlong[1]],
        tooltip='You are here!'
    ).add_to(map)
    return map._repr_html_()

if __name__ == "__main__":
    app.run(debug='True')