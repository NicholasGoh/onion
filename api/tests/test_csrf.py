from app.data.csrf import generate_csrf_token, verify_csrf_token


def test_verify_accepts_matching_token():
    token = generate_csrf_token("session-1", "secret")
    assert verify_csrf_token("session-1", token, "secret") is True


def test_verify_rejects_tampered_token():
    token = generate_csrf_token("session-1", "secret")
    tampered = token[:-1] + ("0" if token[-1] != "0" else "1")
    assert verify_csrf_token("session-1", tampered, "secret") is False


def test_verify_rejects_token_for_different_session():
    token = generate_csrf_token("session-1", "secret")
    assert verify_csrf_token("session-2", token, "secret") is False


def test_verify_rejects_token_signed_with_different_secret():
    token = generate_csrf_token("session-1", "secret")
    assert verify_csrf_token("session-1", token, "other-secret") is False
