import requests
from bs4 import BeautifulSoup
import re

def github_content_extractor(url):
    print(f"--- Đang phân tích GitHub: {url} ---")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Không thể truy cập GitHub (Status: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kiểm tra xem đây là trang Profile hay trang Repo
        # Profile thường có class vcard-names hoặc nickname
        is_profile = soup.find('span', class_='p-nickname') or soup.find('h1', class_='vcard-names')
        
        extracted_data = {}
        
        if is_profile:
            print("Phát hiện: GitHub Profile page")
            # 1. Nickname/Name
            name = soup.find('span', class_='p-name')
            nickname = soup.find('span', class_='p-nickname')
            extracted_data['user'] = f"{name.get_text(strip=True) if name else ''} ({nickname.get_text(strip=True) if nickname else ''})"
            
            # 2. Bio
            bio = soup.find('div', class_='p-note')
            extracted_data['bio'] = bio.get_text(strip=True) if bio else "Không có bio"
            
            # 3. Pinned Repositories
            pinned = soup.find_all('span', class_='repo')
            extracted_data['pinned_repos'] = ", ".join([r.get_text(strip=True) for r in pinned])
            
            # 4. Đặc biệt: Profile README (nếu có)
            readme = soup.find('article', class_='markdown-body')
            if readme:
                extracted_data['profile_readme'] = readme.get_text(separator=' ').strip()[:1000]
            
        else:
            print("Phát hiện: GitHub Repository page")
            # 1. About section (Mô tả ở cột phải)
            about_div = soup.find('div', class_='BorderGrid-cell')
            if about_div:
                desc = about_div.find('p')
                extracted_data['about'] = desc.get_text(strip=True) if desc else "Không có mô tả"
                
                # Lấy các Topics (Tags)
                topics = [t.get_text(strip=True) for t in about_div.find_all('a', class_='topic-tag')]
                if topics:
                    extracted_data['topics'] = ", ".join(topics)
            
            # 2. Languages (Ngôn ngữ lập trình)
            lang_section = soup.find('h2', string=re.compile(r'Languages', re.I))
            if lang_section:
                # Tìm container chứa danh sách ngôn ngữ (thường là anh em của h2)
                langs = lang_section.find_next('ul')
                if langs:
                    extracted_data['languages'] = langs.get_text(separator=' ', strip=True)

            # 3. README Content (Làm sạch chuyên sâu)
            readme = soup.find('article', class_='markdown-body')
            if readme:
                # Dùng separator là dấu cách kép để tránh dính chữ giữa các block
                readme_text = readme.get_text(separator=' \n ', strip=True)
                
                # Thu gọn các dòng trắng quá nhiều
                readme_text = re.sub(r'\n\s*\n', '\n', readme_text)
                
                # Ưu tiên lấy các tiêu đề chính (H1, H2, H3) và nội dung dưới đó
                extracted_data['readme_clean'] = readme_text[:2500] + "..." if len(readme_text) > 2500 else readme_text
            else:
                extracted_data['readme_clean'] = "Không tìm thấy README"

        return extracted_data

    except Exception as e:
        return f"Lỗi xử lý: {str(e)}"

# Thử nghiệm với profile của bạn (nếu có trong log trước đó)
if __name__ == "__main__":
    # Test với repository của bạn
    url_test = "https://github.com/NguyenBaoHuy05/ResumeGuidePro"
    result = github_content_extractor(url_test)
    
    print("\n--- KẾT QUẢ PHÂN TÍCH (ĐÃ CẮT LỌC) ---")
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"[{key.upper()}]:\n{value}\n")
    else:
        print(result)
