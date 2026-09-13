"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPTaskCalendarServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "todo-google-calendar-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi tool và đóng gói Observation theo JSON-RPC mô phỏng MCP."""
        result_json = dispatch_tool_call(tool_name, arguments)

        try:
            # Chuyển JSON string thành Python Dictionary để Agent đọc Observation
            content = json.loads(result_json)
        except json.JSONDecodeError:
            content = {
                "status": "EXECUTION_ERROR",
                "error": "Tool trả về dữ liệu không đúng định dạng JSON.",
                "raw_result": result_json
            }

        # Đóng gói phản hồi theo cấu trúc JSON-RPC mô phỏng MCP
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }


# Giữ tên lớp cũ để không làm hỏng các đoạn mã tham khảo của starter repo.
MCPAcademicServer = MCPTaskCalendarServer


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (todo-google-calendar-mcp-server)")
    print("==========================================================")
    
    server = MCPTaskCalendarServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    test_result = server.call_tool("get_pending_todos", {})
    print("✅ Test dispatch tool 'get_pending_todos':")
    print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
