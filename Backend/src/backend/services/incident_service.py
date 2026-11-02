# responsible for saving the AI-assessed incident and its initial ActionLog into PostgreSQL.

from sqlalchemy.orm import Session
from backend.models.incident import Incident,Team,ActionLog
from backend.schemas.ai_assessment import IncidentAssessment
from sqlalchemy.exc import IntegrityError
def create_incident(
        assessment:IncidentAssessment,
        priority:str,
        team:Team,
        db:Session,
        idempotency_key:str,
        request_hash:str
):
    try:
        # 1. Create Incident object
        incident = Incident(
            title = assessment.title,
            description = assessment.description,
            category=assessment.category.value,
            location=assessment.location,
            impact=assessment.impact.value,
            urgency=assessment.urgency.value,
            deadline=assessment.deadline,
            priority=priority,
            team_id=team.id,
            idempotency_key =idempotency_key,
            request_hash=request_hash
        )

        # 2. Add the incident to the database session
        db.add(incident)

        # 3. Flush to generate Incident ID
        db.flush()

        # 4. Create Action log
        action_log = ActionLog(
            incident_id=incident.id,
            action="INCIDENT_CREATED",
            details=(
                f"Incident assessed by ResolveAI. "
                f"Category: {assessment.category.value}. "
                f"Impact: {assessment.impact.value}. "
                f"Urgency: {assessment.urgency.value}. "
                f"Priority: {priority}. "
                f"Assigned to: {team.name}."
            )
        )
        db.add(action_log)
        db.commit()
        db.refresh(incident)
        return incident

    except IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise

    