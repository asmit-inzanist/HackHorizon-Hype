-- ============================================================
-- Unified Personal Health Record — Database Migration
-- Run this in Supabase Dashboard → SQL Editor
-- ============================================================

-- Enable UUID extension (usually already enabled)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ──────────────────────────────────────────────
-- 1. PROFILES
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.profiles (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name   TEXT NOT NULL DEFAULT '',
    age         INTEGER,
    blood_group TEXT,
    allergies   TEXT[] DEFAULT '{}',
    chronic_conditions TEXT[] DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ──────────────────────────────────────────────
-- 2. MEDICAL RECORDS
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.medical_records (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id        UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    file_url          TEXT NOT NULL,
    file_type         TEXT NOT NULL CHECK (file_type IN ('prescription', 'lab_report', 'imaging')),
    original_filename TEXT NOT NULL,
    extracted_data    JSONB DEFAULT '{}',
    voice_note_url    TEXT,
    transcription     TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_medical_records_patient
    ON public.medical_records(patient_id);

-- ──────────────────────────────────────────────
-- 3. MEDICINE ANALYSES
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.medicine_analyses (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id      UUID NOT NULL REFERENCES public.medical_records(id) ON DELETE CASCADE,
    patient_id     UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    medicines      JSONB DEFAULT '[]',
    total_savings  NUMERIC DEFAULT 0,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_medicine_analyses_record
    ON public.medicine_analyses(record_id);

-- ──────────────────────────────────────────────
-- 4. PATIENT SUMMARIES
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.patient_summaries (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id       UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    summary_text     TEXT NOT NULL DEFAULT '',
    allergy_warnings JSONB DEFAULT '[]',
    audio_url        TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_patient_summaries_patient
    ON public.patient_summaries(patient_id);

-- ──────────────────────────────────────────────
-- 5. SHARE TOKENS (24h expiry links)
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.share_tokens (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id  UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    token       TEXT NOT NULL UNIQUE,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_share_tokens_token
    ON public.share_tokens(token);

-- ──────────────────────────────────────────────
-- 6. SHARED FILES (user-to-user)
-- ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.shared_files (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id       UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    recipient_email TEXT NOT NULL,
    record_id       UUID NOT NULL REFERENCES public.medical_records(id) ON DELETE CASCADE,
    message         TEXT,
    is_read         BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_shared_files_recipient
    ON public.shared_files(recipient_email);

-- ──────────────────────────────────────────────
-- ROW LEVEL SECURITY
-- ──────────────────────────────────────────────

-- Profiles: users can only read/update their own
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- Medical Records: users can CRUD their own
ALTER TABLE public.medical_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own records"
    ON public.medical_records FOR SELECT
    USING (auth.uid() = patient_id);

CREATE POLICY "Users can insert own records"
    ON public.medical_records FOR INSERT
    WITH CHECK (auth.uid() = patient_id);

CREATE POLICY "Users can update own records"
    ON public.medical_records FOR UPDATE
    USING (auth.uid() = patient_id);

CREATE POLICY "Users can delete own records"
    ON public.medical_records FOR DELETE
    USING (auth.uid() = patient_id);

-- Medicine Analyses
ALTER TABLE public.medicine_analyses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own analyses"
    ON public.medicine_analyses FOR SELECT
    USING (auth.uid() = patient_id);

CREATE POLICY "Users can insert own analyses"
    ON public.medicine_analyses FOR INSERT
    WITH CHECK (auth.uid() = patient_id);

-- Patient Summaries
ALTER TABLE public.patient_summaries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own summaries"
    ON public.patient_summaries FOR SELECT
    USING (auth.uid() = patient_id);

CREATE POLICY "Users can insert own summaries"
    ON public.patient_summaries FOR INSERT
    WITH CHECK (auth.uid() = patient_id);

-- Share Tokens
ALTER TABLE public.share_tokens ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own tokens"
    ON public.share_tokens FOR SELECT
    USING (auth.uid() = patient_id);

CREATE POLICY "Users can create own tokens"
    ON public.share_tokens FOR INSERT
    WITH CHECK (auth.uid() = patient_id);

-- Public read for valid tokens (used by share/{token} endpoint via service role)
-- The service role key bypasses RLS, so the public share endpoint works.

-- Shared Files
ALTER TABLE public.shared_files ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view files shared with them"
    ON public.shared_files FOR SELECT
    USING (
        auth.uid() = sender_id
        OR recipient_email = (
            SELECT email FROM auth.users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can send files"
    ON public.shared_files FOR INSERT
    WITH CHECK (auth.uid() = sender_id);

CREATE POLICY "Users can mark files as read"
    ON public.shared_files FOR UPDATE
    USING (
        recipient_email = (
            SELECT email FROM auth.users WHERE id = auth.uid()
        )
    );

-- ──────────────────────────────────────────────
-- STORAGE BUCKETS
-- (Run these separately if needed — Supabase may
--  require bucket creation via Dashboard or API)
-- ──────────────────────────────────────────────
INSERT INTO storage.buckets (id, name, public)
VALUES
    ('prescriptions', 'prescriptions', false),
    ('voice-notes', 'voice-notes', false),
    ('generated-files', 'generated-files', false)
ON CONFLICT (id) DO NOTHING;

-- Storage policies: users can upload to their own folder
CREATE POLICY "Users can upload prescriptions"
    ON storage.objects FOR INSERT
    WITH CHECK (
        bucket_id = 'prescriptions'
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can view own prescriptions"
    ON storage.objects FOR SELECT
    USING (
        bucket_id = 'prescriptions'
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can upload voice notes"
    ON storage.objects FOR INSERT
    WITH CHECK (
        bucket_id = 'voice-notes'
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can view own voice notes"
    ON storage.objects FOR SELECT
    USING (
        bucket_id = 'voice-notes'
        AND auth.uid()::text = (storage.foldername(name))[1]
    );

-- Generated files are managed by the service role (server-side),
-- so no user-facing policies needed.  The service role bypasses RLS.
