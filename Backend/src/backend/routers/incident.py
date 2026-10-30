from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError 

from ..DB.database import get_db
from ..models.incident import Incident, Team
from ..schemas.incident import IncidentCreate, IncidentResponse, IncidentUpdate

router = APIRouter(
    prefix = "/incidents", # All endpoints start with the /incidents
    tags  = ["Incidents"]  # Groups these endpoints under the incident section in Swagger UI
)

# Create Incident

@router.post("/",response_model = IncidentResponse)
def create_incident(
    incident_data: IncidentCreate,
    db:Session = Depends(get_db)
):
    try:
        new_incident = Incident(
            title = incident_data.title,
            description = incident_data.description
        )

        db.add(new_incident)
        db.commit()
        db.refresh(new_incident)

        return new_incident

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = "Failed to create the incident"
        )

# Get all incidents
@router.get("/",response_model = list[IncidentResponse])
def get_all_incidents(db:Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    return incidents

# Get Incident by ID
@router.get("/{incident_id}",response_model = IncidentResponse)
def get_incident(
    incident_id:int,
    db:Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()
    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )
    return incident