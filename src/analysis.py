
# analysis.py - Phân tích và thống kê dữ liệu

# Module này thực hiện các phân tích thống kê:
# 1. Tỉ lệ RemoteWork tổng thể
# 2. Crosstab RemoteWork theo kinh nghiệm, DevType
# 3. Top ngôn ngữ lập trình phổ biến
# 4. Thống kê AI usage
# 5. Thống kê lương theo nhóm


import pandas as pd
import numpy as np
import os


# Tạo thư mục output nếu chưa có
OUTPUT_DIR = './reports/tables'
os.makedirs(OUTPUT_DIR, exist_ok=True)



# HÀM 1: THỐNG KÊ TỈ LỆ REMOTEWORK TỔNG THỂ

def analyze_remote_work_overall(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tính tỉ lệ phần trăm các hình thức làm việc (Remote/Hybrid/In-person).
    
    Tham số:
        df: DataFrame chứa cột 'RemoteWork'
    
    Trả về:
        DataFrame với số lượng và tỉ lệ % của mỗi hình thức
    """
    # Đếm số lượng mỗi loại
    counts = df['RemoteWork'].value_counts()
    
    # Tính tỉ lệ phần trăm
    percentages = df['RemoteWork'].value_counts(normalize=True) * 100
    
    # Gộp thành bảng kết quả
    result = pd.DataFrame({
        'RemoteWork': counts.index,
        'Count': counts.values,
        'Percentage': percentages.values.round(2)
    })
    
    return result



# HÀM 2: CROSSTAB REMOTEWORK THEO KINH NGHIỆM

def analyze_remote_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích tỉ lệ RemoteWork theo từng nhóm kinh nghiệm.
    Giúp trả lời: "Developer senior có làm remote nhiều hơn junior không?"
    
    Tham số:
        df: DataFrame chứa cột 'RemoteWork' và 'ExperienceLevel'
    
    Trả về:
        DataFrame crosstab với tỉ lệ % theo hàng
    """
    # Tạo crosstab đếm số lượng
    crosstab = pd.crosstab(
        df['ExperienceLevel'], 
        df['RemoteWork'],
        margins=True,  # Thêm tổng ở cuối
        margins_name='Total'
    )
    
    # Chuyển sang tỉ lệ % theo hàng (mỗi hàng tổng = 100%)
    crosstab_pct = pd.crosstab(
        df['ExperienceLevel'], 
        df['RemoteWork'],
        normalize='index'  # Normalize theo hàng
    ) * 100
    
    # Làm tròn 2 chữ số thập phân
    crosstab_pct = crosstab_pct.round(2)
    
    return crosstab_pct



# HÀM 3: CROSSTAB REMOTEWORK THEO DEVTYPE

def analyze_remote_by_devtype(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Phân tích tỉ lệ RemoteWork theo từng loại developer (DevType).
    
    Lưu ý: DevType là cột multi-select (một người có thể chọn nhiều role),
    nên cần explode trước khi phân tích.
    
    Tham số:
        df: DataFrame chứa cột 'RemoteWork' và 'DevType'
        top_n: Số lượng DevType phổ biến nhất để phân tích (mặc định 10)
    
    Trả về:
        DataFrame crosstab với tỉ lệ % theo hàng
    """
    # Tạo bản copy và explode cột DevType
    df_exploded = df.copy()
    df_exploded['DevType'] = df_exploded['DevType'].str.split(';')
    df_exploded = df_exploded.explode('DevType')
    df_exploded['DevType'] = df_exploded['DevType'].str.strip()
    
    # Lọc chỉ top N DevType phổ biến nhất
    top_devtypes = df_exploded['DevType'].value_counts().head(top_n).index
    df_filtered = df_exploded[df_exploded['DevType'].isin(top_devtypes)]
    
    # Tạo crosstab với tỉ lệ %
    crosstab_pct = pd.crosstab(
        df_filtered['DevType'], 
        df_filtered['RemoteWork'],
        normalize='index'
    ) * 100
    
    crosstab_pct = crosstab_pct.round(2)
    
    # Sắp xếp theo tỉ lệ Remote giảm dần
    if 'Remote' in crosstab_pct.columns:
        crosstab_pct = crosstab_pct.sort_values('Remote', ascending=False)
    
    return crosstab_pct



# HÀM 4: TOP NGÔN NGỮ LẬP TRÌNH PHỔ BIẾN

def analyze_top_languages(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Thống kê top ngôn ngữ lập trình được sử dụng nhiều nhất.
    
    Tham số:
        df: DataFrame chứa cột 'LanguageHaveWorkedWith'
        top_n: Số lượng ngôn ngữ top (mặc định 15)
    
    Trả về:
        DataFrame với số lượng và tỉ lệ % developer dùng mỗi ngôn ngữ
    """
    # Explode cột LanguageHaveWorkedWith
    df_exploded = df.copy()
    df_exploded['LanguageHaveWorkedWith'] = df_exploded['LanguageHaveWorkedWith'].str.split(';')
    df_exploded = df_exploded.explode('LanguageHaveWorkedWith')
    df_exploded['LanguageHaveWorkedWith'] = df_exploded['LanguageHaveWorkedWith'].str.strip()
    
    # Đếm số lượng
    lang_counts = df_exploded['LanguageHaveWorkedWith'].value_counts().head(top_n)
    
    # Tính tỉ lệ % (so với tổng số developer)
    total_developers = len(df)
    lang_pct = (lang_counts / total_developers * 100).round(2)
    
    # Tạo bảng kết quả
    result = pd.DataFrame({
        'Language': lang_counts.index,
        'Count': lang_counts.values,
        'Percentage': lang_pct.values
    })
    
    return result



# HÀM 5: THỐNG KÊ AI USAGE

def analyze_ai_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thống kê tỉ lệ developer sử dụng AI.
    
    Tham số:
        df: DataFrame chứa cột 'AISelect'
    
    Trả về:
        DataFrame với số lượng và tỉ lệ % của mỗi nhóm AI usage
    """
    counts = df['AISelect'].value_counts()
    percentages = df['AISelect'].value_counts(normalize=True) * 100
    
    result = pd.DataFrame({
        'AIUsage': counts.index,
        'Count': counts.values,
        'Percentage': percentages.values.round(2)
    })
    
    return result



# HÀM 6: THỐNG KÊ LƯƠNG THEO NHÓM KINH NGHIỆM

def analyze_compensation_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thống kê lương (CompTotal) theo từng nhóm kinh nghiệm.
    
    Tham số:
        df: DataFrame chứa cột 'CompTotal' và 'ExperienceLevel'
    
    Trả về:
        DataFrame với các thống kê lương (mean, median, min, max) theo nhóm
    """
    # Nhóm theo ExperienceLevel và tính các thống kê
    stats = df.groupby('ExperienceLevel')['CompTotal'].agg([
        ('Count', 'count'),
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Std', 'std')
    ]).round(2)
    
    # Reset index để ExperienceLevel thành cột
    stats = stats.reset_index()
    
    return stats



# HÀM 7: THỐNG KÊ AI USAGE THEO KINH NGHIỆM

def analyze_ai_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    """
    Phân tích tỉ lệ sử dụng AI theo từng nhóm kinh nghiệm.
    Giúp trả lời: "Developer junior hay senior dùng AI nhiều hơn?"
    
    Tham số:
        df: DataFrame chứa cột 'AISelect' và 'ExperienceLevel'
    
    Trả về:
        DataFrame crosstab với tỉ lệ % theo hàng
    """
    crosstab_pct = pd.crosstab(
        df['ExperienceLevel'], 
        df['AISelect'],
        normalize='index'
    ) * 100
    
    crosstab_pct = crosstab_pct.round(2)
    
    return crosstab_pct



# HÀM 8: TOP FRUSTRATIONS (THÁCH THỨC/KHÓ KHĂN)

def analyze_top_frustrations(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Thống kê top các frustration (khó khăn/thách thức) của developer.
    
    Cột Frustration là multi-select, mỗi người có thể chọn nhiều giá trị
    phân cách bằng dấu ';'.
    
    Tham số:
        df: DataFrame chứa cột 'Frustration'
        top_n: Số lượng frustration top (mặc định 10)
    
    Trả về:
        DataFrame với số lượng và tỉ lệ % developer gặp mỗi frustration
    """
    # Kiểm tra cột Frustration tồn tại
    if 'Frustration' not in df.columns:
        print("Warning: Cột 'Frustration' không tồn tại trong dữ liệu")
        return pd.DataFrame()
    
    # Explode cột Frustration
    df_exploded = df.copy()
    df_exploded['Frustration'] = df_exploded['Frustration'].str.split(';')
    df_exploded = df_exploded.explode('Frustration')
    df_exploded['Frustration'] = df_exploded['Frustration'].str.strip()
    
    # Loại bỏ giá trị rỗng
    df_exploded = df_exploded[df_exploded['Frustration'].notna() & (df_exploded['Frustration'] != '')]
    
    # Đếm số lượng
    frust_counts = df_exploded['Frustration'].value_counts().head(top_n)
    
    # Tính tỉ lệ % (so với tổng số developer)
    total_developers = len(df)
    frust_pct = (frust_counts / total_developers * 100).round(2)
    
    # Tạo bảng kết quả
    result = pd.DataFrame({
        'Frustration': frust_counts.index,
        'Count': frust_counts.values,
        'Percentage': frust_pct.values
    })
    
    return result



# HÀM 9: TOP DEVTYPE

def analyze_top_devtypes(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Thống kê top các loại developer (DevType) phổ biến nhất.
    
    Cột DevType là multi-select, mỗi người có thể chọn nhiều role
    phân cách bằng dấu ';'.
    
    Tham số:
        df: DataFrame chứa cột 'DevType'
        top_n: Số lượng DevType top (mặc định 15)
    
    Trả về:
        DataFrame với số lượng và tỉ lệ % developer thuộc mỗi DevType
    """
    # Kiểm tra cột DevType tồn tại
    if 'DevType' not in df.columns:
        print("Warning: Cột 'DevType' không tồn tại trong dữ liệu")
        return pd.DataFrame()
    
    # Explode cột DevType
    df_exploded = df.copy()
    df_exploded['DevType'] = df_exploded['DevType'].str.split(';')
    df_exploded = df_exploded.explode('DevType')
    df_exploded['DevType'] = df_exploded['DevType'].str.strip()
    
    # Loại bỏ giá trị rỗng
    df_exploded = df_exploded[df_exploded['DevType'].notna() & (df_exploded['DevType'] != '')]
    
    # Đếm số lượng
    devtype_counts = df_exploded['DevType'].value_counts().head(top_n)
    
    # Tính tỉ lệ % (so với tổng số developer)
    total_developers = len(df)
    devtype_pct = (devtype_counts / total_developers * 100).round(2)
    
    # Tạo bảng kết quả
    result = pd.DataFrame({
        'DevType': devtype_counts.index,
        'Count': devtype_counts.values,
        'Percentage': devtype_pct.values
    })
    
    return result



# HÀM CHÍNH: CHẠY TOÀN BỘ PHÂN TÍCH
def run_analysis(input_path: str) -> dict:
    """
    Hàm chính thực hiện toàn bộ phân tích và lưu kết quả.
    
    Tham số:
        input_path: Đường dẫn file CSV đã transform
    
    Trả về:
        Dictionary chứa tất cả các bảng kết quả
    """

    
    # Đọc dữ liệu
    df = pd.read_csv(input_path)
    results = {}
    
    # 1. RemoteWork Overall
    results['remote_overall'] = analyze_remote_work_overall(df)
    results['remote_overall'].to_csv(f'{OUTPUT_DIR}/remote_work_overall.csv', index=False)
    
    # 2. RemoteWork by Experience
    results['remote_by_exp'] = analyze_remote_by_experience(df)
    results['remote_by_exp'].to_csv(f'{OUTPUT_DIR}/remote_by_experience.csv')
    
    # 3. RemoteWork by DevType
    results['remote_by_devtype'] = analyze_remote_by_devtype(df, top_n=10)
    results['remote_by_devtype'].to_csv(f'{OUTPUT_DIR}/remote_by_devtype.csv')
    
    # 4. Top Languages
    results['top_languages'] = analyze_top_languages(df, top_n=15)
    results['top_languages'].to_csv(f'{OUTPUT_DIR}/top_languages.csv', index=False)
    
    # 5. AI Usage
    results['ai_usage'] = analyze_ai_usage(df)
    results['ai_usage'].to_csv(f'{OUTPUT_DIR}/ai_usage.csv', index=False)
    
    # 6. Compensation by Experience
    results['comp_by_exp'] = analyze_compensation_by_experience(df)
    results['comp_by_exp'].to_csv(f'{OUTPUT_DIR}/compensation_by_experience.csv', index=False)
    
    # 7. AI by Experience
    results['ai_by_exp'] = analyze_ai_by_experience(df)
    results['ai_by_exp'].to_csv(f'{OUTPUT_DIR}/ai_by_experience.csv')
    
    # 8. Top Frustrations
    results['top_frustrations'] = analyze_top_frustrations(df, top_n=10)
    if not results['top_frustrations'].empty:
        results['top_frustrations'].to_csv(f'{OUTPUT_DIR}/top_frustrations.csv', index=False)
    
    # 9. Top DevTypes
    results['top_devtypes'] = analyze_top_devtypes(df, top_n=15)
    if not results['top_devtypes'].empty:
        results['top_devtypes'].to_csv(f'{OUTPUT_DIR}/top_devtypes.csv', index=False)
    
    return results




if __name__ == "__main__":
    INPUT_PATH = './data/processed/transformed_developer_survey.csv'
    results = run_analysis(INPUT_PATH)