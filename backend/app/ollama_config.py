from crewai import LLM

def get_ollama_llm(model_name="ollama/gemma3:4b"):
    """
    Sửa lỗi chính tả từ 'olama' thành 'ollama'.
    Sử dụng lớp LLM của CrewAI để tối ưu hóa việc gọi tool và stream.
    """
    return LLM(
        model=model_name,
        base_url="http://localhost:11434"
    )
