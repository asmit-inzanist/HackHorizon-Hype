"""
Supabase client singletons.

- `anon_client`    → used for user-scoped operations (respects RLS)
- `service_client` → used for server-side admin operations (bypasses RLS)
"""

from supabase import create_client, Client
from core.config import get_settings

_anon_client: Client | None = None
_service_client: Client | None = None


def get_anon_client() -> Client:
    """Return the Supabase client using the anon key (RLS-aware)."""
    global _anon_client
    if _anon_client is None:
        s = get_settings()
        _anon_client = create_client(s.SUPABASE_URL, s.SUPABASE_ANON_KEY)
    return _anon_client


def get_service_client() -> Client:
    """Return the Supabase client using the service role key (bypasses RLS)."""
    global _service_client
    if _service_client is None:
        s = get_settings()
        _service_client = create_client(s.SUPABASE_URL, s.SUPABASE_SERVICE_ROLE_KEY)
    return _service_client
