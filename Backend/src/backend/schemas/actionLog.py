from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field

# validates incoming ActionLog
class ActionLogCreate(BaseModel):
    incident_id:int
    action:str=Field(min_length=3,max_length=200)
    details:str=Field(
        min_length = 10
    )



# Defines the data returned by the API
class ActionResponse(BaseModel):
    id:int
    incident_id:int
    action:str
    details:str
    timestamp:datetime

    model_config = ConfigDict(from_attributes=True)

