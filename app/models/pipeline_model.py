from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class ConnectionModel(BaseModel):
    from_node: str = Field(..., alias="from")  # node _id
    to_node: str = Field(..., alias="to")      # node _id

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {"from": "68f77b73af174df7a97037f9", "to": "68f77c1cb754e9c3ac67721e"}
        }

class PipelineModel(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[str]  # list of node _id strings
    connections: List[ConnectionModel] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "name": "ETL3",
                "description": "Checking..",
                "nodes": [
                    "68f77b73af174df7a97037f9",
                    "68f7834e4fa73a9efb55be19",
                    "68f77c1cb754e9c3ac67721e"
                ],
                "connections": [
                    {"from": "68f77b73af174df7a97037f9", "to": "68f77c1cb754e9c3ac67721e"},
                    {"from": "68f77c1cb754e9c3ac67721e", "to": "68f7834e4fa73a9efb55be19"}
                ]
            }
        }
