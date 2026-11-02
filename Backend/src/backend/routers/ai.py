from fastapi import APIRouter , Depends, HTTPException, Header
from pydantic import ValidationError
from backend.schemas.ai_assessment import(
    IncidentReporterRequest,
    IncidentAssessment,
    IncidentProcessingResponse
)
from sqlalchemy.exc import IntegrityError
import hashlib
from backend.models.incident import Incident
from backend.services.incident_service import create_incident
from sqlalchemy.orm import Session
from backend.DB.database import get_db
from backend.core.priority_engine import calculate_priority as cp
from backend.services.gemini_service import analyze_incident
from backend.core.team_assignment import assign_team
router= APIRouter(
    prefix = "/ai",
    tags = ["AI Assessment"]
)


@router.post("/assess", response_model=IncidentProcessingResponse)
def assess_incident(
    request: IncidentReporterRequest,
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
        min_length=1,
        max_length=128
    ),
    db: Session = Depends(get_db)
):
    try:
        # 1. Generate request hash
        request_hash = hashlib.sha256(
            request.report.strip().encode("utf-8")
        ).hexdigest()

        # 2. Check for an existing request
        existing_incident = db.query(Incident).filter(
            Incident.idempotency_key == idempotency_key
        ).first()

        if existing_incident:

            if existing_incident.request_hash != request_hash:
                raise HTTPException(
                    status_code=409,
                    detail="Idempotency key already used with a different request."
                )

            return IncidentProcessingResponse(
                id=existing_incident.id,
                title=existing_incident.title,
                description=existing_incident.description,
                category=existing_incident.category,
                location=existing_incident.location,
                impact=existing_incident.impact,
                urgency=existing_incident.urgency,
                deadline=existing_incident.deadline,
                priority=existing_incident.priority,
                team_id=existing_incident.team_id,
                assigned_team=existing_incident.team.name,
                status=existing_incident.status
            )

        # 3. Gemini AI Assessment
        result = analyze_incident(request.report)

        # 4. Calculate priority
        priority = cp(result.impact, result.urgency)

        # 5. Assign appropriate team
        team = assign_team(result.category, db)

        # 6. Save incident
        saved_incident = create_incident(
            assessment=result,
            priority=priority,
            team=team,
            db=db,
            idempotency_key=idempotency_key,
            request_hash=request_hash
        )

        # 7. Return successful response
        return IncidentProcessingResponse(
            **result.model_dump(),
            priority=priority,
            team_id=saved_incident.team_id,
            assigned_team=team.name,
            id=saved_incident.id,
            status=saved_incident.status
        )

    except IntegrityError:
        db.rollback()

        # Another concurrent request may have created this incident
        existing_incident = db.query(Incident).filter(
            Incident.idempotency_key == idempotency_key
        ).first()

        if existing_incident is None:
            raise HTTPException(
                status_code=500,
                detail="Database integrity error while creating incident."
            )

        if existing_incident.request_hash != request_hash:
            raise HTTPException(
                status_code=409,
                detail="Idempotency key already used with a different request."
            )

        return IncidentProcessingResponse(
            id=existing_incident.id,
            title=existing_incident.title,
            description=existing_incident.description,
            category=existing_incident.category,
            location=existing_incident.location,
            impact=existing_incident.impact,
            urgency=existing_incident.urgency,
            deadline=existing_incident.deadline,
            priority=existing_incident.priority,
            team_id=existing_incident.team_id,
            assigned_team=existing_incident.team.name,
            status=existing_incident.status
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
