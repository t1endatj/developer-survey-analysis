import pandas as pd
import numpy as np

# dọc dữ liệu gốc
file_path = 'survey_results_public.csv'
df = pd.read_csv(file_path)

# lọc các cột cần thiết
selected_columns = [
    'MainBranch', 'Age', 'YearsCodePro', 'DevType', 
    'LanguageHaveWorkedWith', 'CompTotal', 'RemoteWork', 'AISelect'
]
df = df[selected_columns].copy()

df = df[df['MainBranch'] == 'I am a developer by profession']

# cột kinh nghiệm có 'Less than 1 year', chuyển nó thành 0 và ép kiểu số
df['YearsCodePro'] = df['YearsCodePro'].replace('Less than 1 year', 0)
df['YearsCodePro'] = pd.to_numeric(df['YearsCodePro'], errors='coerce')

# ép kiểu lương sang số
df['CompTotal'] = pd.to_numeric(df['CompTotal'], errors='coerce')

# Loại bỏ giá trị rỗng và lương không hợp lệ
df = df.dropna(subset=['CompTotal', 'YearsCodePro', 'LanguageHaveWorkedWith'])
df = df[df['CompTotal'] > 0]

# xác định nhóm thu nhập hợp lý bằng phương pháp iqr
q1, q3 = np.percentile(df['CompTotal'], [25, 75])
iqr = q3 - q1
lo = q1 - 1.5 * iqr
up = q3 + 1.5 * iqr

df_cleaned = df[(df['CompTotal'] >= lo) &(df['CompTotal'] <= up)].copy()


# xuất dữ liệu sạch ra 
output_path = 'cleaned_developer_survey.csv'
df_cleaned.to_csv(output_path, index=False)
