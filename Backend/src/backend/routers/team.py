from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError 

from ..DB.database import get_db
from ..models.incident import  Team
from ..schemas.team import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter(
    prefix = "/teams", # All endpoints start with the /incidents
    tags  = ["Teams"]  # Groups these endpoints under the incident section in Swagger UI
)

# Create Team
@router.post("/",response_model = TeamResponse)
def create_Team(
    team_Data: TeamCreate,
    db:Session = Depends(get_db)
):
    try:
        new_team = Team(
            name = team_Data.name,
            description = team_Data.description
        )
        db.add(new_team)
        db.commit()
        db.refresh(new_team)

        return new_team

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code = 500,
            detail = "Failed to create a Team"
        )

# Get all the teams
@router.get("/",response_model = list[TeamResponse])
def get_all_teams(db:Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams

# Get Team by ID
@router.get("/{team_id}",response_model=TeamResponse)
def get_team(
    team_id:int,
    db:Session = Depends(get_db)
):
    team = db.query(Team).filter(
        Team.id == team_id
    ).first()

    if not team:
        raise HTTPException(
            status_code = 404,
            detail = "Team not found"
        )
    return team

# Update Team
@router.put("/{team_id}",response_model = TeamResponse)
def update_team(
    team_id:int,
    team_data:TeamUpdate,
    db:Session = Depends(get_db)
):
    team = db.query(Team).filter(
        Team.id == team_id
    ).first()

    if not team:
        raise HTTPException(
            status_code = 404,
            detail = "Team not found"
        )
    update_Data = team_data.model_dump(exclude_unset=True)

    # Validate Team if Team_id is provided
    # if update_Data.get("team_id") is not None:
    #         team = db.query(Team).filter(
    #             Team.id == update_Data["team_id"]
    #         ).first()
    
           
    try:
                for key,value in update_Data.items():
                    setattr(team, key, value)
                db.commit()
                db.refresh(team)
                return team
    
    except SQLAlchemyError:
                db.rollback()
                raise HTTPException(
                    status_code = 500,
                    detail = "Failed to update the team"
                )

# Delete Team 
@router.delete("/{team_id}")
def delete_team(
    team_id:int,
    db:Session=Depends(get_db)
):
    team=db.query(Team).filter(
        Team.id==team_id
    ).first()

    if not team:
        raise HTTPException(
            status_code =404,
            detail="Team not found"
        )
    try:
        db.delete(team)
        db.commit()
        return{
            "message":"Team deleted successfully"
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code =500,
            detail="Failed to delete the team"
        )