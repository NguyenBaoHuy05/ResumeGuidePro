import requests
from bs4 import BeautifulSoup
import re

def linkedin_content_extractor(url):
    print(f"--- Đang phân tích LinkedIn: {url} ---")
    
    # LinkedIn cực kỳ khắt khe với bot. Cần User-Agent "xịn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    }
    
    try:
        # Lưu ý: LinkedIn thường chặn requests trực tiếp bằng status 999 hoặc 403
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 999:
            return "LinkedIn đã chặn yêu cầu (Status 999). LinkedIn yêu cầu trình duyệt thực hoặc đăng nhập để xem profile."
        if response.status_code != 200:
            return f"Không thể truy cập LinkedIn (Status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        extracted_data = {}
        
        # 1. Tên và Headline (Sử dụng selectors cho Public Profile)
        name_elem = soup.find('h1', class_=re.compile(r'top-card-layout__title|top-card__name', re.I))
        extracted_data['full_name'] = name_elem.get_text(strip=True) if name_elem else "Không lấy được tên"
        
        headline = soup.find('h2', class_=re.compile(r'top-card-layout__headline|top-card__headline', re.I))
        extracted_data['headline'] = headline.get_text(strip=True) if headline else "Không lấy được headline"
        
        # 2. About section
        about = soup.find('section', class_=re.compile(r'about-section|summary', re.I))
        if about:
            about_content = about.find('div', class_='core-section-container__content')
            extracted_data['about'] = about_content.get_text(separator=' ', strip=True) if about_content else about.get_text(strip=True)
        else:
            extracted_data['about'] = "Không tìm thấy phần Giới thiệu"

        # 3. Experience section
        exp_section = soup.find('section', class_=re.compile(r'experience-section|experience', re.I))
        if exp_section:
            items = exp_section.find_all('li', class_='experience-item')
            experiences = []
            for item in items:
                title = item.find('h3', class_='base-main-card__title')
                company = item.find('h4', class_='base-main-card__subtitle')
                duration = item.find('span', class_='before-duration')
                
                exp_text = f"- {title.get_text(strip=True) if title else 'N/A'} tại {company.get_text(strip=True) if company else 'N/A'}"
                if duration:
                    exp_text += f" ({duration.get_text(strip=True)})"
                experiences.append(exp_text)
            
            extracted_data['experience'] = "\n".join(experiences) if experiences else "Không lấy được chi tiết kinh nghiệm"
        else:
            extracted_data['experience'] = "Không tìm thấy phần Kinh nghiệm"

        return extracted_data

    except Exception as e:
        return f"Lỗi xử lý LinkedIn: {str(e)}"

if __name__ == "__main__":
    # Test với link LinkedIn của bạn
    url_test = "https://www.linkedin.com/in/nguyen-huy-a0aa692a3/"
    result = linkedin_content_extractor(url_test)
    
    print("\n--- KẾT QUẢ PHÂN TÍCH LINKEDIN ---")
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"[{key.upper()}]:\n{value}\n")
    else:
        print(result)
        print("\nLƯU Ý: LinkedIn thường chặn các kết nối tự động không chính thống.")
