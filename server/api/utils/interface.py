from pydantic import BaseModel


class PlantumlGenerationQuery(BaseModel):
    description: str