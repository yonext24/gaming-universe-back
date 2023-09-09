from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional

class SessionBase(BaseModel):
    user_id: int
    expiration_at: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    model_config = ConfigDict(from_attributes=True)
    
    session_id: UUID4
    created_at: str
