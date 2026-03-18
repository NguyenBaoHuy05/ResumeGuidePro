from duckduckgo_search import DDGS as ddgs
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import BaseTool
import os
import re
import requests
from bs4 import BeautifulSoup

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
        # 1. Xử lý LinkedIn (Chặn sớm để đỡ tốn tài nguyên)
        if "linkedin.com" in url:
            return f"Thông báo: Không thể truy cập trực tiếp {url} do chính sách bảo mật của LinkedIn. Vui lòng đánh giá ứng viên dựa trên văn bản có sẵn trong CV."

        # 2. Xử lý GitHub (Dùng logic Smart Cutting)
        if "github.com" in url:
            return self._scrape_github(url)

        # 3. Xử lý Website khác (Dùng ScrapeWebsiteTool chuẩn)
        scraper = ScrapeWebsiteTool(website_url=url)
        try:
            raw_content = scraper.run()
            clean_text = self._clean_general_text(raw_content)
            
            if len(clean_text) < 50:
                 return f"Nội dung từ {url} quá ngắn hoặc cần JavaScript. Agent nên yêu cầu ứng viên cung cấp thông tin chi tiết hơn."
                 
            return f"Nội dung từ website {url}:\n\n{clean_text[:2000]}" 
        except Exception as e:
            return f"Lỗi khi đọc website {url}: {str(e)}"

    def _scrape_github(self, url: str) -> str:
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            is_profile = soup.find('span', class_='p-nickname') or soup.find('h1', class_='vcard-names')
            data = []
            
            if is_profile:
                name = soup.find('span', class_='p-name')
                bio = soup.find('div', class_='p-note')
                pinned = [r.get_text(strip=True) for r in soup.find_all('span', class_='repo')]
                data.append(f"GitHub Profile: {name.get_text(strip=True) if name else 'N/A'}")
                data.append(f"Bio: {bio.get_text(strip=True) if bio else 'N/A'}")
                data.append(f"Dự án nổi bật: {', '.join(pinned)}")
            else:
                about = soup.find('div', class_='BorderGrid-cell')
                lang_section = soup.find('h2', string=re.compile(r'Languages', re.I))
                readme = soup.find('article', class_='markdown-body')
                
                if about and about.find('p'): data.append(f"Mô tả Repo: {about.find('p').get_text(strip=True)}")
                if lang_section and lang_section.find_next('ul'): 
                    data.append(f"Ngôn ngữ: {lang_section.find_next('ul').get_text(separator=' ', strip=True)}")
                if readme:
                    clean_readme = readme.get_text(separator=' \n ', strip=True)
                    data.append(f"Nội dung README:\n{clean_readme[:3000]}")
            
            return "\n".join(data) if data else "Không tìm thấy thông tin hữu ích trên GitHub."
        except Exception as e:
            return f"Lỗi khi phân tích GitHub {url}: {str(e)}"

    def _clean_general_text(self, text: str) -> str:
        # Gom khoảng trắng
        text = re.sub(r'\s+', ' ', text)
        # Xử lý chữ cách rời
        text = re.sub(r'(?<=[a-zA-Z])\s(?=[a-zA-Z]\s)', '', text)
        return text.strip()

# Khởi tạo sẵn các instance để dùng
candidate_search_tool = CandidateSearchTool()
profile_scraper_tool = ProfileScraperTool()
