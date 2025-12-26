"""
roadmap.py - Logic tạo Roadmap đề xuất cho Developer

Module này đọc các file CSV đã phân tích và tổng hợp thành
"""

import os
import pandas as pd

# Đường dẫn đến thư mục chứa các file CSV kết quả phân tích
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TABLES_DIR = os.path.join(BASE_DIR, "reports", "tables")


def get_available_roles() -> list:
    """
    Lấy danh sách các DevType có sẵn trong dữ liệu.
    
    Trả về:
        List các DevType (ví dụ: ["Developer, back-end", "Developer, front-end", ...])
    """
    path = os.path.join(TABLES_DIR, "languages_by_devtype.csv")
    
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path)
    roles = df["DevType"].unique().tolist()
    
    return roles


def get_role_display_name(devtype: str) -> str:
    """
    Chuyển tên DevType gốc thành tên hiển thị ngắn gọn.
    
    Ví dụ:
        "Developer, back-end" -> "Backend Developer"
        "Developer, full-stack" -> "Full-stack Developer"
    """
    rename_map = {
        "Developer, back-end": "Backend Developer",
        "Developer, front-end": "Frontend Developer",
        "Developer, mobile": "Mobile Developer",
        "Developer, full-stack": "Full-stack Developer",
        "Developer, desktop or enterprise applications": "Desktop/Enterprise Developer",
        "Developer, embedded applications or devices": "Embedded Developer",
        "Data engineer": "Data Engineer",
        "Engineering manager": "Engineering Manager",
        "DevOps specialist": "DevOps Specialist",
        "Data scientist or machine learning specialist": "Data Scientist / ML Engineer",
    }
    
    return rename_map.get(devtype, devtype)


def generate_roadmap(devtype: str) -> dict:
    """
    Tạo Roadmap đề xuất cho một DevType cụ thể.
    
    Tham số:
        devtype: Tên DevType (ví dụ: "Developer, back-end")
    
    Trả về:
        Dictionary chứa các thông tin Roadmap:
        {
            "role": str,           # Tên hiển thị
            "languages": list,     # Top languages [(name, percentage), ...]
            "remote_stats": dict,  # {"Remote": %, "Hybrid": %, "In-person": %}
            "ai_usage": str,       # Thông tin về AI usage
            "frustrations": list,  # Top frustrations
            "salary_info": dict    # Thông tin lương
        }
    """
    roadmap = {
        "role": get_role_display_name(devtype),
        "role_original": devtype,
        "languages": [],
        "remote_stats": {},
        "ai_usage": "",
        "frustrations": [],
        "salary_info": {}
    }
    
    # 1. Lấy top languages cho DevType này
    roadmap["languages"] = _get_languages_for_role(devtype)
    
    # 2. Lấy remote work stats cho DevType này
    roadmap["remote_stats"] = _get_remote_stats_for_role(devtype)
    
    # 3. Lấy thông tin AI usage 
    roadmap["ai_usage"] = _get_ai_usage_info()
    
    # 4. Lấy top frustrations
    roadmap["frustrations"] = _get_top_frustrations()
    
    # 5. Lấy thông tin salary
    roadmap["salary_info"] = _get_salary_info()
    
    return roadmap


def _get_languages_for_role(devtype: str) -> list:
    """
    Lấy top languages cho một DevType.
    
    Trả về:
        List of tuples: [(language, percentage), ...]
    """
    path = os.path.join(TABLES_DIR, "languages_by_devtype.csv")
    
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path)
    df_role = df[df["DevType"] == devtype].sort_values("Rank")
    
    languages = []
    for _, row in df_role.iterrows():
        languages.append({
            "name": row["Language"],
            "percentage": row["Percentage"],
            "rank": int(row["Rank"])
        })
    
    return languages


def _get_remote_stats_for_role(devtype: str) -> dict:
    """
    Lấy thống kê remote work cho một DevType.
    
    Trả về:
        Dict: {"Remote": %, "Hybrid": %, "In-person": %}
    """
    path = os.path.join(TABLES_DIR, "remote_by_devtype.csv")
    
    if not os.path.exists(path):
        return {}
    
    df = pd.read_csv(path, index_col=0)
    df.index = df.index.str.strip()
    
    if devtype not in df.index:
        return {}
    
    row = df.loc[devtype]
    
    stats = {}
    for col in ["Remote", "Hybrid", "In-person"]:
        if col in row.index:
            stats[col] = round(row[col], 1)
    
    return stats


def _get_ai_usage_info() -> dict:
    """
    Lấy thông tin AI usage tổng quan.
    
    Trả về:
        Dict với thông tin AI usage
    """
    path = os.path.join(TABLES_DIR, "ai_usage.csv")
    
    if not os.path.exists(path):
        return {}
    
    df = pd.read_csv(path)
    
    result = {}
    for _, row in df.iterrows():
        ai_usage = row.get("AIUsage", row.iloc[0])
        percentage = row.get("Percentage", row.iloc[2] if len(row) > 2 else row.iloc[1])
        result[ai_usage] = round(percentage, 1)
    
    return result


def _get_top_frustrations(top_n: int = 5) -> list:
    """
    Lấy top frustrations.
    
    Trả về:
        List of dicts: [{"name": str, "percentage": float}, ...]
    """
    path = os.path.join(TABLES_DIR, "top_frustrations.csv")
    
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path).head(top_n)
    
    frustrations = []
    for _, row in df.iterrows():
        frustrations.append({
            "name": row["Frustration"],
            "percentage": round(row["Percentage"], 1)
        })
    
    return frustrations


def _get_salary_info() -> list:
    """
    Lấy thông tin salary theo experience level.
    
    Trả về:
        List of dicts với thông tin salary theo level
    """
    path = os.path.join(TABLES_DIR, "compensation_by_experience.csv")
    
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path)
    
    # Sắp xếp theo thứ tự experience
    order = [
        "Fresher (<1)",
        "Junior (1-2)",
        "Mid-level (3-5)",
        "Senior (6-10)",
        "Lead/Staff (11-20)",
        "Principal+ (21+)"
    ]
    
    df["ExperienceLevel"] = pd.Categorical(df["ExperienceLevel"], categories=order, ordered=True)
    df = df.sort_values("ExperienceLevel")
    
    salary_info = []
    for _, row in df.iterrows():
        salary_info.append({
            "level": row["ExperienceLevel"],
            "median": int(row["Median"]) if pd.notna(row["Median"]) else 0,
            "mean": int(row["Mean"]) if pd.notna(row["Mean"]) else 0
        })
    
    return salary_info

