
from backend.core.team_assignment import assign_team
from backend.schemas.ai_assessment import IncidentCategory
from backend.DB.database import SessionLocal


def test_team_assignment():

    db = SessionLocal()

    try:
        category = IncidentCategory.NETWORK

        team = assign_team(
            category=category,
            db=db
        )

        print("Assigned Team ID:", team.id)
        print("Assigned Team Name:", team.name)

    except ValueError as e:
        print("Assignment Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    test_team_assignment()
