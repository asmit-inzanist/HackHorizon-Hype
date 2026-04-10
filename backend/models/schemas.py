"""
Pydantic schemas for request/response validation across all endpoints.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────
class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    user_id: str
    email: str


# ─────────────────────────────────────────────
# Profile
# ─────────────────────────────────────────────
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    allergies: Optional[list[str]] = None
    chronic_conditions: Optional[list[str]] = None

class ProfileResponse(BaseModel):
    id: str
    full_name: str
    age: Optional[int] = None
    blood_group: Optional[str] = None
    allergies: list[str] = Field(default_factory=list)
    chronic_conditions: list[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ─────────────────────────────────────────────
# Medical Records
# ─────────────────────────────────────────────
class MedicineEntry(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None

class ExtractedData(BaseModel):
    """Structured output from Agent 1 — Document Intake."""
    medicines: list[MedicineEntry] = Field(default_factory=list)
    diagnosis: Optional[str] = None
    doctor_name: Optional[str] = None
    hospital: Optional[str] = None
    date: Optional[str] = None
    notes: Optional[str] = None

class RecordResponse(BaseModel):
    id: str
    patient_id: str
    file_url: str
    file_type: str
    original_filename: str
    extracted_data: dict = Field(default_factory=dict)
    voice_note_url: Optional[str] = None
    transcription: Optional[str] = None
    created_at: Optional[str] = None


# ─────────────────────────────────────────────
# Medicine Analysis
# ─────────────────────────────────────────────
class GenericOption(BaseModel):
    name: str
    price: Optional[float] = None
    manufacturer: Optional[str] = None
    savings: Optional[float] = None

class MedicineAlternative(BaseModel):
    original_name: str
    original_price: Optional[float] = None
    generic_name: Optional[str] = None
    generic_alternatives: list[GenericOption] = Field(default_factory=list)
    cdsco_approved: Optional[bool] = None
    safety_equivalent: Optional[bool] = None

class MedicineAnalysisResponse(BaseModel):
    id: str
    record_id: str
    medicines: list[dict] = Field(default_factory=list)
    total_savings: float = 0.0
    created_at: Optional[str] = None


# ─────────────────────────────────────────────
# Patient Summary
# ─────────────────────────────────────────────
class AllergyWarning(BaseModel):
    medicine: str
    allergy: str
    severity: str  # "high", "medium", "low"
    message: str

class PatientSummaryResponse(BaseModel):
    id: str
    patient_id: str
    summary_text: str
    allergy_warnings: list[dict] = Field(default_factory=list)
    audio_url: Optional[str] = None
    created_at: Optional[str] = None


# ─────────────────────────────────────────────
# Sharing
# ─────────────────────────────────────────────
class ShareTokenResponse(BaseModel):
    token: str
    share_url: str
    expires_at: str

class ShareFileRequest(BaseModel):
    record_id: str
    recipient_email: str
    message: Optional[str] = None

class SharedFileResponse(BaseModel):
    id: str
    sender_id: str
    recipient_email: str
    record_id: str
    message: Optional[str] = None
    is_read: bool = False
    created_at: Optional[str] = None


# ─────────────────────────────────────────────
# Pharmacy
# ─────────────────────────────────────────────
class PharmacyResult(BaseModel):
    name: Optional[str] = None
    latitude: float
    longitude: float
    address: Optional[str] = None
    distance_km: Optional[float] = None
    directions_url: str


# ─────────────────────────────────────────────
# Voice
# ─────────────────────────────────────────────
class TranscriptionResponse(BaseModel):
    text: str
    language: Optional[str] = None

class TTSRequest(BaseModel):
    text: str
    language: str = "en"  # en, hi, ta, te, bn, mr, gu, kn, ml

class TTSResponse(BaseModel):
    audio_url: str
