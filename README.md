# ResumeGuidePro 🚀

**ResumeGuidePro** is an intelligent resume analysis application powered by AI (CrewAI & Ollama) to help users optimize their resumes and prepare for interviews.

## ✨ Key Features
- 📄 **Resume Analysis (PDF):** Automatically extract text from PDF files and evaluate compatibility with the Job Description (JD).
- 🤖 **AI Recruiter:** Utilize CrewAI with a "Grandmaster Recruiter" agent to spot errors and provide strict evaluations.
- 📊 **Metrics & Scoring:** Provide an overall score and analysis charts for various elements: Skills, Keywords, Formatting, Experience, etc.
- 🚩 **Red Flags:** Warn about weaknesses in the resume that need immediate fixing.
- 💡 **Tips & Advice:** Suggest ways to improve the resume to meet 2025 standards.
- 🎭 **Mock Interview:** Automatically generate an interview question list based on the real experience stated in the resume.

---

## 🛠️ Prerequisites
Before getting started, make sure your computer has the following installed:
1. **Python 3.10+**
2. **Node.js 18+** & **npm**
3. **Ollama** (To run LLM locally)

---

## 🚀 Installation and Setup Guide

### 1. Prepare LLM (Ollama)
The application uses the **gemma3:4b** (or gemma2) model running via Ollama.
- Download and install Ollama at [ollama.com](https://ollama.com/).
- Open the terminal and pull the model:
  ```bash
  ollama pull gemma3:4b
  ```
- Ensure Ollama is running at `http://localhost:11434`.

### 2. Backend Configuration (FastAPI)
- Navigate to the backend directory:
  ```bash
  cd backend
  ```
- Create a virtual environment (venv):
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment:
  - **Windows:** `venv\Scripts\activate`
  - **macOS/Linux:** `source venv/bin/activate`
- Install required libraries:
  ```bash
  pip install -r requirements.txt
  ```
- Run the backend server:
  ```bash
  python -m app.main
  ```
  *(The backend will be running at: http://localhost:8000)*

### 3. Frontend Configuration (Next.js)
- Open a new terminal and navigate to the frontend directory:
  ```bash
  cd frontend
  ```
- Install dependencies:
  ```bash
  npm install
  ```
- Run the development server:
  ```bash
  npm run dev
  ```
  *(The frontend will be running at: http://localhost:3000)*

---

## 📁 Project Structure
```text
ResumeGuidePro/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI endpoints (Streaming & Direct)
│   │   ├── crew.py          # CrewAI logic (Agents & Tasks)
│   │   └── ollama_config.py # Ollama connection configuration
│   └── requirements.txt     # Python library list
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages & layouts
│   │   └── components/     # UI Components (Upload, Results, etc.)
│   └── package.json        # React/Next.js project configuration
└── README.md
```

## 📝 Notes
- Make sure to upload a PDF file (The application currently only supports `.pdf`).
- If you want to change the AI model, edit the `backend/app/ollama_config.py` file.

---
We hope you get an impressive resume soon and conquer all recruiters! 🎯