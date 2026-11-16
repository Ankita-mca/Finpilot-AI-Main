"""
Authentication endpoint tests: login, logout, me, and session behaviour.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Organization, Membership, AuditLog

User = get_user_model()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def user_and_org(db):
    user = User.objects.create_user(
        username="logout_test@example.com",
        email="logout_test@example.com",
        password="TestPass1!",
        first_name="Test",
        last_name="User",
    )
    org = Organization.objects.create(name="Logout Test Org", default_currency="INR")
    Membership.objects.create(organization=org, user=user, role=Membership.Role.OWNER)
    return user, org


@pytest.fixture
def authenticated_client(client, user_and_org):
    """Django test client with a logged-in session."""
    user, org = user_and_org
    client.force_login(user)
    return client, user, org


# ---------------------------------------------------------------------------
# Logout endpoint
# ---------------------------------------------------------------------------

class TestLogout:
    def test_logout_returns_200_for_authenticated_user(self, authenticated_client):
        c, user, org = authenticated_client
        res = c.post("/api/v1/auth/logout/", content_type="application/json")
        assert res.status_code == 200
        data = res.json()
        assert data["detail"] == "Signed out"

    def test_logout_returns_request_id_for_authenticated_user(self, authenticated_client):
        c, user, org = authenticated_client
        res = c.post("/api/v1/auth/logout/", content_type="application/json")
        data = res.json()
        assert "request_id" in data
        assert len(data["request_id"]) == 36  # UUID4 with hyphens

    def test_logout_destroys_session(self, authenticated_client):
        c, user, org = authenticated_client
        # Verify /me/ works before logout
        res_before = c.get("/api/v1/auth/me/", content_type="application/json")
        assert res_before.status_code == 200

        c.post("/api/v1/auth/logout/", content_type="application/json")

        # After logout, /me/ must return 403 or 401
        res_after = c.get("/api/v1/auth/me/", content_type="application/json")
        assert res_after.status_code in (401, 403)

    def test_logout_writes_audit_log(self, authenticated_client):
        c, user, org = authenticated_client
        before_count = AuditLog.objects.filter(action="auth.logout", actor=user).count()
        c.post("/api/v1/auth/logout/", content_type="application/json")
        after_count = AuditLog.objects.filter(action="auth.logout", actor=user).count()
        assert after_count == before_count + 1

    def test_logout_audit_log_has_correct_fields(self, authenticated_client):
        c, user, org = authenticated_client
        c.post("/api/v1/auth/logout/", content_type="application/json")
        log = AuditLog.objects.filter(action="auth.logout", actor=user).latest("created_at")
        assert log.entity_type == "user"
        assert log.entity_id == str(user.id)
        assert user.email in log.summary
        # Tokens/passwords must not appear in the summary
        assert "password" not in log.summary.lower()
        assert "token" not in log.summary.lower()

    def test_logout_audit_log_has_request_id(self, authenticated_client):
        c, user, org = authenticated_client
        res = c.post("/api/v1/auth/logout/", content_type="application/json")
        request_id = res.json()["request_id"]
        log = AuditLog.objects.filter(action="auth.logout", actor=user).latest("created_at")
        assert log.request_id == request_id

    def test_logout_is_idempotent_for_unauthenticated_request(self, client):
        """Calling logout when not logged in must not crash (200 or 403 acceptable)."""
        res = client.post("/api/v1/auth/logout/", content_type="application/json")
        # Session auth will allow the call (AllowAny not set, but Django won't crash)
        assert res.status_code in (200, 403)

    def test_old_session_gets_401_on_protected_endpoints(self, authenticated_client):
        """After logout, the session cookie is invalid so protected routes return 401/403."""
        c, user, org = authenticated_client
        c.post("/api/v1/auth/logout/", content_type="application/json")
        res = c.get("/api/v1/auth/me/")
        assert res.status_code in (401, 403)

    def test_logout_does_not_log_credentials(self, authenticated_client):
        """Confirm audit log never contains password-like content."""
        c, user, org = authenticated_client
        c.post("/api/v1/auth/logout/", content_type="application/json")
        log = AuditLog.objects.filter(action="auth.logout", actor=user).latest("created_at")
        sensitive = ["password", "secret", "token", "key", "hash"]
        for word in sensitive:
            assert word not in log.summary.lower(), f"Audit log leaks '{word}'"


# ---------------------------------------------------------------------------
# Login endpoint
# ---------------------------------------------------------------------------

class TestLogin:
    def test_login_with_valid_credentials(self, db, user_and_org):
        user, org = user_and_org
        from django.test import Client
        c = Client()
        res = c.post(
            "/api/v1/auth/login/",
            data={"username": "logout_test@example.com", "password": "TestPass1!"},
            content_type="application/json",
        )
        assert res.status_code == 200
        assert res.json()["detail"] == "Signed in"

    def test_login_with_wrong_password(self, db, user_and_org):
        from django.test import Client
        c = Client()
        res = c.post(
            "/api/v1/auth/login/",
            data={"username": "logout_test@example.com", "password": "WrongPass!"},
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_me_requires_authentication(self, client):
        res = client.get("/api/v1/auth/me/")
        assert res.status_code in (401, 403)


# ---------------------------------------------------------------------------
# Google Auth endpoint
# ---------------------------------------------------------------------------

class TestGoogleAuth:
    def test_google_auth_missing_token(self, client):
        res = client.post("/api/v1/auth/google/", data={}, content_type="application/json")
        assert res.status_code == 400
        assert "Google ID token is required" in res.json()["detail"]

    def test_google_auth_missing_client_id(self, client, settings):
        settings.GOOGLE_CLIENT_ID = ""
        res = client.post(
            "/api/v1/auth/google/",
            data={"id_token": "some.token.value"},
            content_type="application/json",
        )
        assert res.status_code == 500
        assert "GOOGLE_CLIENT_ID" in res.json()["detail"]

    def test_google_auth_invalid_token(self, client, settings):
        settings.GOOGLE_CLIENT_ID = "mock-google-client-id.apps.googleusercontent.com"
        from unittest.mock import patch
        with patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Token expired")):
            res = client.post(
                "/api/v1/auth/google/",
                data={"id_token": "invalid.or.expired.token"},
                content_type="application/json",
            )
            assert res.status_code == 400
            assert "Invalid or expired Google token" in res.json()["detail"]

    def test_google_auth_unverified_email(self, client, settings):
        settings.GOOGLE_CLIENT_ID = "mock-google-client-id.apps.googleusercontent.com"
        from unittest.mock import patch
        fake_payload = {
            "email": "unverified@example.com",
            "email_verified": False,
            "name": "Unverified User",
        }
        with patch("google.oauth2.id_token.verify_oauth2_token", return_value=fake_payload):
            res = client.post(
                "/api/v1/auth/google/",
                data={"id_token": "valid.token.unverified.email"},
                content_type="application/json",
            )
            assert res.status_code == 400
            assert "email is not verified" in res.json()["detail"]

    def test_google_auth_new_user_registration(self, db, client, settings):
        settings.GOOGLE_CLIENT_ID = "mock-google-client-id.apps.googleusercontent.com"
        from unittest.mock import patch
        fake_payload = {
            "email": "newgoogleuser@example.com",
            "email_verified": True,
            "given_name": "New",
            "family_name": "GoogleUser",
            "name": "New GoogleUser",
        }
        with patch("google.oauth2.id_token.verify_oauth2_token", return_value=fake_payload):
            res = client.post(
                "/api/v1/auth/google/",
                data={"id_token": "mock.google.id.token"},
                content_type="application/json",
            )
            assert res.status_code == 200
            data = res.json()
            assert data["created"] is True
            assert data["has_organization"] is False
            assert data["user"]["email"] == "newgoogleuser@example.com"
            assert data["user"]["full_name"] == "New GoogleUser"
            # Verify user exists in DB and has unusable password
            user = User.objects.get(email="newgoogleuser@example.com")
            assert not user.has_usable_password()
            # Verify session works
            me_res = client.get("/api/v1/auth/me/")
            assert me_res.status_code == 200

    def test_google_auth_existing_user_login(self, db, client, settings, user_and_org):
        user, org = user_and_org
        settings.GOOGLE_CLIENT_ID = "mock-google-client-id.apps.googleusercontent.com"
        from unittest.mock import patch
        fake_payload = {
            "email": user.email,
            "email_verified": True,
            "given_name": "Test",
            "family_name": "User",
            "name": "Test User",
        }
        with patch("google.oauth2.id_token.verify_oauth2_token", return_value=fake_payload):
            res = client.post(
                "/api/v1/auth/google/",
                data={"id_token": "mock.google.id.token"},
                content_type="application/json",
            )
            assert res.status_code == 200
            data = res.json()
            assert data["created"] is False
            assert data["has_organization"] is True
            assert len(data["user"]["organizations"]) == 1
            assert data["user"]["organizations"][0]["id"] == str(org.id)
