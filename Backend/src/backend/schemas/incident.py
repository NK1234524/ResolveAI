from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field

# validates incoming incident data
class IncidentCreate(BaseModel):
    title:str=Field(
        min_length = 5,
        max_length = 200
    )
    description:str=Field(
        min_length = 10
    )

# Defines the data returned by the API
class IncidentResponse(BaseModel):
    id:int
    title:str
    description:str
    priority:str
    status:str
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)
