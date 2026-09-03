import hashlib
import hmac


def generate_csrf_token(session_id: str, secret: str) -> str:
    """Synchronizer-token pattern: token = HMAC(secret, session_id).
    Stateless - verified by recomputing, no server-side storage needed."""
    return hmac.new(
        secret.encode(), session_id.encode(), hashlib.sha256
    ).hexdigest()


def verify_csrf_token(session_id: str, token: str, secret: str) -> bool:
    expected = generate_csrf_token(session_id, secret)
    return hmac.compare_digest(expected, token)
