import datetime
import os
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = "sen_mid2_2_scores.csv"

# 중2반 / 중2-2 학생 명단
STUDENTS = ["김수연", "최윤우", "주지원", "백서윤"]

# 0021 ~ 0076 문항별 선지 및 정답 데이터 (주관식은 5지 선다 변환)
QUESTIONS = {
    "0021": {
        "options": [
            "① ③, ④",
            "② ①, ⑤",
            "③ ③, ⑤ (정답)",
            "④ ②, ④",
            "⑤ ①, ③",
        ],
        "ans": 2,
    },
    "0022": {
        "options": [
            "① (가) ∠C, (나) ∠A, (다) ∠B",
            "② (가) ∠A, (나) ∠B, (다) ∠C",
            "③ (가) ∠B, (나) ∠C, (다) ∠A",
            "④ (가) ∠C, (나) ∠B, (다) ∠A",
            "⑤ (가) ∠A, (나) ∠C, (다) ∠B",
        ],
        "ans": 0,
    },
    "0023": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0024": {
        "options": ["① 36°", "② 40°", "③ 46°", "④ 50°", "⑤ 54°"],
        "ans": 2,
    },
    "0025": {
        "options": ["① 24°", "② 30°", "③ 36°", "④ 42°", "⑤ 48°"],
        "ans": 2,
    },
    "0026": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0027": {"options": ["①", "②", "③", "④", "⑤"], "ans": 3},
    "0028": {
        "options": ["① 12°", "② 15°", "③ 18°", "④ 21°", "⑤ 24°"],
        "ans": 2,
    },
    "0029": {"options": ["①", "②", "③", "④", "⑤"], "ans": 1},
    "0030": {"options": ["①", "②", "③", "④", "⑤"], "ans": 4},
    "0031": {
        "options": ["① 28°", "② 32°", "③ 36°", "④ 40°", "⑤ 44°"],
        "ans": 2,
    },
    "0032": {"options": ["①", "②", "③", "④", "⑤"], "ans": 3},
    "0033": {
        "options": ["① 15°", "② 20°", "③ 25°", "④ 30°", "⑤ 35°"],
        "ans": 2,
    },
    "0034": {
        "options": ["① 10°", "② 15°", "③ 20°", "④ 25°", "⑤ 30°"],
        "ans": 2,
    },
    "0035": {"options": ["①", "②", "③", "④", "⑤"], "ans": 3},
    "0036": {"options": ["①", "②", "③", "④", "⑤"], "ans": 1},
    "0037": {
        "options": ["① 23°", "② 26°", "③ 29°", "④ 32°", "⑤ 35°"],
        "ans": 2,
    },
    "0038": {
        "options": ["① 45°", "② 50°", "③ 55°", "④ 60°", "⑤ 65°"],
        "ans": 3,
    },
    "0039": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0040": {"options": ["①", "②", "③", "④", "⑤"], "ans": 3},
    "0041": {
        "options": [
            "① (1) 100°, (2) 80°",
            "② (1) 108°, (2) 72°",
            "③ (1) 112°, (2) 68°",
            "④ (1) 120°, (2) 60°",
            "⑤ (1) 126°, (2) 54°",
        ],
        "ans": 1,
    },
    "0042": {
        "options": ["① 75°", "② 80°", "③ 85°", "④ 90°", "⑤ 95°"],
        "ans": 3,
    },
    "0043": {"options": ["①", "②", "③", "④", "⑤"], "ans": 4},
    "0044": {
        "options": [
            "① 25 cm²",
            "② 30 cm²",
            "③ 35 cm²",
            "④ 40 cm²",
            "⑤ 45 cm²",
        ],
        "ans": 2,
    },
    "0045": {
        "options": ["① 4 cm", "② 5 cm", "③ 6 cm", "④ 7 cm", "⑤ 8 cm"],
        "ans": 2,
    },
    "0046": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0047": {"options": ["①", "②", "③", "④", "⑤"], "ans": 0},
    "0048": {"options": ["①", "②", "③", "④", "⑤"], "ans": 1},
    "0049": {"options": ["①", "②", "③", "④", "⑤"], "ans": 4},
    "0050": {
        "options": ["① 8 cm", "② 10 cm", "③ 12 cm", "④ 14 cm", "⑤ 16 cm"],
        "ans": 2,
    },
    "0051": {
        "options": [
            "① 6 cm",
            "② 7.5 cm",
            "③ 9 cm",
            "④ 10.5 cm",
            "⑤ 12 cm",
        ],
        "ans": 2,
    },
    "0052": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0053": {"options": ["① 68", "② 72", "③ 76", "④ 80", "⑤ 84"], "ans": 2},
    "0054": {
        "options": [
            "① 10 cm",
            "② 11 cm",
            "③ 12 cm",
            "④ 13 cm",
            "⑤ 14 cm",
        ],
        "ans": 3,
    },
    "0055": {
        "options": [
            "① (ㄱ), (ㄴ)",
            "② (ㄱ), (ㄷ)",
            "③ (ㄴ), (ㄷ)",
            "④ (ㄷ), (ㄹ)",
            "⑤ (ㄹ), (ㅁ)",
        ],
        "ans": 3,
    },
    "0056": {
        "options": [
            "① 12 cm²",
            "② 16 cm²",
            "③ 20 cm²",
            "④ 24 cm²",
            "⑤ 28 cm²",
        ],
        "ans": 2,
    },
    "0057": {
        "options": [
            "① △ABC≡△RQP (RHS), △GHI≡△JKL (RHA)",
            "② △ABC≡△RQP (RHA), △GHI≡△JKL (RHS)",
            "③ △ABC≡△RQP (ASA), △GHI≡△JKL (SAS)",
            "④ △ABC≡△JKL (RHS), △GHI≡△RQP (RHA)",
            "⑤ △ABC≡△JKL (RHA), △GHI≡△RQP (RHS)",
        ],
        "ans": 0,
    },
    "0058": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0059": {"options": ["①", "②", "③", "④", "⑤"], "ans": 4},
    "0060": {
        "options": [
            "① (가) ∠CEB, (나) ∠BCD, (다) RHA",
            "② (가) ∠BCD, (나) ∠CEB, (다) RHS",
            "③ (가) ∠CEB, (나) ∠BCD, (다) RHS",
            "④ (가) ∠BCD, (나) ∠CEB, (다) RHA",
            "⑤ (가) ∠CEB, (나) ∠ABC, (다) ASA",
        ],
        "ans": 0,
    },
    "0061": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0062": {"options": ["①", "②", "③", "④", "⑤"], "ans": 0},
    "0063": {
        "options": ["① 2 cm", "② 3 cm", "③ 4 cm", "④ 5 cm", "⑤ 6 cm"],
        "ans": 1,
    },
    "0064": {
        "options": [
            "① 15 cm²",
            "② 18 cm²",
            "③ 20 cm²",
            "④ 22 cm²",
            "⑤ 25 cm²",
        ],
        "ans": 2,
    },
    "0065": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0066": {
        "options": [
            "① 1 cm²",
            "② 3/2 cm²",
            "③ 2 cm²",
            "④ 5/2 cm²",
            "⑤ 3 cm²",
        ],
        "ans": 1,
    },
    "0067": {"options": ["①", "②", "③", "④", "⑤"], "ans": 1},
    "0068": {
        "options": [
            "① (1) 15°, (2) 2 cm",
            "② (1) 19°, (2) 3 cm",
            "③ (1) 21°, (2) 4 cm",
            "④ (1) 25°, (2) 5 cm",
            "⑤ (1) 30°, (2) 6 cm",
        ],
        "ans": 1,
    },
    "0069": {
        "options": ["① 120°", "② 132°", "③ 144°", "④ 156°", "⑤ 168°"],
        "ans": 2,
    },
    "0070": {"options": ["①", "②", "③", "④", "⑤"], "ans": 3},
    "0071": {
        "options": [
            "① 24 cm²",
            "② 28 cm²",
            "③ 32 cm²",
            "④ 36 cm²",
            "⑤ 40 cm²",
        ],
        "ans": 2,
    },
    "0072": {"options": ["①", "②", "③", "④", "⑤"], "ans": 2},
    "0073": {"options": ["①", "②", "③", "④", "⑤"], "ans": 1},
    "0074": {
        "options": [
            "① 20 cm²",
            "② 22 cm²",
            "③ 24 cm²",
            "④ 26 cm²",
            "⑤ 28 cm²",
        ],
        "ans": 3,
    },
    "0075": {"options": ["①", "②", "③", "④", "⑤"], "ans": 4},
    "0076": {
        "options": ["① 4 cm", "② 5 cm", "③ 6 cm", "④ 7 cm", "⑤ 8 cm"],
        "ans": 2,
    },
}


