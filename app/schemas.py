from datetime import datetime

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
