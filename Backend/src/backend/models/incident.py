from datetime import datetime,timezone
from sqlalchemy import (DateTime,Integer,String,Text,ForeignKey)
from sqlalchemy.orm import Mapped,mapped_column,relationship
from ..DB.database import Base

class Incident(Base):
    __tablename__ = "Incidents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), # lambda: to make the single line fn
        nullable=False
    )

    team_id: Mapped[int|None]=mapped_column(
        Integer,
        ForeignKey("Teams.id"),
        nullable= True,
        index = True
    )

    team = relationship("Team",back_populates = "incidents")
    action_logs = relationship("ActionLog",back_populates = "incident")


class Team(Base):
    __tablename__ = "Teams"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    incidents = relationship("Incident",back_populates="team")

class ActionLog(Base):
    __tablename__ = "ActionLog"

    id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            index=True
        )

    incident_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Incidents.id"),
        index=True
    )

    action: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    details: Mapped[str] = mapped_column(
        Text,
        nullable = False
    )

    timestamp : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable = False
    )

    incident = relationship("Incident",back_populates = "action_logs")