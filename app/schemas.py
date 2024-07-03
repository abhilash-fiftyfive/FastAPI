from uuid import UUID
from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    access_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    

class UserOut(BaseModel):
    id: UUID
    email: str

class SystemUser(UserOut):
    password: str

class UpdateUserRequest(BaseModel):
    email: str = None


class Restaurant(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    address: str = Field(..., min_length=3, max_length=100)
    rating: float = Field(..., ge=1, le=5)
    averageDeliveryTime: str = Field(..., min_length=3, max_length=100)
    cuisines: list = Field(..., min_items=1)
    img_url: str = None
