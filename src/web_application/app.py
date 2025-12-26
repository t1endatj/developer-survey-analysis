"""
app.py - Streamlit Web Application

Ứng dụung web đơn giản đề xuất Roadmap cho Developer
dựa trên dữ liệu phân tích từ Stack Overflow Survey 2024.
"""

import streamlit as st
import sys
import os

# Thêm đường dẫn project root để import được các module
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from roadmap import (
    get_available_roles,
    get_role_display_name,
    generate_roadmap
)


# Cấu hình trang
st.set_page_config(
    page_title="Developer Roadmap Generator",
    page_icon="🚀",
    layout="wide"
)


# CSS 
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .language-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 25px;
        margin: 5px 0;
    }
    
    .language-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 100%;
        display: flex;
        align-items: center;
        padding-left: 10px;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Developer Roadmap Generator</h1>', unsafe_allow_html=True)
    st.markdown("**Đề xuất lộ trình keyword cho Developer dựa trên khảo sát Stack Overflow Survey 2024**")
    
    st.divider()
    
    # Lấy danh sách roles
    roles = get_available_roles()
    
    if not roles:
        st.error("❌ Không tìm thấy dữ liệu. Vui lòng chạy analysis trước!")
        return
    
    # Tạo mapping để hiển thị tên
    role_options = {get_role_display_name(role): role for role in roles}
    
    # Dropdown chọn role
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_display = st.selectbox(
            "🎯 Chọn vai trò của bạn:",
            options=list(role_options.keys()),
            index=0
        )
    
    selected_role = role_options[selected_display]
    
    st.divider()
    
    # Generate roadmap
    roadmap = generate_roadmap(selected_role)
    
    # Hiển thị roadmap
    st.header(f"📋 Roadmap cho {roadmap['role']}")
    
    # Row 1: Languages và Remote Stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Top Ngôn ngữ nên học")
        if roadmap["languages"]:
            for lang in roadmap["languages"]:
                # Progress bar cho mỗi ngôn ngữ
                st.markdown(f"**{lang['rank']}. {lang['name']}**")
                st.progress(lang["percentage"] / 100)
                st.caption(f"{lang['percentage']}% developer sử dụng")
        else:
            st.info("Không có dữ liệu ngôn ngữ")
    
    with col2:
        st.subheader("🏠 Hình thức làm việc")
        if roadmap["remote_stats"]:
            # Hiển thị dưới dạng metrics
            cols = st.columns(3)
            for i, (work_type, percentage) in enumerate(roadmap["remote_stats"].items()):
                with cols[i]:
                    icon = "🏠" if work_type == "Remote" else ("🔄" if work_type == "Hybrid" else "🏢")
                    st.metric(
                        label=f"{icon} {work_type}",
                        value=f"{percentage}%"
                    )
        else:
            st.info("Không có dữ liệu remote work cho role này")
    
    st.divider()
    
    # Row 2: AI Usage và Frustrations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Mức độ sử dụng AI")
        if roadmap["ai_usage"]:
            # Gộp thành 2 nhóm: Có dùng vs Không dùng
            using = roadmap["ai_usage"].get("Using AI", 0)
            not_using = roadmap["ai_usage"].get("Not Using", 0) + roadmap["ai_usage"].get("Planning", 0)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(label="✅ Có dùng AI", value=f"{using}%")
            with col_b:
                st.metric(label="❌ Không dùng", value=f"{not_using:.1f}%")
        else:
            st.info("Không có dữ liệu AI usage")
    
    with col2:
        st.subheader("⚠️ Thách thức thường gặp")
        if roadmap["frustrations"]:
            for frust in roadmap["frustrations"]:
                st.markdown(f"• **{frust['name']}** ({frust['percentage']}%)")
        else:
            st.info("Không có dữ liệu frustrations")
    
    st.divider()
    
    # Row 3: Salary Info
    st.subheader("💰 Thu nhập theo kinh nghiệm (USD/năm)")
    if roadmap["salary_info"]:
        cols = st.columns(len(roadmap["salary_info"]))
        for i, salary in enumerate(roadmap["salary_info"]):
            with cols[i]:
                st.metric(
                    label=salary["level"],
                    value=f"${salary['median']:,}",
                    help=f"Median salary cho {salary['level']}"
                )
    else:
        st.info("Không có dữ liệu lương")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        📊 Dữ liệu từ Stack Overflow Developer Survey 2024<br>
        🔧 Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
