from fastapi import FastAPI, status, HTTPException, Depends
from app.database import restaurants_collection as collection
from app.schemas import Restaurant
from uuid import uuid4
from . import api_router 
from typing import List

router = api_router

@router.post('/create-reastaurant', summary="Create new restaurant", response_model=Restaurant)
async def create_restaurant(data: Restaurant):
    restaurant = {
        'id': str(uuid4()),
        'name': data.name,
        'address': data.address,
        'rating': data.rating,
        'cuisines': data.cuisines,
        'img_url': data.img_url,
        'averageDeliveryTime': data.averageDeliveryTime
    }
    collection.insert_one(restaurant)   # saving restaurant to database
    return restaurant

@router.get("/get-restaurants", response_model=List[Restaurant])
async def get_restaurants():
    restaurants = []
    result = collection.find()
    for restaurant in result:
        restaurants.append(restaurant)
    
    return restaurants