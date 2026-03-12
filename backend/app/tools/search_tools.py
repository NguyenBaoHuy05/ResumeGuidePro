from duckduckgo_search import DDGS as ddgs
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import BaseTool
import os
import re

class CandidateSearchTool(BaseTool):
    name: str = "search_candidate_online"
    description: str = "Tìm kiếm thông tin ứng viên trên LinkedIn, GitHub, Facebook hoặc Website cá nhân dựa trên tên và kỹ năng."

    def _run(self, candidate_name: str, key_skills: str = "") -> str:
        query = f"{candidate_name} {key_skills} (LinkedIn OR GitHub OR Portfolio) -movie -film"
        try:
            with ddgs() as search:
                results = list(search.text(query, max_results=5))
                if not results:
                    return f"Không tìm thấy kết quả nào cho {candidate_name}."
                
                formatted_results = "\n\n".join([f"Tiêu đề: {r['title']}\nLink: {r['href']}\nNội dung: {r['body']}" for r in results])
                return f"Kết quả tìm kiếm cho {candidate_name}:\n\n{formatted_results}"
        except Exception as e:
            return f"Lỗi khi tìm kiếm: {str(e)}"

class ProfileScraperTool(BaseTool):
    name: str = "scrape_profile_content"
    description: str = "Đọc nội dung chi tiết từ một link (URL) cụ thể để lấy thông tin chi tiết về dự án hoặc kinh nghiệm."

    def _run(self, url: str) -> str:
        scraper = ScrapeWebsiteTool(website_url=url)
        try:
            raw_content = scraper.run()
            
            # Làm sạch văn bản:
            # 1. Loại bỏ các ký tự điều khiển và khoảng trắng cực đoan
            clean_text = re.sub(r'\s+', ' ', raw_content)
            
            # 2. Xử lý trường hợp chữ bị cách rời (ví dụ: W e l c o m e -> Welcome)
            # Một trick nhỏ: nếu thấy chuỗi có dạng "X X X X" (chữ cái cách nhau 1 khoảng trắng)
            clean_text = re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z]\s)', '', clean_text)
            
            # 3. Loại bỏ khoảng trắng đầu cuối và giới hạn độ dài để tránh làm Agent bị ngợp
            clean_text = clean_text.strip()
            
            if len(clean_text) < 50:
                 return f"Nội dung cào được từ {url} quá ngắn hoặc không có ý nghĩa. Có thể trang web yêu cầu JavaScript để hiển thị nội dung."
                 
            return f"Nội dung đã được làm sạch từ {url}:\n\n{clean_text[:5000]}" # Giới hạn 5000 ký tự
        except Exception as e:
            return f"Không thể đọc nội dung từ {url}: {str(e)}"

# Khởi tạo sẵn các instance để dùng
candidate_search_tool = CandidateSearchTool()
profile_scraper_tool = ProfileScraperTool()
