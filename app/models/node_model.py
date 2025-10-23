# from pydantic import BaseModel, Field
# from typing import Optional, List
# from datetime import datetime

# class NodeModel(BaseModel):
#     name: str
#     type: str  # "extract", "transform", "load", etc.
#     description: Optional[str] = None
#     code: str  # store full Python code here
#     tags: Optional[List[str]] = []  # optional list of tags
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "extract_data3.py",
#                 "type": "extract",
#                 "description": "Uploaded script: extract_data3.py",
#                 "code": "import json\nimport os\n...",
#                 "tags": ["sales"]
#             }
#         }
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class NodeModel(BaseModel):
    id: str= Field(alias="_id")  # ✅ Maps MongoDB _id to id
    name: str
    type: str  # "extract", "transform", "load", etc.
    description: Optional[str] = None
    code: str  # store full Python code here
    tags: Optional[List[str]] = []  # optional list of tags
    position: Optional[Dict[str, int]] = None  # e.g., {"x": 100, "y": 200}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "name": "extract_data3.py",
                "type": "extract",
                "description": "Uploaded script: extract_data3.py",
                "code": "import json\nimport os\n...",
                "tags": ["sales"],
                "position": {"x": 100, "y": 200}
            }
        }
