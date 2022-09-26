#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

class PersonBase(BaseModel): 
    first_name: str = Field(
        min_length=1,
        max_length=50,
        example="Marcos"
        )
    last_name: str = Field(
        min_length=1,
        max_length=50,
        example="Alvarez"
        )
    age: int = Field(
        gt=0,
        le=115,
        example=15
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config: 
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Luis",
    #             "last_name": "Aviles Altamar",
    #             "age": 27, 
    #             "hair_color": "brown",
    #             "is_married": False
    #         }
    #     }

class Person(PersonBase):
    password: str = Field(min_length=8, example="Cont4aseña1234")
class PersonOut(BaseModel): 
    pass



@app.get(
    "/",
    status_code=status.HTTP_200_OK)
def home(): 
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    "/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body()): 
    return person

# Validaciones: Query Parameters

@app.get(
    "/person/detail",
    status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocío"
        ),
    age: str = Query(
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
): 
    return {name: age}

# Validaciones: Path Parameters

@app.get(
    "/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        gt=0,
        example=123
        )
): 
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    "/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED)
def update_person(
    person_id: int = Path(
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(),
    #location: Location = Body()
): 
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person