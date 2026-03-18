from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .crew import run_resume_analysis_crew
import uvicorn
import io
from pypdf import PdfReader

app = FastAPI(title="ResumeGuidePro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ResumeRanker API v3.0 is running", "docs": "/docs"}

from fastapi.responses import StreamingResponse
import asyncio
import threading
import queue
import json
import re

@app.post("/analyze-stream")
async def analyze_resume_stream(file: UploadFile = File(...), jd: str = None):
    # 1. Trích xuất text tương tự endpoint cũ
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file định dạng PDF.")
    
    pdf_content = await file.read()
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += (page.extract_text() or "").replace('\x00', '')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi PDF: {str(e)}")

    log_queue = queue.Queue()

    def run_crew():
        try:
            def log_callback(msg):
                log_queue.put({"type": "log", "content": str(msg)})

            result = run_resume_analysis_crew(
                resume_text, 
                jd or "Tối ưu CV cho ngành công nghệ.",
                step_callback=log_callback
            )

            # Phân tích kết quả JSON (Sử dụng Regex trích xuất chuỗi thủ công)
            result_str = str(result)
            
            # Ưu tiên tìm trong thẻ <result>
            json_match = re.search(r'<result>(.*?)</result>', result_str, re.DOTALL)
            
            clean_json = None
            if json_match:
                try:
                    json_str = json_match.group(1).strip()
                    clean_json = json.loads(json_str)
                except Exception as e:
                    print(f"Lỗi parse thẻ result: {e}")
            
            # Nếu thẻ <result> thất bại, thử tìm khối { } bất kỳ
            if not clean_json:
                json_blocks = re.findall(r'\{.*\}', result_str, re.DOTALL)
                for block in json_blocks:
                    try:
                        clean_json = json.loads(block.strip())
                        break
                    except:
                        continue

            if clean_json:
                log_queue.put({"type": "result", "data": clean_json})
            else:
                print(f"DEBUG - Full result from AI: {result_str}")
                log_queue.put({"type": "error", "content": "AI không trả về kết quả JSON hợp lệ trong thẻ <result>."})
        except Exception as e:
            print(f"Error in run_crew thread: {str(e)}")
            log_queue.put({"type": "error", "content": f"Lỗi hệ thống: {str(e)}"})
        finally:
            log_queue.put(None) 

    # Chạy Crew trong thread riêng
    threading.Thread(target=run_crew).start()

    async def event_generator():
        while True:
            try:
                # Tăng timeout lên 300 giây (5 phút) vì cào web và suy nghĩ tốn thời gian
                item = await asyncio.to_thread(log_queue.get, timeout=300)
                if item is None:
                    break
                yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"
            except queue.Empty:
                # Nếu quá lâu không có gì, gửi một gói 'ping' để giữ kết nối browser không bị ngắt
                yield f"data: {json.dumps({'type': 'ping', 'content': 'keep-alive'}, ensure_ascii=False)}\n\n"
                continue
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': f'Lỗi luồng dữ liệu: {str(e)}'}, ensure_ascii=False)}\n\n"
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), jd: str = None):
    # Giữ nguyên endpoint cũ cho tương thích
    try:
        pdf_content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        resume_text = "".join([(p.extract_text() or "") for p in pdf_reader.pages])
        raw_result = run_resume_analysis_crew(resume_text, jd or "Tối ưu CV.")
        result_str = str(raw_result)
        json_match = re.search(r'<result>(.*?)</result>', result_str, re.DOTALL) or \
                     re.search(r'\{.*\}', result_str, re.DOTALL)
        if json_match:
             json_str = json_match.group(1) if json_match.lastindex else json_match.group(0)
             return {"status": "success", "data": json.loads(json_str.strip())}
        return {"status": "partial_success", "raw_result": result_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
