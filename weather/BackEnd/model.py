from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(..., title="Username", description="Username of the user.")
    password: str = Field(..., title="Password", description="Password of the user.")

class Register(User):
    email: str = Field(..., title="Email", description="Email of the user.")

class JWT(BaseModel):
    jwt: str = Field(..., title="JWT", description="JWT token of the user.")

class City(JWT):
    city: str = Field(..., title="City", description="City for which weather data is to be fetched.")
