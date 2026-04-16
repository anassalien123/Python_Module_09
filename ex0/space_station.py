from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("\n========================")

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now()
    )
    print("Valid station created:")
    print(f"  ID:     {station.station_id}")
    print(f"  Name:   {station.name}")
    print(f"  Crew:   {station.crew_size} people")
    print(f"  Power:  {station.power_level}%")
    print(f"  Oxygen: {station.oxygen_level}%")
    status: str = (
        "Operational"
        if station.is_operational
        else "Offline"
    )

    print(f"  Status: {status}")
    print("\n=========================")

    print("Expected validation error:")
    try:
        bad_station = SpaceStation(
            station_id="ISS001",
            name="Orbital One",
            crew_size=90,
            power_level=92.5,
            oxygen_level=88.0,
            last_maintenance=datetime.now()
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])
