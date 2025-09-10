from pydantic import BaseModel

class PlanInput(BaseModel):
    name: str
    rate_limit_window: int = 60
    requests_per_window: int = 10

class PlanOutput(PlanInput):
    id: int

    class Config:
        from_attributes = True  
