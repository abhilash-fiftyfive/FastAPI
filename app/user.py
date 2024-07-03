from . import api_router 
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId
from app.database import users_collection as collection
from app.schemas import UserOut, UserAuth, TokenSchema, SystemUser, UpdateUserRequest
from app.utils import get_hashed_password, verify_password, create_access_token
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm
from app.deps import get_current_user


router = api_router

@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = collection.find_one({"email": data.email})
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    collection.insert_one(user)   # saving user to database
    return user

@router.post('/login', summary="Create access tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = collection.find_one({"email": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email'])
    }

@router.get("/get-users")
async def get_users(user: SystemUser = Depends(get_current_user)):
    users = []
    result = collection.find()
    for user in result:
        users.append({
            "id": user["id"],
            "email": user["email"]
        })
    return users

@router.put("/update-user/{id}")
async def update_user(id: str, request: UpdateUserRequest, user: SystemUser = Depends(get_current_user)):
    try:
        object_id = ObjectId(id)
        print("Converted ObjectId:", object_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    update_data = {k: v for k, v in request.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update")

    print("Update Data:", update_data)
    
    result = collection.update_one({"_id": object_id}, {"$set": update_data})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found or no changes made")

@router.delete("/delete-user/{id}")
async def delete_user(id: str, user: SystemUser = Depends(get_current_user)):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = collection.delete_one({"_id": object_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")