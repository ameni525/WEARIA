from pydantic import BaseModel

class ClassifyResponse(BaseModel):
    category: str
    color: str
    confidence: float
    image_url: str
