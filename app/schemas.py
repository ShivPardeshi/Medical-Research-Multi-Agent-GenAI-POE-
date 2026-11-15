"""Pydantic schemas for Medical Researcher Agents API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class MedicalQuestionRequest(BaseModel):
    """Schema for incoming user clinical and biomedical research inquiries."""
    question: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="The medical scenario, clinical inquiry, or pharmacology question to analyze.",
        examples=["What are the first-line antihypertensive choices in a patient with Type 2 Diabetes and persistent albuminuria?"]
    )

    @field_validator("question")
    @classmethod
    def validate_question_content(cls, value: str) -> str:
        trimmed = value.strip()
        if len(trimmed) < 5:
            raise ValueError("Medical query must contain at least 5 non-whitespace characters.")
        return trimmed


class MedicalResearchResponse(BaseModel):
    """Schema for multi-agent evidence-based medical research response."""
    status: str = Field(default="success", description="Status of the clinical research analysis.")
    question: str = Field(..., description="The original clinical question or scenario submitted.")
    answer: str = Field(..., description="Synthesized, peer-reviewed medical guidance memo.")
    category: Optional[str] = Field(default=None, description="Identified medical or clinical specialty area.")
    sources: List[str] = Field(default_factory=list, description="Clinical practice guidelines and pharmacotherapy sources cited.")
    disclaimer: str = Field(..., description="Mandatory medical research disclaimer.")


class HealthResponse(BaseModel):
    """Schema for application health check endpoint."""
    status: str = Field(default="healthy")
    app_name: str
    groq_configured: bool
    model: str
    agents: List[str]


# Backward compatibility aliases
LegalQuestionRequest = MedicalQuestionRequest
LegalBotResponse = MedicalResearchResponse
