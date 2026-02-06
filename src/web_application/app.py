"""
app.py - Developer Roadmap Web Application
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

# Constants
PAGE_TITLE = "Developer Roadmap Generator"
PAGE_ICON = "🚀"
LAYOUT = "wide"

# Cấu hình trang
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

def display_languages_section(languages):
    """Hiển thị section ngôn ngữ lập trình."""
    st.subheader("📚 Top Ngôn ngữ nên học")
    if languages:
        for lang in languages:
            st.markdown(f"**{lang['rank']}. {lang['name']}**")
            st.progress(lang["percentage"] / 100)
            st.caption(f"{lang['percentage']}% developer sử dụng")
    else:
        st.info("Không có dữ liệu ngôn ngữ")

def main():
    """
    Hàm chính hiển thị giao diện web application.
    Cho phép người dùng chọn role và xem roadmap tương ứng.
    """
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
    st.header(f"📋 Roadmap cho {roadmap[\'role\']}")
    
    # Row 1: Languages và Remote Stats
    col1, col2 = st.columns(2)
    
    with col1:
        display_languages_section(roadmap["languages"])
    
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
    
    # Row 3: Salary Info theo ngành nghề
    st.subheader(f"💰 Thu nhập theo kinh nghiệm - {roadmap['role']} (USD/năm)")
    if roadmap["salary_info"]:
        cols = st.columns(len(roadmap["salary_info"]))
        for i, salary in enumerate(roadmap["salary_info"]):
            with cols[i]:
                # Hiển thị số mẫu 
                help_text = f"Median salary cho {salary['level']}"
                if salary.get('count'):
                    help_text += f" (n={salary['count']:,})"
                
                st.metric(
                    label=salary["level"],
                    value=f"${salary['median']:,}",
                    help=help_text
                )
    else:
        st.info("Không có dữ liệu lương cho ngành này")
    
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