def load_data():
  if os.path.exists(DATA_FILE):
    return pd.read_csv(DATA_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "제출일시",
            "학생명",
            "교재명",
            "맞은개수",
            "전체문항",
            "환산점수",
            "오답문항",
        ]
    )


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


st.set_page_config(
    page_title="중2-2 쎈 수학 B단계 정답 제출 시스템",
    page_icon="✏️",
    layout="wide",
)
st.title("✏️ 중2-2 쎈 수학 B단계 (0021~0076) 과제 채점 시스템")

df = load_data()
tab1, tab2, tab3 = st.tabs(
    ["✍️ 답안 제출", "📊 전체 성적 대시보드", "👤 학생별 오답 분석"]
)

# 1. 답안 제출 탭
with tab1:
  st.subheader("학생 답안 입력")
  col_user, col_date = st.columns(2)
  with col_user:
    student_name = st.selectbox("학생 이름을 선택하세요", STUDENTS)
  with col_date:
    submit_date = st.date_input("제출일", datetime.date.today())

  st.info("💡 각 문항의 정답을 선택한 후 최하단의 [과제 제출하기] 버튼을 눌러주세요.")

  user_answers = {}
  q_keys = list(QUESTIONS.keys())

  # 10개 문항씩 보기 쉽게 구분
  for i in range(0, len(q_keys), 10):
    chunk = q_keys[i : i + 10]
    with st.expander(
        f"📌 문항 {chunk[0]}번 ~ {chunk[-1]}번 답안 선택", expanded=(i == 0)
    ):
      cols = st.columns(2)
      for idx, q_num in enumerate(chunk):
        q_info = QUESTIONS[q_num]
        with cols[idx % 2]:
          user_answers[q_num] = st.radio(
              f"**{q_num}번**",
              options=range(len(q_info["options"])),
              format_func=lambda x, opts=q_info["options"]: opts[x],
              key=f"q_{q_num}",
              horizontal=True,
          )

  if st.button("🚀 과제 제출 및 채점하기", type="primary", use_container_width=True):
    correct_count = 0
    wrong_list = []

    for q_num, user_ans in user_answers.items():
      if user_ans == QUESTIONS[q_num]["ans"]:
        correct_count += 1
      else:
        wrong_list.append(q_num)

    total_q = len(QUESTIONS)
    score = round((correct_count / total_q) * 100, 1)
    wrong_str = ", ".join(wrong_list) if wrong_list else "없음"

    # 데이터 저장
    new_data = pd.DataFrame([{
        "제출일시": str(submit_date),
        "학생명": student_name,
        "교재명": "쎈 중2-2 B단계 (0021~0076)",
        "맞은개수": correct_count,
        "전체문항": total_q,
        "환산점수": score,
        "오답문항": wrong_str,
    }])

    # 기존 동일 학생 제출 기록이 있으면 갱신, 없으면 추가
    df = df[
        ~((df["학생명"] == student_name) & (df["제출일시"] == str(submit_date)))
    ]
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)

    st.balloons()
    st.success(f"🎉 {student_name} 학생의 과제가 성공적으로 제출되었습니다!")

    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("맞은 개수", f"{correct_count} / {total_q}개")
    res_col2.metric("환산 점수", f"{score}점")
    res_col3.metric("틀린 개수", f"{len(wrong_list)}개")

    if wrong_list:
      st.warning(f"❌ **틀린 문항 번호**: {wrong_str}")
    else:
      st.success("💯 만점입니다! 축하합니다!")

