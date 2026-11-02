from sqlalchemy.orm import Session
from backend.models.incident import Team
from backend.schemas.ai_assessment import IncidentCategory

TEAM_CATEGORY_MAPPING = {
    IncidentCategory.NETWORK: "Network Support",
    IncidentCategory.HARDWARE: "Hardware Support",
    IncidentCategory.SOFTWARE: "Software Support",
    IncidentCategory.SECURITY: "Security Team",
    IncidentCategory.ACCESS: "Access Management",
    IncidentCategory.INFRASTRUCTURE: "Infrastructure Team",
    IncidentCategory.OTHER: "General Support"
}

def assign_team( 
    category: IncidentCategory,
    db: Session
) -> Team:
    team_name = TEAM_CATEGORY_MAPPING.get(category)
    if team_name is None:
        raise ValueError(
            f"No team mapping found for category:{category}"
        )
    team = (
        db.query(Team).filter(Team.name == team_name)
        .first()
    )
    if team is None:
        raise ValueError(
            f"Team : {team_name} is not found in the Database."
        )
    return team