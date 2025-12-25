"""
visualize.py - Trực quan hoá dữ liệu (Matplotlib)

MỤC ĐÍCH FILE NÀY
- Đọc các file CSV đã được xử lý/chuẩn hoá (nằm trong thư mục data/)
- Vẽ các biểu đồ theo yêu cầu đề tài (remote work, AI usage, top languages, frustrations, compensation...)
- Xuất ảnh biểu đồ ra thư mục reports/figures/

CÁCH HOẠT ĐỘNG (TỔNG QUAN)
1) Xác định đường dẫn gốc dự án (BASE_DIR)
2) Từ BASE_DIR suy ra:
   - DATA_DIR  : nơi chứa CSV đầu vào (data/)
   - FIG_DIR   : nơi lưu ảnh đầu ra (reports/figures/)
3) Mỗi hàm plot_*:
   - Đọc đúng 1 file CSV tương ứng
   - Tiền xử lý nhẹ (sort, rename label, reorder nhóm...)
   - Vẽ matplotlib
   - Lưu ảnh vào FIG_DIR

LƯU Ý QUAN TRỌNG
- File này chỉ “vẽ”. Dữ liệu nên được làm sạch/chuẩn hoá từ các bước trước (cleaning/transform/process).
- Nếu muốn đổi cấu trúc thư mục (ví dụ chuyển data/ đi nơi khác) thì cần cập nhật DATA_DIR/FIG_DIR.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


# 1) THIẾT LẬP ĐƯỜNG DẪN
# __file__ là đường dẫn của chính file visualize.py
# dirname 2 lần để lấy thư mục gốc dự án:
#   project_root/
#     data/
#     reports/
#     src/
#       visualize.py   <-- __file__
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Thư mục chứa dữ liệu CSV đầu vào
DATA_DIR = os.path.join(BASE_DIR, "data")

# Thư mục chứa ảnh đầu ra
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")

# Tạo thư mục ảnh nếu chưa tồn tại (để tránh lỗi savefig)
os.makedirs(FIG_DIR, exist_ok=True)


def test_setup():
    """
    Hàm test nhanh để xem đường dẫn và môi trường chạy OK chưa.
    Chạy file visualize.py là bạn sẽ thấy in ra FIG_DIR.
    """
    print("Visualize setup OK")
    print("Figure directory:", FIG_DIR)



# 2) BIỂU ĐỒ: Remote Work Overall (DONUT CHART)

def plot_remote_work_overall():
    """
    Vẽ donut chart cho tỷ lệ hình thức làm việc tổng quan:
    - Remote
    - Hybrid
    - In-person

    Input : data/remote_work_overall.csv
    Output: reports/figures/remote_work_overall.png
    """
    path = os.path.join(DATA_DIR, "remote_work_overall.csv")
    df = pd.read_csv(path)

    labels = df["RemoteWork"]
    values = df["Percentage"]

    plt.figure(figsize=(7, 7))

    # Pie chart dạng donut = pie + wedgeprops(width=...)
    wedges, texts, autotexts = plt.pie(
        values,
        labels=None,               # không ghi nhãn trực tiếp lên miếng (để gọn)
        autopct="%1.2f%%",         # in % trên vòng
        startangle=90,            
        pctdistance=0.75,          # điều chỉnh vị trí chữ % (gần tâm hơn)
        wedgeprops=dict(width=0.4) # tạo “lỗ” ở giữa
    )

    plt.title("Tỉ lệ hình thức làm việc của Developer (2024)")

    # Legend tách riêng bên phải để tránh chật
    plt.legend(
        wedges,
        labels,
        title="Chú thích",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "remote_work_overall.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 3) BIỂU ĐỒ: Remote by Experience (STACKED BAR)

def plot_remote_by_experience():
    """
    Vẽ stacked bar (cột chồng) theo nhóm kinh nghiệm.

    Input : data/remote_by_experience.csv
            index = ExperienceLevel
            cols  = Remote, Hybrid, In-person
    Output: reports/figures/remote_by_experience.png
    """
    path = os.path.join(DATA_DIR, "remote_by_experience.csv")
    df = pd.read_csv(path, index_col=0)

    # Thứ tự nhóm kinh nghiệm để biểu đồ dễ đọc theo “career path”
    order = [
        "Fresher (<1)",
        "Junior (1-2)",
        "Mid-level (3-5)",
        "Senior (6-10)",
        "Lead/Staff (11-20)",
        "Principal+ (21+)"
    ]
    df = df.reindex([i for i in order if i in df.index])

    # Lọc cột hợp lệ (phòng trường hợp thiếu cột)
    cols = [c for c in ["Remote", "Hybrid", "In-person"] if c in df.columns]

    ax = df[cols].plot(kind="bar", stacked=True, figsize=(10, 6))

    ax.set_title("Hình thức làm việc theo nhóm kinh nghiệm")
    ax.set_xlabel("Nhóm kinh nghiệm")
    ax.set_ylabel("Tỉ lệ (%)")

    plt.xticks(rotation=0, fontsize=10)

    # Legend đưa ra ngoài để tránh đè lên chart
    ax.legend(title="Chú thích", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "remote_by_experience.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 4) BIỂU ĐỒ: AI by Experience (STACKED BAR) 

def plot_ai_by_experience():
    """
    Vẽ stacked bar theo nhóm kinh nghiệm (mức độ sử dụng AI).

    Input : data/ai_by_experience.csv
    Output: reports/figures/ai_by_experience_stacked.png
    """
    path = os.path.join(DATA_DIR, "ai_by_experience.csv")
    df = pd.read_csv(path, index_col=0)

    order = [
        "Fresher (<1)",
        "Junior (1-2)",
        "Mid-level (3-5)",
        "Senior (6-10)",
        "Lead/Staff (11-20)",
        "Principal+ (21+)"
    ]
    df = df.reindex([i for i in order if i in df.index])

    cols = [c for c in df.columns if c in ["Using AI", "Planning", "Not Using"]]
    if not cols:

        cols = df.columns.tolist()

    ax = df[cols].plot(kind="bar", stacked=True, figsize=(10, 6))
    ax.set_title("Mức độ sử dụng AI theo nhóm kinh nghiệm")
    ax.set_xlabel("Nhóm kinh nghiệm")
    ax.set_ylabel("Tỉ lệ (%)")

    plt.xticks(rotation=0, fontsize=10)
    ax.legend(title="Chú thích", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "ai_by_experience_stacked.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 5) BIỂU ĐỒ: Top Languages (BARH)

def plot_top_languages():
    """
    Vẽ top ngôn ngữ lập trình phổ biến (bar ngang).

    Input : data/top_languages.csv
            columns: Language, Count
    Output: reports/figures/top_languages.png
    """
    path = os.path.join(DATA_DIR, "top_languages.csv")
    df = pd.read_csv(path)

    # Sắp xếp để barh hiển thị từ thấp -> cao (cao nhất nằm trên cùng)
    df = df.sort_values("Count", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(df["Language"], df["Count"])

    # Chừa khoảng trống bên phải để số không bị tràn khỏi box
    max_val = df["Count"].max()
    ax.set_xlim(0, max_val * 1.15)

    # Ghi số ngay đầu mỗi thanh nhưng vẫn điều chỉnh nằm trong box
    for i, v in enumerate(df["Count"]):
        ax.text(
            v + max_val * 0.01,
            i,
            f"{v:,}",
            va="center",
            ha="left",
            fontsize=10
        )

    ax.set_title("Top 10 ngôn ngữ lập trình phổ biến")
    ax.set_xlabel("Số lượng")
    ax.set_ylabel("Ngôn ngữ")

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "top_languages.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 6) BIỂU ĐỒ: AI Usage Overall (DONUT CHART)

def plot_ai_usage_overall():
    """
    Vẽ donut chart cho mức độ sử dụng AI (tổng quan).

    Input : data/ai_usage.csv
    Output: reports/figures/ai_usage_overall.png
    """
    path = os.path.join(DATA_DIR, "ai_usage.csv")
    df = pd.read_csv(path)

    # Nhãn hiển thị
    labels = [
        "Using AI",
        "Not Using",
        "Planning"
    ]

    values = df.iloc[:, 1].values

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=None,
        autopct="%1.1f%%",
        pctdistance=0.75,
        startangle=90,
        wedgeprops=dict(width=0.4)
    )

    
    plt.legend(
        labels,
        title="Chú thích",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=10
    )

    plt.title("Thống kê mức độ sử dụng AI của Developer")
    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "ai_usage_overall.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 7) BIỂU ĐỒ: Remote by DevType (STACKED BARH)

def plot_remote_by_devtype():
    """
    Vẽ bar ngang dạng stacked theo loại Developer (DevType).

    Input : data/remote_by_devtype.csv
    Output: reports/figures/remote_by_devtype_stacked.png

    Ý tưởng:
    - Rename các DevType dài -> ngắn (Backend/Frontend/...)
    - Sort theo Remote để dễ nhìn (nhóm nào remote ít nằm dưới)
    - Grid nhẹ để đọc % dễ hơn
    - Legend đặt ở góc trái dưới (không đè lên chart)
    """
    path = os.path.join(DATA_DIR, "remote_by_devtype.csv")
    df = pd.read_csv(path, index_col=0)

    # Chuẩn hoá index: tránh case có khoảng trắng đầu/cuối làm rename bị fail
    df.index = df.index.str.strip()

    rename_map = {
        "Developer, back-end": "Backend",
        "Developer, front-end": "Frontend",
        "Developer, mobile": "Mobile",
        "Developer, full-stack": "Full-stack",
        "Data engineer": "Data Engineer",
        "Engineering manager": "Engineering Manager",
        "DevOps specialist": "DevOps",
        "Developer, desktop or enterprise applications": "Desktop / Enterprise",
        "Developer, embedded applications or devices": "Embedded",
        "Other (please specify):": "Other"
    }
    df.rename(index=rename_map, inplace=True)

    cols = ["Remote", "Hybrid", "In-person"]

    # Sort để biểu đồ theo trật tự
    df = df.sort_values(by="Remote", ascending=True)

    ax = df[cols].plot(
        kind="barh",
        stacked=True,
        figsize=(10, 6),
        width=0.7
    )

    ax.set_title("Hình thức làm việc theo loại Developer", fontsize=13)
    ax.set_xlabel("Tỉ lệ (%)")
    ax.set_ylabel("Loại Developer")

    ax.xaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    # Legend: “góc trái dưới cùng” của vùng figure
    # - loc="lower left" là điểm neo (anchor point) của legend
    # - bbox_to_anchor=(x, y) dùng toạ độ tương đối theo axes (0..1)
    #   x=0.0: sát bên trái; y=0.0: sát bên dưới
    ax.legend(
        title="Chú thích",
        loc="lower left",
        bbox_to_anchor=(-0.2, -0.25)
    )



    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "remote_by_devtype_stacked.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 8) BIỂU ĐỒ: Top Frustrations (BARH)

def plot_top_frustrations():
    """
    Vẽ top khó khăn (frustrations) mà developer gặp phải.

    Input : data/top_frustrations.csv
            columns: Frustration, Count, Percentage
    Output: reports/figures/top_frustrations.png
    """
    path = os.path.join(DATA_DIR, "top_frustrations.csv")
    df = pd.read_csv(path)

    # Đổi label dài -> ngắn để biểu đồ gọn hơn
    rename_map = {
        "Amount of technical debt": "Technical debt",
        "Complexity of tech stack for build": "Build complexity",
        "Complexity of tech stack for deployment": "Deployment complexity",
        "Reliability of tools/systems used in work": "Tool/system reliability",
        "Tracking my work": "Work tracking",
        "Patching/updating core components": "System updates",
        "Number of software tools in use": "Too many tools",
        "Showing my contributions": "Showing contributions",
        "Maintaining security of code being produced": "Code security",
        "Maintaining security of systems/platforms used in work": "System security"
    }
    df["Frustration"] = df["Frustration"].replace(rename_map)

    # Sort tăng dần để barh lớn nhất nằm trên cùng
    df = df.sort_values(by="Percentage", ascending=True)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(df["Frustration"], df["Percentage"])

    # Nới xlim để phần text % không bị tràn ra ngoài
    ax = plt.gca()
    ax.set_xlim(0, df["Percentage"].max() + 6)

    plt.title("Top khó khăn mà Developer gặp phải")
    plt.xlabel("Tỉ lệ (%)")
    plt.ylabel("Vấn đề")

    # Ghi % ở cuối mỗi thanh
    for bar, pct in zip(bars, df["Percentage"]):
        plt.text(
            bar.get_width() + 0.6,
            bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%",
            va="center",
            fontsize=9
        )

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "top_frustrations.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()



# 9) BIỂU ĐỒ: Compensation by Experience (MEDIAN)

def plot_compensation_by_experience():
    """
    Vẽ lương trung vị (Median) theo nhóm kinh nghiệm.

    Input : data/compensation_by_experience.csv
            columns: ExperienceLevel, Median, ...
    Output: reports/figures/compensation_by_experience_median.png
    """
    path = os.path.join(DATA_DIR, "compensation_by_experience.csv")
    df = pd.read_csv(path)

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

    plt.figure(figsize=(9, 5))
    bars = plt.bar(df["ExperienceLevel"], df["Median"])

    plt.title("Median thu nhập theo nhóm kinh nghiệm Developer")
    plt.xlabel("Nhóm kinh nghiệm")
    plt.ylabel("Lương trung vị (USD)")

    # Ghi giá trị lên đỉnh cột
    for bar in bars:
        y = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            y + 2000,
            f"${y:,.0f}",
            ha="center",
            fontsize=9
        )

    plt.tight_layout()

    out_path = os.path.join(FIG_DIR, "compensation_by_experience_median.png")
    plt.savefig(out_path, dpi=200)
    plt.close()



# 10) ENTRY POINT (CHẠY TẤT CẢ BIỂU ĐỒ)

if __name__ == "__main__":
    # Chạy test nhanh
    test_setup()

    # Vẽ toàn bộ biểu đồ theo pipeline
    plot_remote_work_overall()
    plot_remote_by_experience()
    plot_ai_by_experience()
    plot_top_languages()
    plot_ai_usage_overall()
    plot_remote_by_devtype()
    plot_top_frustrations()
    plot_compensation_by_experience()
