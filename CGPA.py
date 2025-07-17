import streamlit as st
import pandas as pd

# ---------- Grade Point Mapping ----------
grade_points = {
    'A': 4.0,
    'B+': 3.5,
    'B': 3.0,
    'C+': 2.5,
    'C': 2.0,
    'F': 0.0
}

# ---------- CGPA Performance Legend ----------
def cgpa_legend(cgpa):
    if cgpa >= 3.7:
        return "Excellent"
    elif 3.30 <= cgpa < 3.7:
        return "Very Good"
    elif 3.0 <= cgpa < 3.30:
        return "Good"
    else:
        return "Fail"

# ---------- Sidebar Legends ----------
# ---------- Grade Point Legend ----------
st.sidebar.markdown(
    """
    <div style="font-family:sans-serif; line-height:1.1; padding-left:5px;">
        <h3 style="margin-bottom:10px;">📘 Grade Point Legend</h3>
        <ul style="list-style:none; padding-left:0; margin-top:0; margin-bottom:20px; font-size:14px;">
            <li style="margin-bottom:15px;"><b>A</b> = 4.0</li>
            <li style="margin-bottom:15px;"><b>B+</b> = 3.5</li>
            <li style="margin-bottom:15px;"><b>B</b> = 3.0</li>
            <li style="margin-bottom:15px;"><b>C+</b> = 2.5</li>
            <li style="margin-bottom:15px;"><b>C</b> = 2.0</li>
            <li style="margin-bottom:15px;"><b>F</b> = 0.0</li>
        </ul>
    </div>

    <hr style="border: 0; height: 2px; background: #DDD; margin: 40px 0 10px 0;">
    """,
    unsafe_allow_html=True,
)

# ---------- Performance Legend ----------
st.sidebar.markdown(
    """
    <div style="font-family:sans-serif; line-height:1.4; padding-left:5px; margin-top:20px;">
        <h3 style="margin-bottom:5px;">📊 Performance Legend</h3>
        <ul style="list-style:none; padding-left:0; margin-top:0; margin-bottom:0; font-size:14px;">
            <li style="margin-bottom:15px;"><b>3.70 - 4.00</b>: Excellent</li>
            <li style="margin-bottom:15px;"><b>3.30 - 3.69</b>: Very Good</li>
            <li style="margin-bottom:15px;"><b>3.00 - 3.29</b>: Good</li>
            <li style="margin-bottom:15px;"><b>Below 3.00</b>: Fail</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------- Main App ----------

st.markdown(
    """
    <h1 style='
        text-align: center; 
        white-space: nowrap; 
        font-size: 35px; 
        margin-top: -30px;
    '>
        🎓 UoS Masters Program GPA and CGPA Calculator
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------- Number of Semesters ----------
num_semesters = st.number_input("Enter number of semesters:", min_value=1, max_value=12, step=1)

all_semester_data = []
total_quality_points = 0
total_credits = 0

# ---------- Input for Each Semester ----------
for sem in range(1, num_semesters + 1):
    st.header(f"📚 Semester {sem}")
    num_courses = st.number_input(f"Number of courses in Semester {sem}:", min_value=1, max_value=12, step=1, key=f"courses_{sem}")
    
    sem_quality_points = 0
    sem_credits = 0
    sem_data = []

    for i in range(num_courses):
        col1, col2, col3 = st.columns(3)
        with col1:
            grade = st.selectbox(f"Grade for Course {i+1} (Sem {sem}):", list(grade_points.keys()), key=f"grade_{sem}_{i}")
        with col2:
            credit = st.number_input(f"Credit Hours:", min_value=1, max_value=6, key=f"credit_{sem}_{i}")
        with col3:
            q_points = grade_points[grade] * credit
            st.write(f"Quality Points: `{q_points:.2f}`")

        sem_quality_points += q_points
        sem_credits += credit
        sem_data.append((grade, credit, q_points))

    # ---------- GPA for the Semester ----------
    if sem_credits > 0:
        semester_gpa = sem_quality_points / sem_credits
        st.success(f"🎯 GPA for Semester {sem}: `{semester_gpa:.2f}`")

    # Store for CGPA
    total_quality_points += sem_quality_points
    total_credits += sem_credits
    all_semester_data.append((sem, semester_gpa, sem_credits))

# ---------- Final CGPA ----------
if total_credits > 0:
    cgpa = total_quality_points / total_credits
    legend = cgpa_legend(cgpa)
    
    st.subheader("🏁 Final Results")
    st.info(f"✅ **Cumulative GPA (CGPA)**: `{cgpa:.2f}`")
    st.markdown(f"**Performance:** 🏅 {legend}")

    st.write(f"📊 Total Quality Points: `{total_quality_points:.2f}`")
    st.write(f"📦 Total Credit Hours: `{total_credits}`")

    # ---------- Show Table ----------
    df = pd.DataFrame(all_semester_data, columns=["Semester", "Semester GPA", "Credits"])
    st.dataframe(df)







