# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Đinh Hoàng Đức<br>
> **Mã Sinh Viên / Mã Học viên:** 2A202602795
> **Chủ đề Lựa chọn:** Trợ lý đặt lịch cá nhân, đồng bộ hóa lịch và tra cứu lịch qua Google Calendar.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | **4 / 5** | Với yêu cầu đặt lịch, Agent cần hiểu thời gian, kiểm tra khung giờ trống, sau đó mới tạo sự kiện. Luồng tra cứu lịch cũng cần gọi công cụ rồi tổng hợp kết quả cho người dùng. |
| **2. Tool Interaction** | **5 / 5** | Bài toán phải đọc và ghi dữ liệu trên Google Calendar, đồng thời thao tác danh sách to-do. LLM không thể tự biết dữ liệu lịch cá nhân nên cần gọi Tool qua MCP Server. |
| **3. Dynamic Decision** | **5 / 5** | Hành động kế tiếp phụ thuộc vào Observation: nếu có khung giờ trống thì tạo lịch; nếu không có hoặc Tool trả lỗi thì Agent thông báo lại thay vì tự bịa kết quả. |
| **4. Long Horizon Goal** | **3 / 5** | Trong một phiên xử lý, Agent giữ mục tiêu từ yêu cầu ban đầu đến câu trả lời cuối. Hệ thống hiện chưa có memory bền vững hoặc cơ chế lập kế hoạch dài hạn giữa nhiều phiên. |
| **TỔNG ĐIỂM AGENTIC FIT** | **17 / 20** | *Bài toán phù hợp để triển khai Agentic System vì vượt ngưỡng 12/20 và cần Tool use, quan sát dữ liệu thực tế và quyết định theo kết quả.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dưới đây là đoạn trace tiêu biểu của TC04. Gemini gọi `check_calendar_availability`, nhận Observation về khung giờ trống, rồi gọi `create_calendar_reminder` để đặt lịch ở giờ đầu tiên phù hợp.

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "query": "Kiểm tra xem thứ Năm tuần này tôi có khung giờ nào trống từ 14:00 đến 17:00 không, nếu có thì lên lịch Review mã nguồn Sprint 3 vào 1 tiếng đầu tiên của khoảng trống đó nhé.",
    "thought": "Gemini chọn kiểm tra khung giờ trống trước khi tạo lịch.",
    "tool_name": "check_calendar_availability",
    "arguments": {
      "date": "2026-09-24",
      "start_time": "14:00",
      "end_time": "17:00"
    },
    "observation": {
      "status": "SUCCESS",
      "date": "2026-09-24",
      "available_slots": [
        {
          "start_datetime": "2026-09-24T14:00:00+07:00",
          "end_datetime": "2026-09-24T17:00:00+07:00"
        }
      ],
      "message": "Tìm thấy 1 khung giờ trống."
    },
    "latency_ms": 15724.57
  },
  {
    "step": 2,
    "action_type": "TOOL_EXECUTION",
    "thought": "Gemini dùng khung giờ trống đầu tiên để tạo lịch nhắc.",
    "tool_name": "create_calendar_reminder",
    "arguments": {
      "title": "Review mã nguồn Sprint 3",
      "start_datetime": "2026-09-24T14:00:00+07:00",
      "duration_minutes": 60,
      "reminder_minutes": 30
    },
    "observation": {
      "status": "SUCCESS",
      "message": "Đã tạo lịch nhắc trên Google Calendar."
    },
    "latency_ms": 4134.98
  },
  {
    "step": 3,
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản sau khi nhận Observation từ Tool.",
    "output": "Đã kiểm tra khung trống và tạo lịch Review mã nguồn Sprint 3 từ 14:00 đến 15:00 ngày 24/09/2026.",
    "latency_ms": 4444.52
  }
]
```

Trace đầy đủ được lưu tại [`docs/trace_waterfall.json`](trace_waterfall.json).

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã cấu hình `GEMINI_API_KEY` trong `.env` và chạy nghiệm thu trên Gemini thật, bao gồm các thao tác đọc/ghi Google Calendar.
- **Tổng số Test Cases đã chạy thành công:** **5 / 5 test cases** (trả lời hướng dẫn, thêm to-do, tạo lịch, kiểm tra rồi đặt lịch, và xử lý mã to-do không tồn tại).
- **Số lượt gọi Tool qua MCP Server chính xác trong trace hiện tại:** **5 lượt** (`add_todo`, `create_calendar_reminder` hai lần, `check_calendar_availability`, `update_todo_status`).
- **Kết quả đẩy Repo nộp bài:** [x] Đã commit và push mã nguồn thành công lên GitHub cá nhân: `https://github.com/ducdh205/K4-DAY03-DinhHoangDuc-2A202602795`.

> Ghi chú: TC03 đã tạo lịch **Họp kick-off dự án mới** và TC04 đã kiểm tra khung trống rồi tạo lịch **Review mã nguồn Sprint 3** trên Google Calendar. Các bước `TOOL_EXECUTION` trong trace đã lưu trường `thought`, tool call, observation và latency.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