# 2. 반 전체 대시보드 탭
with tab2:
  st.subheader("📊 반 전체 과제 제출 현황")
  if not df.empty:
    avg_score = round(df["환산점수"].mean(), 1)
    m1, m2, m3 = st.columns(3)
    m1.metric("반 평균 점수", f"{avg_score}점")
    m2.metric("과제 제출 인원", f"{len(df['학생명'].unique())} / {len(STUDENTS)}명")
    m3.metric("최고 점수", f"{df['환산점수'].max()}점")

    fig = px.bar(
        df,
        x="학생명",
        y="환산점수",
        text="환산점수",
        color="환산점수",
        title="학생별 쎈 중2-2 B단계 성적",
    )
    fig.update_traces(textposition="outside")
    fig.update_yaxes(range=[0, 110])
    st.plotly_chart(fig, use_container_width=True)

    st.write("**📝 최근 제출 누적 데이터**")
    st.dataframe(
        df.sort_values(by="제출일시", ascending=False), use_container_width=True
    )
  else:
    st.info("아직 제출된 과제 데이터가 없습니다.")

# 3. 학생별 오답 분석 탭
with tab3:
  st.subheader("👤 개별 학생 오답 리포트")
  if not df.empty:
    selected_stu = st.selectbox("학생 선택", STUDENTS, key="analyze_stu")
    stu_df = df[df["학생명"] == selected_stu]

    if not stu_df.empty:
      latest_rec = stu_df.iloc[-1]
      st.write(f"### 📌 {selected_stu} 학생 리포트")
      st.write(
          f"- **맞은 개수**: {latest_rec['맞은개수']}개 / {latest_rec['전체문항']}개"
      )
      st.write(f"- **환산 점수**: {latest_rec['환산점수']}점")
      st.write(f"- **오답 문항**: {latest_rec['오답문항']}")
    else:
      st.warning(f"{selected_stu} 학생의 제출 기록이 없습니다.")
  else:
    st.info("데이터가 없습니다.")