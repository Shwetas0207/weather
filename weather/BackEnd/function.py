from os.path import abspath, join, dirname
from sys import path

base_dir = abspath(join(dirname(__file__), "../"))
path.append(base_dir)

import requests
from sys import exc_info
import sqlite3
from datetime import datetime, timedelta
from jwt import decode, encode,DecodeError


def get_weather(city):
    try:
        api_key = '55e7de491ab01aab5138a5989a9489bc'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        res = requests.get(url)
        data = res.json()
        if data['cod'] == '404':
            return {'Error':'City not found.'}
        if data['cod'] == '401':
            return {'Error':'Invalid API key.'}
        if data['cod'] == '429':
            return {'Error':'API key has reached the maximum number of requests.'}
        if data['cod'] == '400':
            return {'Error':'Bad request.'}
        temperature_kelvin = data['main']['temp']
        temperature_celsius = round((temperature_kelvin - 273.15), 2)
        humidity = data['main']['humidity']
        name = data['name']
        return {'name':name,'temperature':temperature_celsius, 'humidity':humidity}
    except Exception as e:
        print(f'!ERROR!\nFile : xhgfh.py\nFunction : get_weather\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error':'An error occurred while fetching weather data.'}

def add_data(name, temperature, humidity):
    try:
        conn = sqlite3.connect('weather.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        temperature INTEGER,
                        humidity INTEGER
                    )''')
        cur.execute("SELECT id FROM weather WHERE name=?", (name,))
        existing_record = cur.fetchone()
        if existing_record:
            conn.close()
            return {'Error':'Data already exists for this name.'}
        else:
            cur.execute("INSERT INTO weather (name, temperature, humidity) VALUES (?, ?, ?)", (name, temperature, humidity))
            conn.commit()
            conn.close()
            return {'Success':'Data added successfully.'}
    except Exception as e:
        print(f'!ERROR!\nFile : xhgfh.py\nFunction : add_data\nLine : {e.__traceback__.tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return{'Error':'An error occurred while adding data.'}

def get_data():
    try:
        conn = sqlite3.connect('weather.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM weather")
        rows = cur.fetchall()
        conn.close()
        if not rows: 
            return {'Error':"No data found."}
        return rows
    except Exception as e:
        print(f'!ERROR!\nFile : xhgfh.py\nFunction : get_data\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error':'An error occurred while fetching data.'}
    
def delete_data(name):
    try:
        conn = sqlite3.connect('weather.db')
        cur = conn.cursor()
        cur.execute("SELECT id FROM weather WHERE name=?", (name,))
        existing_record = cur.fetchone()
        if existing_record:
            cur.execute("DELETE FROM weather WHERE name = ?", (name,))
            conn.commit()
            conn.close()
            return {'Success': 'Data deleted successfully.'}
        else:
            conn.close()
            return {'Error': 'Data with the provided name does not exist in the table.'}
    except Exception as e:
        print(f'!ERROR!\nFile : xhgfh.py\nFunction : delete_data\nLine : {e.__traceback__.tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error': 'An error occurred while deleting data.'}
    
def update_data(name, temperature, humidity):
    try:
        conn = sqlite3.connect('weather.db')
        cur = conn.cursor()
        cur.execute("SELECT id FROM weather WHERE name=?", (name,))
        existing_record = cur.fetchone()
        if existing_record:
            cur.execute("UPDATE weather SET temperature = ?, humidity = ? WHERE name = ?", (temperature, humidity, name))
            conn.commit()
            conn.close()
            return {'Success': 'Data updated successfully.'}
        else:
            conn.close()
            return {'Error': 'Data with the provided name does not exist in the table.'}
    except Exception as e:
        print(f'!ERROR!\nFile : xhgfh.py\nFunction : update_data\nLine : {e.__traceback__.tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error': 'An error occurred while updating data.'}
    
def generate_jwt(username):
    try:
        payload = {'username': username}
        payload['Time'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        jwt_token = encode(payload, '37GUGKDWEGF7L8HF7GURGOHR48RFH', algorithm="HS256")
        return jwt_token
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        print(f'!ERROR!\nFile : function.py\nFunction : generate_jwt\nLine : {exc_tb.tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error':'An error occurred while generating JWT.'}

def verify_jwt(jwt):
    try:
        payload = decode(jwt, '37GUGKDWEGF7L8HF7GURGOHR48RFH', algorithms=["HS256"])
        if 'username' not in payload:
            return {'Error':'Invalid JWT token.'}
        current_date = datetime.now()
        jwt_date = datetime.strptime(payload.get('Time'), "%d-%m-%Y %H:%M:%S")
        jwt_expiry = 60*60*2
        if (current_date-jwt_date).seconds > jwt_expiry:
            return{'Error':'Session Expired'}
        return payload
    except DecodeError:
        return {'Error':'Invalid JWT token.'}
    except Exception as e:
        exc_type, exc_obj, exc_tb = exc_info()
        print(f'!ERROR!\nFile : function.py\nFunction : verify_jwt\nLine : {exc_tb.tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return {'Error':'An error occurred while verifying JWT.'}

