import streamlit as st
import sqlite3
from datetime import datetime
import pytz
import os
import pandas as pd

# Page Configuration
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Database Initialization
def get_db_connection():
    conn = sqlite3.connect('myproject.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT,
            userid TEXT UNIQUE,
            password TEXT,
            created_at TEXT
        )
    ''')
    # Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userid TEXT,
            q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, q5 INTEGER,
            q6 INTEGER, q7 INTEGER, q8 INTEGER, q9 INTEGER, q10 INTEGER,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'userid' not in st.session_state:
    st.session_state['userid'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Create dummy text and csv for landing page preview if not exist
if not os.path.exists('./data.csv'):
    df_dummy = pd.DataFrame({'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']})
    df_dummy.to_csv('./data.csv', index=False)
if not os.path.exists('./ml.txt'):
    with open('./ml.txt', 'w', encoding='UTF-8') as f:
        f.write("머신러닝 학습 안내 텍스트입니다.")

# Navigation / Sidebar
st.sidebar.title("메뉴")

if st.session_state['logged_in']:
    st.sidebar.write(f"🔑 로그인 완료: {st.session_state['username']}님")
    menu = st.sidebar.radio("이동할 메뉴", ["홈 (대시보드)", "실태조사"])
    
    if st.sidebar.button("로그아웃"):
        st.session_state['logged_in'] = False
        st.session_state['userid'] = None
        st.session_state['username'] = None
        st.rerun()
else:
    st.sidebar.warning("로그인 후 추가 메뉴(실태조사 및 상세페이지)를 이용할 수 있습니다.")
    menu = "홈 (대시보드)"

# Main App Logic
if menu == "홈 (대시보드)":
    if not st.session_state['logged_in']:
        st.title('Welcome! Please Login or Register')
        tab1, tab2 = st.tabs(["로그인", "신규회원가입"])
        
        with tab1:
            st.subheader("로그인")
            login_id = st.text_input("아이디", key="login_id")
            login_pw = st.text_input("비밀번호", type="password", key="login_pw")
            if st.button("로그인 실행"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users WHERE userid = ? AND password = ?", (login_id, login_pw))
                user = cursor.fetchone()
                conn.close()
                
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['userid'] = login_id
                    st.session_state['username'] = user[0]
                    st.success(f"{user[0]}님 환영합니다!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
                    
        with tab2:
            st.subheader("신규회원가입")
            reg_name = st.text_input("이름 (username)", key="reg_name")
            reg_id = st.text_input("아이디 (userid)", key="reg_id")
            reg_pw = st.text_input("비밀번호 (password)", type="password", key="reg_pw")
            
            if st.button("가입하기"):
                if reg_name and reg_id and reg_pw:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    try:
                        ktc_tz = pytz.timezone('Asia/Seoul')
                        now_ktc = datetime.now(ktc_tz).strftime('%Y-%m-%d %H:%M:%S')
                        
                        cursor.execute("INSERT INTO users (username, userid, password, created_at) VALUES (?, ?, ?, ?)",
                                       (reg_name, reg_id, reg_pw, now_ktc))
                        conn.commit()
                        st.success("회원가입이 완료되었습니다! 로그인 탭에서 로그인해주세요.")
                    except sqlite3.IntegrityError:
                        st.error("이미 존재하는 아이디입니다.")
                    finally:
                        conn.close()
                else:
                    st.error("모든 칸을 입력해주세요.")
    else:
        # Original Landing Page Code (Authenticated Only)
        st.title('This is my first webapp')
        image = ['https://www.youtube.com/watch?v=MP8R6kBykzE']
        urls = [
            'https://www.youtube.com/watch?v=KR8ddnPjCtk', 
            'https://www.youtube.com/watch?v=CgSvahZkJmc', 
            'https://www.youtube.com/watch?v=CgSvahZkJmc'
        ]
        
        con1, con2 = st.columns((4,1))
        with con1:
           with st.expander('Content....'):
                for i in range(len(urls)):
                    st.video(urls[0])
                pass
        with con2:
            with st.expander('Tips...'):
                st.image(image[0])
                pass

        con3, con4 = st.columns((4,1))
        with con3:
            with st.expander('Content....'):
                if os.path.exists('./data.csv'):
                    df = pd.read_csv('./data.csv')
                    st.write(df)
                else:
                    st.info("data.csv 파일이 없습니다.")
        with con4:
            with st.expander('Tips...'):
                if os.path.exists('./ml.txt'):
                    with open('./ml.txt', 'r', encoding='UTF-8') as f:
                        mltxt = f.read()
                        st.markdown(mltxt)
                else:
                    st.info("ml.txt 파일이 없습니다.")
                st.image(image[0])
                pass

elif menu == "실태조사":
    st.title("📋 AX 전환에 따른 학생 인식 실태조사")
    st.write("본 설문은 AX(인공지능 전환)에 따른 학생들의 인식을 조사하기 위한 연구용 문항입니다. 각 문항에 성실히 답해 주시기 바랍니다. (1: 전혀 그렇지 않다 ~ 5: 매우 그렇다)")
    
    questions = [
        "1. 나는 AI 기술이 나의 전공 및 학습 능력을 향상시키는 데 기여한다고 생각한다.",
        "2. 학교 수업 내 다양한 AX(인공지능 전환) 시도 및 도입에 대해 긍정적으로 생각한다.",
        "3. 미래 사회에 대비하기 위해 대학에서 AX 관련 교육을 강화해야 한다고 본다.",
        "4. AI 기반 학습 플랫폼이나 도구를 다루는 데 어려움이나 거부감이 없다.",
        "5. 교수자와 학생 간 소통 프로세스에 AI 피드백을 도입하는 방식에 찬성한다.",
        "6. AX 도구를 도입함으로써 전통적인 수업에 비해 학습 집중도가 올라갔다고 느낀다.",
        "7. 향후 취업이나 진로 결정 시 인공지능 활용 능력이 필수적 요인이 될 것으로 예측한다.",
        "8. 우리 대학은 다른 대학에 비해 AX 전환 인프라가 잘 구축되어 있다고 느낀다.",
        "9. 개인 맞춤형 교육 서비스를 제공하는 AI 튜터 시스템이 필요하다고 생각한다.",
        "10. 전반적으로 AX 기반의 캠퍼스 및 교육 변화 흐름에 동참하고 적응할 준비가 되어 있다."
    ]
    
    with st.form("survey_form"):
        responses = []
        for i, q in enumerate(questions):
            score = st.radio(q, options=[1, 2, 3, 4, 5], index=2, horizontal=True, key=f"q_{i+1}")
            responses.append(score)
            
        submitted = st.form_submit_button("설문 제출하기")
        if submitted:
            conn = get_db_connection()
            cursor = conn.cursor()
            ktc_tz = pytz.timezone('Asia/Seoul')
            now_ktc = datetime.now(ktc_tz).strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO inventory (userid, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (st.session_state['userid'], *responses, now_ktc))
            conn.commit()
            conn.close()
            st.success("🎉 실태조사 응답이 성공적으로 기록되었습니다. 감사합니다!")
