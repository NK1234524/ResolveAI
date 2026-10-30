from pydantic import BaseModel,ConfigDict,Field

class TeamCreate(BaseModel):
    
    name:str=Field(
        min_length = 5
    )
    description:str=Field(
        min_length = 10
    )

class TeamUpdate(BaseModel):
    name:str|None = Field(default= None,min_length=5,max_length=200)
    description:str|None = Field(default = None,min_length =10)

class TeamResponse(BaseModel):
    id:int
    name:str
    description:str
    
    model_config=ConfigDict(from_attributes=True)

