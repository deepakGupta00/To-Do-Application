import pytest
from django.urls import reverse
from django.test import Client
import sqlite3
import os
from tasks.db import get_connection  

pytestmark = pytest.mark.django_db

client = Client()

def insert_task(title="Sample Task", description="Testing task", due_date="2025-09-12"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                   (title, description, due_date))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def test_index_page_loads():
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert b"Task" in response.content 

def test_add_task_post_redirects():
    response = client.post(reverse('task_entry'), {
        "title": "New Task",
        "description": "pytest task",
        "due_date": "2025-09-15"
    })
    assert response.status_code == 302  

def test_task_list_api_returns_json():
    insert_task()
    response = client.get(reverse('task_list_api'))
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)

def test_task_detail_api_returns_single_task():
    task_id = insert_task()
    response = client.get(reverse('task_detail_api', args=[task_id]))
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"]["id"] == task_id

def test_complete_task_marks_completed():
    task_id = insert_task()
    response = client.post(reverse('complete_task', args=[task_id]))
    assert response.status_code == 302 

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tasks WHERE id=?", (task_id,))
    status = cursor.fetchone()[0]
    conn.close()
    assert status == "completed"

def test_delete_task_removes_it():
    task_id = insert_task()
    response = client.post(reverse('delete_task', args=[task_id]))
    assert response.status_code == 302

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE id=?", (task_id,))
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 0
