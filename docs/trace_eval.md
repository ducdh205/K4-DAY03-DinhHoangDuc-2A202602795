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

Dưới đây là đoạn trace tiêu biểu khi Gemini chọn Tool `list_calendar_events` để tra cứu Google Calendar ngày 14/09/2026. Tool trả về dữ liệu lịch thật, sau đó Agent tổng hợp câu trả lời ở bước 2.

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "query": "ngày 14/9/2026 có lịch gì không",
    "tool_name": "list_calendar_events",
    "arguments": {
      "date": "2026-09-14"
    },
    "observation": {
      "status": "SUCCESS",
      "date": "2026-09-14",
      "count": 1,
      "message": "Tìm thấy 1 sự kiện vào ngày 2026-09-14."
    },
    "latency_ms": 5159.44
  },
  {
    "step": 2,
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản sau khi nhận Observation từ Tool.",
    "output": "Vào ngày 14/09/2026, bạn có 1 lịch hẹn: Đi chơi, từ 22:00 đến 23:00.",
    "latency_ms": 2737.57
  }
]
```

Trace đầy đủ được lưu tại [`docs/trace_waterfall.json`](trace_waterfall.json).

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã cấu hình `GEMINI_API_KEY` trong `.env` và lưu được trace gọi Tool `list_calendar_events` trả về dữ liệu Google Calendar thành công.
- **Tổng số Test Cases đã có bằng chứng chạy thành công:** **1 / 5 test cases** (truy vấn lịch ngày 14/09/2026).
- **Số lượt gọi Tool qua MCP Server chính xác trong trace hiện tại:** **1 lượt** (`list_calendar_events`).
- **Kết quả đẩy Repo nộp bài:** [x] Đã commit và push mã nguồn thành công lên GitHub cá nhân: `https://github.com/ducdh205/K4-DAY03-DinhHoangDuc-2A202602795`.

> Ghi chú: Cần chạy và lưu thêm TC01–TC05 nếu muốn có bằng chứng nghiệm thu đầy đủ 5/5 test cases. TC03 và TC04 có thể tạo sự kiện thật trên Google Calendar.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
