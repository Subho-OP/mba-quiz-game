# ============================================
# 🎮 MBA Specialization Quiz Game (Dark Mode UI + Default Neutral + Responsive)
# ============================================

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# -------------------
# APP CONFIGURATION
# -------------------
st.set_page_config(page_title="MBA Quiz Game", page_icon="🎓", layout="wide")

# -------------------
# DATABASE SETUP
# -------------------
conn = sqlite3.connect("results.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS student_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_number TEXT,
    specialization1 TEXT,
    score1 REAL,
    specialization2 TEXT,
    score2 REAL,
    specialization3 TEXT,
    score3 REAL,
    full_score_data TEXT,
    date_taken TEXT
)
""")
conn.commit()

# -------------------
# DARK MODE STYLING
# -------------------
st.markdown("""
<style>
/* Dark gradient background */
body {
    background: radial-gradient(circle at top left, #0e0f12, #121318, #1a1b21);
    color: #f5f5f5 !important;
    font-family: 'Inter', sans-serif;
}

/* Main container glass effect */
.block-container {
    max-width: 900px !important;
    margin: auto;
    padding: 2rem 1.5rem !important;
    background: rgba(25, 25, 32, 0.8);
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.1);
    backdrop-filter: blur(20px);
}

/* Headings */
h1, h2, h3 {
    text-align: center !important;
    color: #00ffff !important;
    font-weight: 700;
}

