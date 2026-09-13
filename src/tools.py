"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "add_todo",
        "description": "Thêm một công việc mới vào danh sách to-do của người dùng.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Nội dung công việc cần thêm."
                },
                "due_date": {
                    "type": "string",
                    "description": "Ngày đến hạn theo YYYY-MM-DD, nếu người dùng có cung cấp."
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Mức ưu tiên; mặc định là medium."
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "create_calendar_reminder",
        "description": (
            "Tạo sự kiện nhắc việc trên Google Calendar cho một công việc cụ thể."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Tên công việc/sự kiện cần nhắc. Ví dụ: 'Nộp báo cáo Day 03'."
                },
                "start_datetime": {
                    "type": "string",
                    "description": (
                        "Thời điểm bắt đầu theo ISO 8601 có múi giờ. "
                        "Ví dụ: '2026-09-20T19:00:00+07:00'."
                    )
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Thời lượng sự kiện tính bằng phút. Ví dụ: 60."
                },
                "reminder_minutes": {
                    "type": "integer",
                    "description": "Số phút nhắc trước thời điểm bắt đầu. Ví dụ: 30."
                },
                "description": {
                    "type": "string",
                    "description": "Ghi chú chi tiết cho công việc, nếu có."
                }
            },
            "required": [
                "title",
                "start_datetime",
                "duration_minutes",
                "reminder_minutes"
            ]
        }
    },
    {
        "name": "get_pending_todos",
        "description": (
            "Tra cứu danh sách công việc chưa hoàn thành, có thể lọc theo "
            "ngày đến hạn hoặc mức độ ưu tiên."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "due_date": {
                    "type": "string",
                    "description": (
                        "Ngày đến hạn cần lọc theo định dạng YYYY-MM-DD. "
                        "Ví dụ: '2026-09-20'. Bỏ trống nếu lấy tất cả việc chưa hoàn thành."
                    )
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": (
                        "Mức ưu tiên cần lọc: low, medium hoặc high. "
                        "Bỏ trống nếu không cần lọc."
                    )
                }
            },
            "required": []
        }
    },
    {
        "name": "update_todo_status",
        "description": "Cập nhật trạng thái của một công việc theo mã định danh to-do.",
        "parameters": {
            "type": "object",
            "properties": {
                "todo_id": {
                    "type": "string",
                    "description": "Mã công việc, ví dụ TODO-001."
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed"],
                    "description": "Trạng thái mới của công việc."
                }
            },
            "required": ["todo_id", "status"]
        }
    },
    {
        "name": "check_calendar_availability",
        "description": "Kiểm tra các khung giờ trống trên Google Calendar trong một khoảng thời gian của một ngày.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Ngày cần kiểm tra theo YYYY-MM-DD."
                },
                "start_time": {
                    "type": "string",
                    "description": "Bắt đầu khoảng cần kiểm tra theo HH:MM, ví dụ 14:00."
                },
                "end_time": {
                    "type": "string",
                    "description": "Kết thúc khoảng cần kiểm tra theo HH:MM, ví dụ 17:00."
                }
            },
            "required": ["date", "start_time", "end_time"]
        }
    },
    {
        "name": "list_calendar_events",
        "description": (
            "Liệt kê các sự kiện đã có trên Google Calendar trong một ngày cụ thể, "
            "bao gồm tên sự kiện và thời gian bắt đầu/kết thúc. Dùng khi người dùng hỏi "
            "hôm đó có lịch gì hoặc lịch nào."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Ngày cần xem lịch theo định dạng YYYY-MM-DD."
                }
            },
            "required": ["date"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_TODOS = [
    {"id": "TODO-001", "title": "Hoàn thiện báo cáo Day 03", "due_date": "2026-09-20", "priority": "high", "status": "pending"},
    {"id": "TODO-002", "title": "Kiểm tra Waterfall Trace Log", "due_date": "2026-09-19", "priority": "medium", "status": "pending"},
    {"id": "TODO-003", "title": "Ôn lại bài ReAct Agent", "due_date": "2026-09-18", "priority": "low", "status": "completed"},
]

GOOGLE_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def execute_get_pending_todos(due_date: str = None, priority: str = None) -> str:
    """Tra cứu công việc đang pending từ dữ liệu mô phỏng của bài lab."""
    todos = [todo for todo in MOCK_TODOS if todo["status"] == "pending"]
    if due_date:
        todos = [todo for todo in todos if todo["due_date"] == due_date]
    if priority:
        todos = [todo for todo in todos if todo["priority"] == priority.lower()]

    return json.dumps({
        "status": "SUCCESS",
        "count": len(todos),
        "todos": todos,
        "message": f"Tìm thấy {len(todos)} công việc chưa hoàn thành."
    }, ensure_ascii=False)


def execute_add_todo(
    title: str, due_date: str = None, priority: str = "medium"
) -> str:
    """Thêm to-do vào danh sách mô phỏng trong suốt phiên chạy hiện tại."""
    if priority not in {"low", "medium", "high"}:
        return json.dumps({"status": "EXECUTION_ERROR", "error": "priority không hợp lệ."}, ensure_ascii=False)

    todo = {
        "id": f"TODO-{len(MOCK_TODOS) + 1:03d}",
        "title": title,
        "due_date": due_date or "Chưa đặt hạn",
        "priority": priority,
        "status": "pending",
    }
    MOCK_TODOS.append(todo)
    return json.dumps({
        "status": "SUCCESS",
        "todo": todo,
        "message": f"Đã thêm công việc '{title}' vào danh sách to-do.",
    }, ensure_ascii=False)


def execute_update_todo_status(todo_id: str, status: str) -> str:
    """Cập nhật trạng thái to-do hoặc trả NOT_FOUND nếu mã không tồn tại."""
    todo = next((item for item in MOCK_TODOS if item["id"] == todo_id.upper()), None)
    if not todo:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy công việc có mã '{todo_id}'.",
        }, ensure_ascii=False)
    todo["status"] = status
    return json.dumps({
        "status": "SUCCESS",
        "todo": todo,
        "message": f"Đã cập nhật công việc '{todo['title']}' thành {status}.",
    }, ensure_ascii=False)


