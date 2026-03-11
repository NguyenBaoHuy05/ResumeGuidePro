# ResumeGuidePro 🚀

**ResumeGuidePro** là một ứng dụng phân tích CV thông minh sử dụng AI (CrewAI & Ollama) để giúp người dùng tối ưu hóa hồ sơ xin việc và chuẩn bị cho các buổi phỏng vấn.

## ✨ Tính năng chính
- 📄 **Phân tích CV (PDF):** Tự động trích xuất text từ file PDF và đánh giá độ tương thích với mô tả công việc (JD).
- 🤖 **AI Recruiter:** Sử dụng CrewAI với agent "Grandmaster Recruiter" để soi lỗi và đưa ra đánh giá khắt khe.
- 📊 **Metrics & Scoring:** Cung cấp điểm số tổng quan và biểu đồ phân tích các yếu tố: Skills, Keywords, Formatting, Experience...
- 🚩 **Red Flags:** Cảnh báo các điểm yếu trong CV cần khắc phục ngay lập tức.
- 💡 **Tips & Advice:** Gợi ý cách cải thiện CV đạt chuẩn 2025.
- 🎭 **Mock Interview:** Tự động tạo danh sách câu hỏi phỏng vấn dựa trên kinh nghiệm thực tế trong CV.

---

## 🛠️ Yêu cầu hệ thống (Prerequisites)
Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt:
1. **Python 3.10+**
2. **Node.js 18+** & **npm**
3. **Ollama** (Để chạy LLM cục bộ)

---

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Chuẩn bị LLM (Ollama)
Ứng dụng sử dụng mô hình **gemma3:4b** (hoặc gemma2) chạy qua Ollama.
- Tải và cài đặt Ollama tại [ollama.com](https://ollama.com/).
- Mở terminal và tải model:
  ```bash
  ollama pull gemma3:4b
  ```
- Đảm bảo Ollama đang chạy tại `http://localhost:11434`.

### 2. Cấu hình Backend (FastAPI)
- Di chuyển vào thư mục backend:
  ```bash
  cd backend
  ```
- Tạo môi trường ảo (venv):
  ```bash
  python -m venv venv
  ```
- Kích hoạt môi trường ảo:
  - **Windows:** `venv\Scripts\activate`
  - **macOS/Linux:** `source venv/bin/activate`
- Cài đặt các thư viện cần thiết:
  ```bash
  pip install -r requirements.txt
  ```
- Chạy server backend:
  ```bash
  python -m app.main
  ```
  *(Backend sẽ chạy tại: http://localhost:8000)*

### 3. Cấu hình Frontend (Next.js)
- Mở một terminal mới và di chuyển vào thư mục frontend:
  ```bash
  cd frontend
  ```
- Cài đặt dependencies:
  ```bash
  npm install
  ```
- Chạy server phát triển:
  ```bash
  npm run dev
  ```
  *(Frontend sẽ chạy tại: http://localhost:3000)*

---

## 📁 Cấu trúc dự án
```text
ResumeGuidePro/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI endpoints (Streaming & Direct)
│   │   ├── crew.py          # CrewAI logic (Agents & Tasks)
│   │   └── ollama_config.py # Cấu hình kết nối Ollama
│   └── requirements.txt     # Danh sách thư viện Python
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages & layouts
│   │   └── components/     # UI Components (Upload, Results, etc.)
│   └── package.json        # Cấu hình dự án React/Next.js
└── README.md
```

## 📝 Lưu ý
- Đảm bảo bạn đã bọc file PDF khi upload (Ứng dụng hiện chỉ hỗ trợ `.pdf`).
- Nếu muốn đổi model AI, hãy chỉnh sửa trong file `backend/app/ollama_config.py`.

---
Chúc bạn sớm có một chiếc CV "xịn xò" và chinh phục mọi nhà tuyển dụng! 🎯