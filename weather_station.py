import RPi.GPIO as GPIO
import dht11
import I2C_LCD_driver
import time
import requests
import unidecode

mylcd = I2C_LCD_driver.lcd()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
mode_state = 0

def get_localisation():
  r = requests.get('https://api.ipdata.co?api-key=test').json()
  city = r['city']
  city = unidecode.unidecode(city)
  return city

city = get_localisation()
  
def actual_weather():
  api_address='http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
  url = api_address + city
  json_data = requests.get(url).json()
  pressure = int(json_data['main']['pressure'])
  temperature = int(json_data['main']['temp'] - 273.15)
  humidity = int(json_data['main']['humidity'])
  wind = int(json_data['wind']['speed'])
  return pressure, temperature, humidity, wind
  
def mode_1():
  result = instance.read()
  mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 1)
  mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 2)
  
  if result.is_valid():
    mylcd.lcd_display_string("Temp: %d%s C" % (result.temperature, chr(223)), 3)
    mylcd.lcd_display_string("Humidity: %d %%" % result.humidity, 4)
    
def mode_2():
  pressure, temperature, humidity, wind = actual_weather()
  mylcd.lcd_display_string("Pressure: %d HPA" % (pressure), 1)
  mylcd.lcd_display_string("Temperature: %d%s C" % (temperature, chr(223)), 2)
  mylcd.lcd_display_string("Humidity: %d %%" % (humidity), 3)
  mylcd.lcd_display_string("Wind: %d km/h" % (wind), 4)
  time.sleep(4)
  

while True:
  input_state = GPIO.input(23)
  instance = dht11.DHT11(pin = 4)
  if input_state == False:
    if mode_state == 0:
      mylcd.lcd_clear()
      mode_state = 1
      print('Button Pressed')
      time.sleep(0.2)
    elif mode_state == 1:
      mylcd.lcd_clear()
      mode_state = 0
      print('Button Pressed')
      time.sleep(0.2)
  
  if mode_state == 0:
    mode_1()
  else:
    mode_2()

