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

    except SQLAlchemyError as e:
        db.rollback()
        # Debugging step :
        # import traceback
        # traceback.print_exc()
        # print("Database error:",str(e))
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

# Update Incident
@router.put("/{incident_id}",response_model= IncidentResponse)
def update_incident(
    incident_id:int,
    incident_data:IncidentUpdate,
    db:Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code = 404,
            detail = "Incident not found"
        )
    update_Data = incident_data.model_dump(exclude_unset =True)

    # Validate Team if team_id is provided

    if update_Data.get("team_id") is not None:
        team = db.query(Team).filter(
            Team.id == update_Data["team_id"]
        ).first()

        if not team:
            raise HTTPException(
                status_code  = 404,
                detail = "Team not found"
            )
        try:
            for key,value in update_Data.items():
                setattr(incident, key, value)
            db.commit()
            db.refresh(incident)
            return incident

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                staus_code = 500,
                detail = "Failed to update the incident"
            )

# Delete Incident 
@router.delete("/{incident_id}")
def delete_incident(
    incident_id : int,
    db:Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code = 404,
            detail = "Incident not found"
        )
    try:
        db.delete(incident)
        db.commit()
        return{
            "message":"Incident completed successfully"
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = "Failed to delete the incidents"
        )