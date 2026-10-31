
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..DB.database import get_db
from ..models.incident import ActionLog, Incident
from ..schemas.actionLog import (
    ActionLogCreate,
    ActionResponse
)

router = APIRouter(
    prefix="/action-logs",
    tags=["ActionLog"]
)


# Create ActionLog
@router.post("/", response_model=ActionResponse)
def create_actionlog(
    actionlog_data: ActionLogCreate,
    db: Session = Depends(get_db)
):
    # Check whether the incident exists
    incident = db.query(Incident).filter(
        Incident.id == actionlog_data.incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    try:
        new_actionlog = ActionLog(
            incident_id=actionlog_data.incident_id,
            action=actionlog_data.action,
            details=actionlog_data.details
        )

        db.add(new_actionlog)
        db.commit()
        db.refresh(new_actionlog)

        return new_actionlog

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create the action log."
        )


# Get all ActionLogs
@router.get("/", response_model=list[ActionResponse])
def get_all_actionlogs(db: Session = Depends(get_db)):
    actionlogs = db.query(ActionLog).all()
    return actionlogs


# Get ActionLog by ID
@router.get("/{actionlog_id}", response_model=ActionResponse)
def get_actionlog(
    actionlog_id: int,
    db: Session = Depends(get_db)
):
    actionlog = db.query(ActionLog).filter(
        ActionLog.id == actionlog_id
    ).first()

    if not actionlog:
        raise HTTPException(
            status_code=404,
            detail="Action log not found"
        )

    return actionlog


# Get ActionLogs belonging to an Incident
@router.get("/incident/{incident_id}", response_model=list[ActionResponse])
def get_incident_actionlogs(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return db.query(ActionLog).filter(
        ActionLog.incident_id == incident_id
    ).all()
