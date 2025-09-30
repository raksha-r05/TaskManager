#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


BASE_URL = os.getenv("TODO_API_BASE_URL", "http://localhost:8000")


def pretty_print(title: str, data: Any) -> None:
	print(f"\n=== {title} ===")
	if isinstance(data, (dict, list)):
		print(json.dumps(data, indent=2, sort_keys=True, default=str))
	else:
		print(str(data))


def create_task(
	title: str,
	description: Optional[str] = None,
	is_completed: Optional[bool] = None,
	priority: Optional[int] = None,
	due_date: Optional[datetime] = None,
) -> Dict[str, Any]:
	url = f"{BASE_URL}/tasks"
	payload: Dict[str, Any] = {"title": title}
	if description is not None:
		payload["description"] = description
	if is_completed is not None:
		payload["is_completed"] = is_completed
	if priority is not None:
		payload["priority"] = priority
	if due_date is not None:
		payload["due_date"] = due_date.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

	response = requests.post(url, json=payload, timeout=10)
	response.raise_for_status()
	return response.json()


def list_tasks() -> list[Dict[str, Any]]:
	url = f"{BASE_URL}/tasks"
	response = requests.get(url, timeout=10)
	response.raise_for_status()
	return response.json()


def get_task(task_id: int) -> Dict[str, Any]:
	url = f"{BASE_URL}/tasks/{task_id}"
	response = requests.get(url, timeout=10)
	response.raise_for_status()
	return response.json()


def update_task(task_id: int, **fields: Any) -> Dict[str, Any]:
	url = f"{BASE_URL}/tasks/{task_id}"
	# Clean None values and format datetime
	clean_fields: Dict[str, Any] = {}
	for key, value in fields.items():
		if value is None:
			continue
		if isinstance(value, datetime):
			clean_fields[key] = value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
		else:
			clean_fields[key] = value
	response = requests.put(url, json=clean_fields, timeout=10)
	response.raise_for_status()
	return response.json()


def delete_task(task_id: int) -> int:
	url = f"{BASE_URL}/tasks/{task_id}"
	response = requests.delete(url, timeout=10)
	# Expect 204 No Content
	if response.status_code not in (200, 202, 204):
		response.raise_for_status()
	return response.status_code


def demo_sequence() -> None:
	pretty_print("Health", requests.get(f"{BASE_URL}/", timeout=5).json())

	pretty_print("Initial tasks", list_tasks())

	created = create_task(
		title="Buy groceries",
		description="Milk, eggs, bread",
		priority=1,
		due_date=datetime.now(timezone.utc).replace(microsecond=0),
	)
	pretty_print("Created task", created)

	created_id = int(created["id"]) if "id" in created else created.get("id")
	pretty_print("Get task", get_task(created_id))

	updated = update_task(created_id, title="Buy groceries and fruits", is_completed=True)
	pretty_print("Updated task", updated)

	status_code = delete_task(created_id)
	pretty_print("Delete status", status_code)

	pretty_print("Final tasks", list_tasks())


if __name__ == "__main__":
	try:
		demo_sequence()
	except requests.HTTPError as http_err:
		print("HTTP error:", http_err)
	except Exception as exc:
		print("Unexpected error:", exc)


