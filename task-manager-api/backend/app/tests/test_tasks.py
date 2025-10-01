import os
import contextlib
import pytest
from fastapi.testclient import TestClient


@contextlib.contextmanager
def _patched_settings(tmp_path):
	from app.core.config import get_settings
	# Point to a unique temp sqlite database file per test session
	db_path = tmp_path / "test_tasks.db"
	os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"
	# Clear the settings cache so the test DB URL is picked up
	get_settings.cache_clear()  # type: ignore[attr-defined]
	try:
		yield
	finally:
		# Cleanup: clear cache to avoid leaking config to other tests
		get_settings.cache_clear()  # type: ignore[attr-defined]


@pytest.fixture()
def client(tmp_path):
	with _patched_settings(tmp_path):
		# Import after settings are patched so engine/app use the test DB
		from app.main import app
		with TestClient(app) as c:
			yield c


def test_create_task(client: TestClient):
	payload = {"title": "Write unit tests"}
	resp = client.post("/api/v1/tasks/", json=payload)
	assert resp.status_code == 201
	data = resp.json()
	assert data["id"] > 0
	assert data["title"] == payload["title"]
	assert data["is_completed"] is False


def test_list_tasks(client: TestClient):
	# Ensure at least one task exists
	client.post("/api/v1/tasks/", json={"title": "Task A"})
	client.post("/api/v1/tasks/", json={"title": "Task B"})
	resp = client.get("/api/v1/tasks/")
	assert resp.status_code == 200
	tasks = resp.json()
	assert isinstance(tasks, list)
	assert len(tasks) >= 2
	# Ensure only fields we expect are present
	for t in tasks:
		assert {"id", "title", "is_completed", "created_at", "updated_at"}.issubset(t.keys())


def test_update_task_and_get(client: TestClient):
	created = client.post("/api/v1/tasks/", json={"title": "Edit me", "description": "old"}).json()
	task_id = created["id"]
	resp = client.put(f"/api/v1/tasks/{task_id}", json={"title": "Edited", "description": "new"})
	assert resp.status_code == 200
	updated = resp.json()
	assert updated["title"] == "Edited"
	assert updated["description"] == "new"
	# Get by id
	got = client.get(f"/api/v1/tasks/{task_id}")
	assert got.status_code == 200
	assert got.json()["id"] == task_id


def test_toggle_complete_filtering(client: TestClient):
	created = client.post("/api/v1/tasks/", json={"title": "Complete me"}).json()
	task_id = created["id"]
	# Mark complete
	resp = client.put(f"/api/v1/tasks/{task_id}", json={"is_completed": True})
	assert resp.status_code == 200
	assert resp.json()["is_completed"] is True
	# Filter by is_completed
	only_completed = client.get("/api/v1/tasks/?is_completed=true")
	assert only_completed.status_code == 200
	assert any(t["id"] == task_id for t in only_completed.json())
	only_open = client.get("/api/v1/tasks/?is_completed=false")
	assert only_open.status_code == 200
	assert all(t["is_completed"] is False for t in only_open.json())


def test_delete_task(client: TestClient):
	created = client.post("/api/v1/tasks/", json={"title": "Delete me"}).json()
	task_id = created["id"]
	resp = client.delete(f"/api/v1/tasks/{task_id}")
	assert resp.status_code == 204
	# Confirm 404 afterwards
	not_found = client.get(f"/api/v1/tasks/{task_id}")
	assert not_found.status_code == 404
