from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from .ollama_config import get_ollama_llm

class SearchJobTrendsTool(BaseTool):
    name: str = "search_job_trends"
    description: str = "Tìm kiếm xu hướng việc làm và các từ khóa (keywords) hot nhất cho một ngành cụ thể."

    def _run(self, industry: str) -> str:
        # Đây là logic thực thi của tool
        return f"Xu hướng hiện tại cho ngành {industry} là: AI Integration, Cloud Native, và Cybersecurity."

# Khởi tạo instance của tool
search_tool = SearchJobTrendsTool()

def run_resume_analysis_crew(resume_content: str, jd_content: str = "", step_callback=None):
    llm = get_ollama_llm()

    def agent_step_callback(step):
        if step_callback:
            msg = "Đang phân tích..."
            if hasattr(step, 'thought') and step.thought:
                msg = step.thought[:150]
            step_callback(f"[Recruiter]: {msg}...")

    # Gom thành 1 Agent duy nhất để tránh lỗi chuyển giao (delegation) trên model nhỏ
    recruiter = Agent(
        role='Grandmaster Recruiter (Chuyên gia soi CV 20 năm)',
        goal='Tìm ra mọi lỗi sai và đánh giá khắt khe CV {resume_content} dựa trên JD {jd_content}',
        backstory="""Bạn là một 'huyền thoại' trong giới tuyển dụng. Bạn không có sự thương hại. 
        Bạn sẽ băm vằn CV thành từng mảnh nếu nó không đạt chuẩn 2025. 
        Bạn chuyên tìm Red Flags và đánh giá các yếu tố: Experience, Projects, Awards.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        step_callback=agent_step_callback
    )

    # Quay lại phương pháp yêu cầu chuỗi văn bản để tránh lỗi Tool Calling của thư viện Instructor
    analysis_task = Task(
        description=f"""Hãy phân tích CV và JD sau đây một cách cực kỳ khắt khe:
        CV: {resume_content}
        JD: {jd_content}
        
        YÊU CẦU ĐẦU RA (BẮT BUỘC):
        Bạn phải trả về một JSON object nằm trong thẻ <result>...</result> với các trường:
        - overall_score: (số từ 0-10)
        - recruiter_summary: (1 câu tóm tắt)
        - red_flags: (danh sách chuỗi)
        - metrics: {{"skills":0, "keywords":0, "formatting":0, "experience":0, "projects":0, "awards":0}}
        - detailed_analysis: (Markdown báo cáo)
        - checklist: [{{"label": "...", "status": true}}]
        - tips: [{{"title": "...", "text": "..."}}]
        - mock_interview: [{{"question": "...", "purpose": "..."}}]

        MẪU JSON CHUẨN:
        <result>
        {{
            "overall_score": 4,
            "recruiter_summary": "Tóm tắt phũ phàng tại đây.",
            "red_flags": ["Lỗi 1", "Lỗi 2"],
            "metrics": {{ "skills": 50, "keywords": 40, "formatting": 70, "experience": 30, "projects": 20, "awards": 10 }},
            "detailed_analysis": "## Phân tích chi tiết...",
            "checklist": [ {{"label": "Tiêu chí 1", "status": false}} ],
            "tips": [ {{"title": "Gợi ý", "text": "Nội dung..."}} ],
            "mock_interview": [ {{"question": "Câu hỏi?", "purpose": "Mục đích..."}} ]
        }}
        </result>
        """,
        expected_output="Báo cáo phân tích CV dưới dạng JSON bọc trong thẻ <result>.",
        agent=recruiter
    )

    crew = Crew(
        agents=[recruiter],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return str(result)
