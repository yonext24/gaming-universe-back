from pydantic import BaseModel, ConfigDict

class BaseUser(BaseModel):

    first_name: str
    email: str | None
    last_name: str
    username: str
    active: bool


class User(BaseUser):
    id: int


class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)
    
    password: str
