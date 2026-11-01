from datetime import datetime
from pydantic import BaseModel, Field

class IncidentAssessment(BaseModel):
    title:str=Field(description="Short incident title")
    description:str=Field(description="Clear incident summary")
    category:str=Field(description="Incident Category")
    location:str|None=Field(
        default=None,
        description="Location mentioned in the report"
    )
    impact:str=Field(description="Impact layer")
    urgency:str=Field(description="urgency level")
    deadline:datetime|None=Field(
        default=None,
        description="Deadline mentioned in the report."
    )