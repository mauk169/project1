from dataclasses import dataclass
@dataclass
class Operation:
    operation_id: int
    operation_type: str
    amount: float
    description: str | None
    user_id: int
    user_login: str | None = None