/* Text inputs */
.stTextInput input {
    border-radius: 10px !important;
    background-color: rgba(255, 255, 255, 0.07);
    border: 1px solid #2dd4bf !important;
    color: #fff !important;
    padding: 0.7rem 1rem !important;
    font-size: 1rem !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00b4d8, #0077b6);
    border: none;
    border-radius: 12px;
    color: #fff;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.8rem 1rem;
    width: 100%;
    transition: all 0.25s ease-in-out;
    box-shadow: 0px 3px 12px rgba(0, 255, 255, 0.2);
}
.stButton button:hover {
    background: linear-gradient(90deg, #0096c7, #023e8a);
    transform: scale(1.03);
}

/* Radio buttons */
.stRadio > div {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.stRadio label {
    color: #e0e0e0 !important;
    font-size: 1rem !important;
    font-weight: 500;
}

/* Progress bar */
.stProgress > div > div {
    height: 22px !important;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #00b4d8, #0077b6);
}

/* DataFrame styling */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    background-color: #181a1f !important;
    color: #ffffff !important;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    h1, h2, h3 {
        font-size: 1.4rem !important;
    }
    .stRadio > div {
        flex-direction: column !important;
        align-items: flex-start !important;
    }
    .stButton button {
        font-size: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------
# QUESTIONS DATA
# -------------------
questions = pd.DataFrame([
    ("I enjoy analyzing financial statements and company balance sheets.", "Finance"),
    ("I’m comfortable making investment and budgeting decisions.", "Finance"),
    ("I follow stock markets, economic trends, and business news regularly.", "Finance"),
    ("I’m interested in corporate valuation and risk management.", "Finance"),
    ("I’m passionate about understanding customer needs and behavior.", "Marketing"),
    ("I enjoy designing advertising or promotional campaigns.", "Marketing"),
    ("I like creating brand strategies to increase market share.", "Marketing"),
    ("I am skilled in using social media and digital tools for business.", "Marketing"),
    ("I like improving efficiency and reducing waste in business processes.", "Operations / Supply Chain"),
    ("I enjoy managing logistics, inventory, and production schedules.", "Operations / Supply Chain"),
    ("I’m detail-oriented when planning and executing projects.", "Operations / Supply Chain"),
    ("I’m interested in Six Sigma, Lean, or quality improvement methods.", "Operations / Supply Chain"),
    ("I enjoy resolving interpersonal conflicts and fostering teamwork.", "Human Resources (HR)"),
    ("I like recruiting, interviewing, and evaluating candidates.", "Human Resources (HR)"),
    ("I’m interested in designing employee engagement and retention programs.", "Human Resources (HR)"),
    ("I understand the importance of organizational culture and motivation.", "Human Resources (HR)"),
    ("I’m fascinated by how technology transforms business operations.", "Information Technology (IT Management)"),
    ("I enjoy managing IT projects or working with software systems.", "Information Technology (IT Management)"),
    ("I can translate business needs into technical requirements.", "Information Technology (IT Management)"),
    ("I like exploring emerging technologies such as AI, IoT, and cloud computing.", "Information Technology (IT Management)"),
    ("I enjoy working with data to uncover patterns and insights.", "Business Analytics / Data Science"),
    ("I’m comfortable using tools like Excel, SQL, Python, or R.", "Business Analytics / Data Science"),
    ("I like making data-driven decisions and visualizing business trends.", "Business Analytics / Data Science"),
    ("I’m interested in predictive modeling and machine learning applications.", "Business Analytics / Data Science"),
    ("I enjoy solving complex business problems strategically.", "Strategy & Consulting"),
    ("I like analyzing case studies and designing business solutions.", "Strategy & Consulting"),
    ("I have strong critical thinking and decision-making skills.", "Strategy & Consulting"),
    ("I’m interested in management consulting or corporate strategy roles.", "Strategy & Consulting"),
    ("I’m passionate about starting my own business or venture.", "Entrepreneurship"),
    ("I enjoy identifying new market opportunities and innovations.", "Entrepreneurship"),
    ("I’m willing to take calculated risks and handle uncertainty.", "Entrepreneurship"),
    ("I like building business plans and pitching ideas to investors.", "Entrepreneurship"),
    ("I enjoy understanding cross-cultural business dynamics.", "International Business"),
    ("I’m interested in working with multinational corporations.", "International Business"),
    ("I like studying trade policies, global markets, and international strategy.", "International Business"),
    ("I’m open to relocating or working across countries and cultures.", "International Business"),
    ("I’m interested in how hospitals and healthcare systems operate.", "Healthcare Management"),
    ("I want to improve efficiency and patient outcomes in healthcare.", "Healthcare Management"),
    ("I enjoy learning about healthcare policy, insurance, and regulation.", "Healthcare Management"),
    ("I like analyzing data or managing operations in healthcare settings.", "Healthcare Management"),
], columns=["Statement", "Specialization"])

total_questions = len(questions)

# -------------------
# SESSION STATE INIT
# -------------------
if "page" not in st.session_state:
    st.session_state.page = "student_info"
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "roll_number" not in st.session_state:
    st.session_state.roll_number = ""

# -------------------
# PAGE 1: STUDENT INFO
# -------------------
if st.session_state.page == "student_info":
    st.title("🎓 MBA Specialization Quiz Game")
    st.markdown("Welcome! Enter your details to start your personalized MBA specialization quiz.")

    name = st.text_input("👤 Full Name", placeholder="Enter your full name")
    roll = st.text_input("🧾 Roll Number", placeholder="Enter your roll number")

    st.write("")
    if st.button("🚀 Start Quiz", use_container_width=True):
        if not name.strip() or not roll.strip():
            st.error("⚠️ Please fill in both fields before starting.")
        else:
            st.session_state.student_name = name
            st.session_state.roll_number = roll
            st.session_state.page = "quiz"
            st.rerun()

# -------------------
# PAGE 2: QUIZ
# -------------------
elif st.session_state.page == "quiz":
    current_index = st.session_state.current_q
    progress = min(current_index / total_questions, 1.0)
    st.progress(progress)

    if current_index < total_questions:
        q = questions.iloc[current_index]
        st.markdown(f"### Question {current_index + 1} of {total_questions}")
        st.markdown(f"**{q['Statement']}**")

        rating = st.radio(
            "Select your response:",
            [1, 2, 3, 4, 5],
            format_func=lambda x: {
                1: "1️⃣ Strongly Disagree",
                2: "2️⃣ Disagree",
                3: "3️⃣ Neutral",
                4: "4️⃣ Agree",
                5: "5️⃣ Strongly Agree",
            }[x],
            horizontal=True,
            index=2,  # Default Neutral
            key=f"q_{current_index}"
        )

        if st.button("Next ➡️", use_container_width=True):
            st.session_state.responses.append((q["Specialization"], rating))
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.page = "result"
        st.rerun()

# -------------------
# PAGE 3: RESULT
# -------------------
elif st.session_state.page == "result":
    st.success("✅ Quiz Completed! Great job!")
    st.balloons()

    responses_df = pd.DataFrame(st.session_state.responses, columns=["Specialization", "Response"])
    scores = responses_df.groupby("Specialization")["Response"].sum().reset_index()
    scores["normalized_score"] = scores["Response"] / (5 * 4)
    scores = scores.sort_values("normalized_score", ascending=False).reset_index(drop=True)
    top3 = scores.head(3)

    st.markdown(f"## 🏆 Top 3 MBA Specializations for **{st.session_state.student_name}**")
    for i, row in top3.iterrows():
        st.subheader(f"{i+1}. {row['Specialization']} — {row['normalized_score']:.2f}")
        st.progress(row["normalized_score"])

    cursor.execute("""
        INSERT INTO student_results (
            name, roll_number,
            specialization1, score1,
            specialization2, score2,
            specialization3, score3,
            full_score_data, date_taken
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        st.session_state.student_name,
        st.session_state.roll_number,
        top3.iloc[0]['Specialization'], top3.iloc[0]['normalized_score'],
        top3.iloc[1]['Specialization'], top3.iloc[1]['normalized_score'],
        top3.iloc[2]['Specialization'], top3.iloc[2]['normalized_score'],
        scores.to_json(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    st.markdown("✅ Your result has been **saved successfully!**")

    st.markdown("---")
    st.markdown("### 📊 Complete Score Breakdown")
    st.dataframe(scores, use_container_width=True)
    st.bar_chart(scores.set_index("Specialization")["normalized_score"], use_container_width=True)

    if st.button("🔄 Play Again", use_container_width=True):
        st.session_state.page = "student_info"
        st.session_state.current_q = 0
        st.session_state.responses = []
        st.rerun()
