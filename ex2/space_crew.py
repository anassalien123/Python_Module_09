from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader: bool = False

        member: CrewMember
        for member in self.crew:
            if (
                member.rank == Rank.commander
                or member.rank == Rank.captain
            ):
                has_leader = True
                break

        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced: int = sum(
                1
                for member in self.crew
                if member.years_experience >= 5
            )

            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions require 50% experienced crew "
                    "(5+ years)"
                )

        all_active: bool = True

        for member in self.crew:
            if not member.is_active:
                all_active = False
                break

        if not all_active:
            raise ValueError("All crew members must be active")

        return self


if __name__ == "__main__":

    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        mission: SpaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=40,
                    specialization="Mission Command",
                    years_experience=15,
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=6,
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")

        m: CrewMember
        for m in mission.crew:
            print(f"- {m.name} ({m.rank.value}) - {m.specialization}")

    except ValidationError as e:
        for ee in e.errors():
            print(ee['msg'])

    print("=========================================")
    print("Expected validation error:")

    try:
        bad_mission: SpaceMission = SpaceMission(
            mission_id="M_BAD_01",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=100,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="C004",
                    name="Bob",
                    rank=Rank.officer,
                    age=30,
                    specialization="Science",
                    years_experience=3,
                ),
                CrewMember(
                    member_id="C005",
                    name="Eve",
                    rank=Rank.lieutenant,
                    age=28,
                    specialization="Engineering",
                    years_experience=2,
                ),
            ],
        )

    except ValidationError as e:
        for ee in e.errors():
            print(ee['msg'])
