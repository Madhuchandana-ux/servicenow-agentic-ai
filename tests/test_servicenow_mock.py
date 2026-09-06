from src import servicenow


class DummyResponse:
    def __init__(self, code=201, payload=None):
        self.status_code = code
        self._payload = payload or {"result": {"number": "INC0001", "sys_id": "abc123"}}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")


class DummySession:
    def post(self, *args, **kwargs):
        return DummyResponse()


def test_create_incident_monkeypatch(monkeypatch):
    monkeypatch.setenv("SERVICENOW_INSTANCE", "https://example.service-now.com")
    monkeypatch.setenv("SERVICENOW_USERNAME", "admin")
    monkeypatch.setenv("SERVICENOW_PASSWORD", "pass")

    monkeypatch.setattr(servicenow, "_get_session", lambda: DummySession())

    result = servicenow.create_incident(
        short_description="Test",
        description="desc",
        category="Network",
        priority="High",
        assignment_group="Network Support",
    )

    assert result["success"] is True
    assert result["number"] == "INC0001"
