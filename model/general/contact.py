from dataclasses import dataclass


@dataclass
class Contact:
    name: str
    contact_emails: list[str]
