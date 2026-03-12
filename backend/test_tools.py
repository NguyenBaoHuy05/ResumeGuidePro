from app.tools.search_tools import candidate_search_tool, profile_scraper_tool

def test_search():
    print("--- Đang thử nghiệm tìm kiếm thông tin cuộc thi ---")
    res = candidate_search_tool._run("Encourage Prize in Vietnam Student AI Olympics 2025", "(Southern Region)")
    print(res)

    print("\n--- Đang thử nghiệm cào dữ liệu từ Portfolio ---")
    res_scrape = profile_scraper_tool._run("https://www.huynb.io.vn/")
    print(res_scrape[:1000]) # In 1000 ký tự đầu để xem nội dung

if __name__ == "__main__":
    test_search()
