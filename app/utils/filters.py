def is_software_job(title: str, keyword: str) -> bool:
    t = title.lower()
    k = keyword.lower()

    block = ["marketing", "sales", "hr", "content", "business", "video", "graphic"]
    if any(b in t for b in block):
        return False

    tech = ["software", "developer", "engineer", "web", "data", "ai", "app", "backend", "frontend"]
    return k in t or any(tk in t for tk in tech)