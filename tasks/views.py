import logging
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .db import get_connection
from django.contrib import messages

logger = logging.getLogger(__name__)

def index(request):
    conn = None
    try:
        logger.info("Fetching all tasks from database.")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        conn.commit()
        logger.info(f"Fetched {len(tasks)} tasks successfully.")
        return render(request, 'tasks/index.html', {'tasks': tasks})
    except Exception as e:
        logger.exception("Error while fetching tasks.")
        return HttpResponse(f"An error occurred: {e}", status=500)
    finally:
        if conn:
            conn.close()

def add_task_page(request):
    conn = None
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            due_date = request.POST.get("due_date")

            logger.info(f"Adding new task: {title}")

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                (title, description, due_date),
            )
            conn.commit()
            logger.info("Task added successfully.")
            messages.success(request, "Task added successfully.")
            return redirect('/')
        logger.warning("Invalid HTTP method used on add_task_page.")
        messages.error(request, "Invalid HTTP method.")
        return redirect('/')
    except Exception as e:
        logger.exception("Error while adding task.")
        messages.error(request, f"An error occurred: {e}")
        return redirect('/')
    finally:
        if conn:
            conn.close()

def task_list_api(request):
    conn = None
    try:
        if request.method == "GET":
            logger.info("API call: Get all tasks.")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            conn.commit()
            tasks = cursor.fetchall()
            tasks_list = [
                {
                    "id": task[0],
                    "title": task[1],
                    "description": task[2],
                    "due_date": task[3],
                    "status": task[4],
                    "created_at": task[5],
                    "updated_at": task[6],
                }
                for task in tasks
            ]
            logger.info(f"Returning {len(tasks_list)} tasks via API.")
            return JsonResponse({"message": "Tasks list retrieve successfully.", "data": tasks_list}, safe=False, status=200)
        else:
            logger.warning("Invalid HTTP method used on task_list_api.")
            return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    except Exception as e:
        logger.exception("Error while fetching tasks in API.")
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if conn:
            conn.close()

def task_detail_api(request, task_id):
    conn = None
    try:
        if request.method == "GET":
            logger.info(f"API call: Get task details for ID {task_id}.")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            task = cursor.fetchone()
            if task:
                task_data = {
                    "id": task[0],
                    "title": task[1],
                    "description": task[2],
                    "due_date": task[3],
                    "status": task[4],
                    "created_at": task[5],
                    "updated_at": task[6],
                }
                logger.info(f"Task {task_id} found and returned.")
                return JsonResponse({"message": "Task details retrieve successfully.", "data": task_data}, safe=False, status=200)
            else:
                logger.warning(f"Task with ID {task_id} not found.")
                return JsonResponse({"error": "Task not found"}, status=404)
        else:
            logger.warning(f"Invalid HTTP method used for task_detail_api for task {task_id}.")
            return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    except Exception as e:
        logger.exception(f"Internal server error while fetching task {task_id}.")
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
    finally:
        if conn:
            conn.close()

def complete_task(request, task_id):
    conn = None
    try:
        if request.method == "POST":
            logger.info(f"Marking task {task_id} as completed.")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status='completed', updated_at=CURRENT_TIMESTAMP WHERE id=?", (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Task with ID {task_id} not found while completing.")
                messages.error(request, "Task not found.")
                return HttpResponse("Task not found", status=404)
            logger.info(f"Task {task_id} marked as completed.")
            messages.success(request, "Task marked as completed.")
            return redirect('/')
        else:
            logger.warning("Invalid HTTP method used on complete_task.")
            messages.error(request, "Invalid HTTP method.")
            return redirect('/')
    except Exception as e:
        logger.exception(f"Error while completing task {task_id}.")
        messages.error(request, f"An error occurred: {e}")
        return redirect('/')
    finally:
        if conn:
            conn.close()

def delete_task(request, task_id):
    conn = None
    try:
        if request.method == "POST":
            logger.info(f"Deleting task with ID {task_id}.")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Task with ID {task_id} not found for deletion.")
                messages.error(request, "Task not found.")
                return redirect('/')
            logger.info(f"Task {task_id} deleted successfully.")
            messages.success(request, "Task deleted successfully.")
            return redirect('/')
        else:
            logger.warning("Invalid HTTP method used on delete_task.")
            messages.error(request, "Invalid HTTP method.")
            return redirect('/')
    except Exception as e:
        logger.exception(f"Error while deleting task {task_id}.")
        messages.error(request, f"Internal server error: {e}")
        return redirect('/')
    finally:
        if conn:
            conn.close()