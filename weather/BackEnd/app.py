from os.path import abspath, join, dirname
from sys import path

base_dir = abspath(join(dirname(__file__), "../"))
path.append(base_dir)


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sys import exc_info
from function import get_weather,add_data, get_data, delete_data, update_data,generate_jwt,verify_jwt
import sqlite3
from BackEnd.model import User, Register, JWT, City

app = FastAPI()

@app.post("/register")
def register_user(mod: Register):
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        # Create 'users' table if it doesn't exist
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL)''')

        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (mod.username,))
        result = cur.fetchone()
        if result[0] > 0:
            conn.close()
            return JSONResponse(status_code=400, content={"Error":"Username already exists"})
        cur.execute("INSERT INTO users (username, password,email) VALUES (?, ?, ?)", (mod.username, mod.password,mod.email))
        conn.commit()
        conn.close()
        return JSONResponse(content={"Success": "User registered successfully."},status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : register_user\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while registering the user."},status_code=500)

@app.post("/login")
def login_user(mod: User):
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ? AND password = ?", (mod.username, mod.password))
        result = cur.fetchone()
        if result[0] > 0:
            conn.close()
            jwt = generate_jwt(mod.username)
            return JSONResponse(content={"Success": "User logged in successfully.", "jwt": jwt},status_code=200)
        conn.close()
        return JSONResponse(status_code=400, content={"Error":"Invalid username or password."})
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : login_user\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while logging in."},status_code=500)
    
@app.post("/profile")
def get_profile(mod: JWT):
    try:
        jwt_data = verify_jwt(mod.jwt)
        if 'Error' in jwt_data:
            return JSONResponse(content=jwt_data, status_code=400)
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (jwt_data['username'],))
        user_data = cur.fetchone()
        if not user_data:
            conn.close()
            return JSONResponse(content={"Error": "User not found."}, status_code=404)
        user = User(username=user_data[1], password=user_data[2], email=user_data[3])
        conn.close()
        user=dict(user)
        user.pop('password')
        return JSONResponse(content=(user), status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : get_profile\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while fetching profile."}, status_code=500)

@app.post("/add_city_weather")
def add_city_weather(mod:City):
    try:
        jwt_data=verify_jwt(mod.jwt)
        if 'Error' in jwt_data:
            return JSONResponse(content=jwt_data,status_code=400)
        weather_data = get_weather(mod.city)
        if 'Error' in weather_data:
            return JSONResponse(content=weather_data,status_code=400)
        data=add_data(weather_data['name'],weather_data['temperature'],weather_data['humidity'])
        if 'Error' in data:
            return JSONResponse(content=data,status_code=400)
        return JSONResponse(content=data,status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : add_city_weather\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while adding data."},status_code=500)

@app.post("/weather_list")
def get_weather_list(mod:JWT):
    try:
        jwt_data=verify_jwt(mod.jwt)
        if 'Error' in jwt_data:
            return JSONResponse(content=jwt_data,status_code=400)
        data=get_data()
        if 'Error' in data:
            return JSONResponse(content=data,status_code=400)
        return JSONResponse(content=data,status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : get_weather_list\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while fetching data."},status_code=500)

@app.post("/delete_city_weather")
def delete_city_weather(mod:City):
    try:
        jwt_data=verify_jwt(mod.jwt)
        if 'Error' in jwt_data:
            return JSONResponse(content=jwt_data,status_code=400)
        data=delete_data(mod.city)
        if 'Error' in data:
            return JSONResponse(content=data,status_code=400)
        return JSONResponse(content=data,status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : delete_city_weather\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while deleting data."},status_code=500)

@app.post("/update_city_weather")
def update_city_weather(mod:City):
    try:
        jwt_data=verify_jwt(mod.jwt)
        if 'Error' in jwt_data:
            return JSONResponse(content=jwt_data,status_code=400)
        weather_data = get_weather(mod.city)
        data=update_data(weather_data['name'],weather_data['temperature'],weather_data['humidity'])
        if 'Error' in data:
            return JSONResponse(content=data,status_code=400)
        return JSONResponse(content=data,status_code=200)
    except Exception as e:
        print(f'!ERROR!\nFile : app.py\nFunction : update_city_weather\nLine : {exc_info()[-1].tb_lineno}\nType : {type(e).__name__}\nDescription : {e}')
        return JSONResponse(content={"Error": "An error occurred while updating data."},status_code=500)


app.add_middleware(
   middleware_class = CORSMiddleware,
   allow_origins= ["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