def _get_calendar_service():
    """Lấy Calendar service; lần đầu mở trình duyệt để người dùng cấp OAuth consent."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError(
            "Thiếu thư viện Google Calendar. Hãy chạy: pip install -r requirements.txt"
        ) from exc

    credentials_path = Path(os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json"))
    token_path = Path(os.getenv("GOOGLE_TOKEN_PATH", "token.json"))
    if not credentials_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {credentials_path}. Tải OAuth Desktop credentials từ Google Cloud "
            "và lưu file này tại thư mục gốc dự án."
        )

    credentials = None
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(token_path, GOOGLE_CALENDAR_SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), GOOGLE_CALENDAR_SCOPES
            )
            print("Mở URL OAuth bên dưới trong trình duyệt để cấp quyền Google Calendar.")
            credentials = flow.run_local_server(port=0, open_browser=False)
        token_path.write_text(credentials.to_json(), encoding="utf-8")

    return build("calendar", "v3", credentials=credentials)


def execute_check_calendar_availability(date: str, start_time: str, end_time: str) -> str:
    """Tìm khoảng trống trong một khung giờ bằng các event hiện có trên Calendar."""
    try:
        timezone_name = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "Asia/Ho_Chi_Minh")
        requested_start = datetime.fromisoformat(f"{date}T{start_time}:00+07:00")
        requested_end = datetime.fromisoformat(f"{date}T{end_time}:00+07:00")
        if requested_start >= requested_end:
            raise ValueError("start_time phải sớm hơn end_time.")

        service = _get_calendar_service()
        events = service.events().list(
            calendarId=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            timeMin=requested_start.isoformat(),
            timeMax=requested_end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute().get("items", [])

        slots, cursor = [], requested_start
        for event in events:
            event_start_text = event.get("start", {}).get("dateTime")
            event_end_text = event.get("end", {}).get("dateTime")
            if not event_start_text or not event_end_text:
                continue
            event_start = datetime.fromisoformat(event_start_text.replace("Z", "+00:00"))
            event_end = datetime.fromisoformat(event_end_text.replace("Z", "+00:00"))
            if event_start > cursor:
                slots.append({"start_datetime": cursor.isoformat(), "end_datetime": min(event_start, requested_end).isoformat()})
            cursor = max(cursor, event_end)
        if cursor < requested_end:
            slots.append({"start_datetime": cursor.isoformat(), "end_datetime": requested_end.isoformat()})

        return json.dumps({
            "status": "SUCCESS",
            "date": date,
            "timezone": timezone_name,
            "available_slots": slots,
            "message": f"Tìm thấy {len(slots)} khung giờ trống.",
        }, ensure_ascii=False)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        return json.dumps({"status": "CONFIGURATION_REQUIRED", "message": str(exc)}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(exc)}, ensure_ascii=False)


def execute_list_calendar_events(date: str) -> str:
    """Liệt kê đầy đủ event trên Google Calendar của một ngày."""
    try:
        day_start = datetime.fromisoformat(f"{date}T00:00:00+07:00")
        day_end = day_start + timedelta(days=1)
        service = _get_calendar_service()
        calendar_events = service.events().list(
            calendarId=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            timeMin=day_start.isoformat(),
            timeMax=day_end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        ).execute().get("items", [])

        events = []
        for event in calendar_events:
            start = event.get("start", {})
            end = event.get("end", {})
            events.append({
                "id": event.get("id"),
                "summary": event.get("summary", "(Không có tiêu đề)"),
                "start_datetime": start.get("dateTime", start.get("date")),
                "end_datetime": end.get("dateTime", end.get("date")),
            })

        return json.dumps({
            "status": "SUCCESS",
            "date": date,
            "count": len(events),
            "events": events,
            "message": f"Tìm thấy {len(events)} sự kiện vào ngày {date}.",
        }, ensure_ascii=False)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        return json.dumps({"status": "CONFIGURATION_REQUIRED", "message": str(exc)}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(exc)}, ensure_ascii=False)


def execute_create_calendar_reminder(
    title: str,
    start_datetime: str,
    duration_minutes: int,
    reminder_minutes: int,
    description: str = "",
) -> str:
    """Tạo event thật trên Google Calendar chính, kèm popup reminder."""
    try:
        start = datetime.fromisoformat(start_datetime.replace("Z", "+00:00"))
        if start.tzinfo is None:
            raise ValueError("start_datetime phải có múi giờ, ví dụ +07:00.")
        if duration_minutes <= 0 or reminder_minutes < 0:
            raise ValueError("duration_minutes phải > 0 và reminder_minutes phải >= 0.")

        end = start + timedelta(minutes=duration_minutes)
        timezone_name = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "Asia/Ho_Chi_Minh")
        event_body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start.isoformat(), "timeZone": timezone_name},
            "end": {"dateTime": end.isoformat(), "timeZone": timezone_name},
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "popup", "minutes": reminder_minutes}],
            },
        }
        service = _get_calendar_service()
        event = service.events().insert(
            calendarId=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            body=event_body,
        ).execute()
        return json.dumps({
            "status": "SUCCESS",
            "message": "Đã tạo lịch nhắc trên Google Calendar.",
            "event": {
                "id": event.get("id"),
                "summary": event.get("summary"),
                "start_time": event.get("start", {}).get("dateTime"),
                "duration": f"{duration_minutes} phút",
                "html_link": event.get("htmlLink"),
            },
        }, ensure_ascii=False)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        return json.dumps({"status": "CONFIGURATION_REQUIRED", "message": str(exc)}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(exc)}, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "add_todo": execute_add_todo,
    "get_pending_todos": execute_get_pending_todos,
    "update_todo_status": execute_update_todo_status,
    "check_calendar_availability": execute_check_calendar_availability,
    "list_calendar_events": execute_list_calendar_events,
    "create_calendar_reminder": execute_create_calendar_reminder,
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
