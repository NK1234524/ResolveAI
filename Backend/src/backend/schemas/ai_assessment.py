from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
class IncidentCategory(str,Enum):
    NETWORK="NETWORK"
    HARDWARE="HARDWARE"
    SOFTWARE="SOFTWARE"
    SECURITY="SECURITY"
    ACCESS="ACCESS"
    INFRASTRUCTURE="INFRASTRUCTURE"
    OTHER="OTHER"

class ImpactLevel(str,Enum):
    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"
    CRITICAL="CRITICAL"

class UrgencyLevel(str,Enum):
    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"
    CRITICAL="CRITICAL"

class PriorityLevel(str,Enum):
    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"
    CRITICAL="CRITICAL"

class IncidentAssessment(BaseModel):
    title:str=Field(description="Short incident title")
    description:str=Field(description="Clear incident summary")
    category:IncidentCategory
    location:str|None=Field(
        default=None,
        description="Location mentioned in the report"
    )
    impact:ImpactLevel
    urgency:UrgencyLevel
    deadline:datetime|None=Field(
        default=None,
        description="Deadline mentioned in the report."
    )
    

class IncidentReporterRequest(BaseModel):
    report : str=Field(
        min_length = 10,
        description = "Natural language incident report."
    )


class IncidentProcessingResponse(IncidentAssessment):
    id:int
    priority:PriorityLevel
    team_id:int
    assigned_team:str
    status:str