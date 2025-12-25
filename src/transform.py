
# transform.py - Biến đổi và chuẩn hoá dữ liệu
# file này thực hiện các biến đổi cần thiết cho phân tích:
# 1. Tạo nhóm kinh nghiệm 
# 2. Xử lý cột multi-select 
# 3. Chuẩn hoá các cột category

import pandas as pd
import numpy as np


# HÀM TẠO NHÓM KINH NGHIỆM 
def create_experience_bins(df: pd.DataFrame, col: str = 'YearsCodePro') -> pd.DataFrame:
    """
    Chia số năm kinh nghiệm thành các nhóm ) để dễ phân tích.
    
    Các nhóm:
    - Fresher: dưới 1 năm kinh nghiệm 
    - Junior: 1-2 năm kinh nghiệm
    - Mid-level: 3-5 năm
    - Senior: 6-10 năm  
    - Lead/Staff: 11-20 năm
    - Principal+: >20 năm
    
    Tham số:
        df: DataFrame chứa dữ liệu
        col: Tên cột chứa số năm kinh nghiệm (mặc định 'YearsCodePro')
    
    Trả về:
        DataFrame với cột mới 'ExperienceLevel' chứa nhóm kinh nghiệm
    """
    # Định nghĩa các mốc chia nhóm và nhãn tương ứng
    # Fresher: 0-1 năm, Junior: 1-2 năm, v.v.
    bins = [0, 1, 2, 5, 10, 20, np.inf]  # Các mốc: 0-1, 1-2, 3-5, 6-10, 11-20, 21+
    labels = ['Fresher (<1)', 'Junior (1-2)', 'Mid-level (3-5)', 
              'Senior (6-10)', 'Lead/Staff (11-20)', 'Principal+ (21+)']
    
    # Tạo cột mới với pd.cut() để phân nhóm
    df = df.copy()  # Tránh SettingWithCopyWarning
    df['ExperienceLevel'] = pd.cut(
        df[col], 
        bins=bins, 
        labels=labels, 
        include_lowest=True  # Bao gồm giá trị 0
    )
    
    return df



# HÀM XỬ LÝ CỘT MULTI-SELECT
def explode_multi_select(df: pd.DataFrame, col: str, sep: str = ';') -> pd.DataFrame:
    """
    Xử lý cột multi-select: tách các giá trị và mở rộng thành nhiều dòng.
    
    Ví dụ: Nếu một developer chọn "Python;JavaScript;TypeScript" cho câu hỏi 
    về ngôn ngữ, hàm này sẽ tạo 3 dòng riêng biệt cho developer đó, 
    mỗi dòng với một ngôn ngữ.
    
    Tham số:
        df: DataFrame gốc
        col: Tên cột cần xử lý (VD: 'LanguageHaveWorkedWith', 'DevType')
        sep: Ký tự phân cách giữa các giá trị (mặc định là ';')
    
    Trả về:
        DataFrame mới với các dòng đã được mở rộng (exploded)
    """
    df = df.copy()
    
    # Bước 1: Tách chuỗi thành list bằng str.split()
    # VD: "Python;JavaScript" -> ["Python", "JavaScript"]
    df[col] = df[col].str.split(sep)
    
    # Bước 2: Explode - mỗi phần tử trong list thành một dòng riêng
    df = df.explode(col)
    
    # Bước 3: Loại bỏ khoảng trắng thừa ở đầu/cuối
    df[col] = df[col].str.strip()
    
    # Bước 4: Loại bỏ các dòng rỗng (nếu có)
    df = df[df[col].notna() & (df[col] != '')]
    
    return df



#  HÀM CHUẨN HOÁ GIÁ TRỊ REMOTEWORK
def standardize_remote_work(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hoá nhãn cột RemoteWork cho ngắn gọn và dễ hiển thị.
    
    Chuyển đổi:
    - "Remote" -> "Remote"
    - "Hybrid (some remote, some in-person)" -> "Hybrid"
    - "In-person" -> "In-person"
    
    Tham số:
        df: DataFrame chứa cột 'RemoteWork'
    
    Trả về:
        DataFrame với cột RemoteWork đã chuẩn hoá
    """
    df = df.copy()
    
    # Mapping từ giá trị gốc sang giá trị ngắn gọn
    mapping = {
        'Remote': 'Remote',
        'Hybrid (some remote, some in-person)': 'Hybrid',
        'In-person': 'In-person'
    }
    
    df['RemoteWork'] = df['RemoteWork'].map(mapping)
    
    return df


# HÀM CHUẨN HOÁ GIÁ TRỊ AI SELECT
def standardize_ai_select(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hoá nhãn cột AISelect cho ngắn gọn.
    
    Chuyển đổi:
    - "Yes" -> "Using AI"
    - "No, but I plan to soon" -> "Planning"
    - "No, and I don't plan to" -> "Not Using"
    
    Tham số:
        df: DataFrame chứa cột 'AISelect'
    
    Trả về:
        DataFrame với cột AISelect đã chuẩn hoá
    """
    df = df.copy()
    
    mapping = {
        'Yes': 'Using AI',
        'No, but I plan to soon': 'Planning',
        "No, and I don't plan to": 'Not Using'
    }
    
    df['AISelect'] = df['AISelect'].map(mapping)
    
    return df


# HÀM CHẠY TOÀN BỘ QUY TRÌNH TRANSFORM
def run_transform(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Hàm chính thực hiện toàn bộ quy trình biến đổi dữ liệu.
    
    Các bước:
    1. Đọc dữ liệu đã clean
    2. Tạo nhóm kinh nghiệm
    3. Chuẩn hoá các cột category
    4. Lưu kết quả
    
    Tham số:
        input_path: Đường dẫn file CSV đầu vào (sau khi clean)
        output_path: Đường dẫn file CSV đầu ra (sau khi transform)
    
    Trả về:
        DataFrame đã được transform
    """
    
    # Bước 1: Đọc dữ liệu
    df = pd.read_csv(input_path)
    
    # Bước 2: Tạo nhóm kinh nghiệm
    df = create_experience_bins(df)
    
    # Bước 3: Chuẩn hoá RemoteWork
    df = standardize_remote_work(df)
    
    # Bước 4: Chuẩn hoá AISelect
    df = standardize_ai_select(df)
    
    # Lưu kết quả
    df.to_csv(output_path, index=False)

    return df



if __name__ == "__main__":
    # Đường dẫn mặc định
    INPUT_PATH = './data/processed/cleaned_developer_survey.csv'
    OUTPUT_PATH = './data/processed/transformed_developer_survey.csv'
    
    # Chạy transform
    df = run_transform(INPUT_PATH, OUTPUT_PATH)
