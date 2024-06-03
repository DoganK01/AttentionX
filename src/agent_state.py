from typing import Any, Dict, TypedDict
from langchain_core.pydantic_v1 import BaseModel, Field, validator

class ReflectionState(TypedDict):
    keys: Dict[str, Any]
    iteration: int

class Feedback(BaseModel):
    """ Represents feedback to improve response. """
    has_suggestions: bool = Field(..., description="Indicates whether there are suggestions for further improvements. True if there are suggestions, False otherwise.")
    suggestions: str = Field(..., description="Feedback and suggestions for improving the response. If there are no suggestions, this should be an empty string.")

    @validator("suggestions", "has_suggestions", pre=True, always=True)
    def question_ends_with_question_mark(cls, value, field):
      if field.name == "suggestions":
        if not isinstance(value, bool):
            raise ValueError(f"{field.name} must be a boolean!")
      if field.name == "has_suggestions":
        if not isinstance(value, str):
          raise ValueError(f"{field.name} must be a string!")
      return value