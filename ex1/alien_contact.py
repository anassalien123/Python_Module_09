from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(
        default=None,
        max_length=500,
    )
    is_verified: bool = False

    @model_validator(mode="after")
    def apply_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "Contact ID must start with 'AC' (Alien Contact)"
            )

        if (
            self.contact_type == ContactType.physical
            and not self.is_verified
        ):
            raise ValueError(
                "Physical contact reports must be verified before submission"
            )

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) must include a received message"
            )

        return self


def print_contact(report: AlienContact) -> None:
    print("Valid contact report:")
    print(f"  ID:        {report.contact_id}")
    print(f"  Type:      {report.contact_type.value}")
    print(f"  Location:  {report.location}")
    print(f"  Signal:    {report.signal_strength}/10")
    print(f"  Duration:  {report.duration_minutes} minutes")
    print(f"  Witnesses: {report.witness_count}")

    if report.message_received:
        print(f"  Message:'{report.message_received}'")


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("============================")

    try:
        valid = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
        print_contact(valid)

    except ValidationError as e:
        for err in e.errors():
            print(err["msg"].replace("Value error, ", ""))

    print("\n============================")
    print("Expected validation error:")

    try:
        invalid = AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Roswell, New Mexico",
            contact_type=ContactType.telepathic,
            signal_strength=4.5,
            duration_minutes=30,
            witness_count=2,
            message_received="Mind signal detected",
        )
        print_contact(invalid)

    except ValidationError as e:
        for err in e.errors():
            print(err["msg"].replace("Value error, ", ""))
