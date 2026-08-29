import datetime
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = "sen_mid2_2_scores.csv"
UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔒 선생님 전용 비밀번호 (원하시는 비밀번호로 변경해서 사용하세요)
TEACHER_PASSWORD = "1234"

# ✉️ 이메일 알림 설정 (Gmail)
SENDER_EMAIL = "pend9494@gmail.com"  # 발송용 Gmail 주소
SENDER_PASSWORD = "gson fpcr mlcz kzfy"  # Gmail 앱 비밀번호 (16자리)
RECEIVER_EMAIL = "pend9494@gmail.com"  # 선생님 이메일 주소

# 가락고반 / 중2-2 학생 명단
STUDENTS = ["김수연", "백서윤", "주지원", "최윤우"]

# 0021 ~ 0076 문항 데이터
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

RANGE_PART1 = [f"{i:04d}" for i in range(21, 51)]
RANGE_PART2 = [f"{i:04d}" for i in range(51, 77)]


def load_data():
  if os.path.exists(DATA_FILE):
    return pd.read_csv(DATA_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "제출일시",
            "학생명",
            "과제범위",
            "맞은개수",
            "전체문항",
            "환산점수",
            "오답문항",
            "사진경로",
        ]
    )


def save_data(df):
  df.to_csv(DATA_FILE, index=False)


def send_email_notification(
    student_name,
    range_title,
    score,
    correct_count,
    total_q,
    wrong_str,
    photo_path=None,
):
  if (
      SENDER_EMAIL == "your_email@gmail.com"
      or SENDER_PASSWORD == "your_app_password"
  ):
    return

  try:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = (
        f"[과제 제출 알림] {student_name} 학생 - {range_title} ({score}점)"
    )

    body = f"""
    안녕하세요 박지호 선생님,

    {student_name} 학생이 과제 답안을 제출했습니다.

    ■ 학생명: {student_name}
    ■ 과제 범위: {range_title}
    ■ 맞은 개수: {correct_count} / {total_q} 개
    ■ 환산 점수: {score} 점
    ■ 오답 문항: {wrong_str}

    감사합니다.
    """
    msg.attach(MIMEText(body, "plain"))

    if photo_path and os.path.exists(photo_path):
      with open(photo_path, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(photo_path),
        )
        msg.attach(img)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
  except Exception as e:
    st.error(f"이메일 알림 전송 중 오류 발생: {e}")


st.set_page_config(
    page_title="중2-2 쎈 수학 B단계 과제 채점 시스템",
    page_icon="✏️",
    layout="wide",
)
st.title("✏️ 중2-2 쎈 수학 B단계 과제 채점 시스템")

df = load_data()
tab1, tab2, tab3 = st.tabs(
    ["✍️ 답안 제출", "📊 전체 성적 대시보드 (선생님)", "👤 학생별 오답 분석 (선생님)"]
)

# -------------------------------------------------------------------
# 1. 답안 제출 탭 (학생용) - 데이터 삭제 UI 절대 없음
# -------------------------------------------------------------------
with tab1:
  st.subheader("학생 답안 입력")
  col_user, col_range, col_date = st.columns([1, 1.5, 1])

  with col_user:
    student_name = st.selectbox("학생 이름을 선택하세요", STUDENTS)
  with col_range:
    selected_range_label = st.radio(
        "과제 범위를 선택하세요",
        ["0021번 ~ 0050번 (Part 1)", "0051번 ~ 0076번 (Part 2)"],
        horizontal=True,
    )
  with col_date:
    submit_date = st.date_input("제출일", datetime.date.today())

  if "0021" in selected_range_label:
    target_keys = RANGE_PART1
    range_title = "쎈 중2-2 B단계 (0021~0050)"
  else:
    target_keys = RANGE_PART2
    range_title = "쎈 중2-2 B단계 (0051~0076)"

  st.info(
      f"💡 **[{range_title}]** 총 {len(target_keys)}문항입니다. 정답을 선택한 후 최하단의 [과제 제출하기] 버튼을 눌러주세요."
  )

  user_answers = {}
  for i in range(0, len(target_keys), 10):
    chunk = target_keys[i : i + 10]
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
              key=f"q_{q_num}_{selected_range_label}",
              horizontal=True,
          )

  st.write("---")
  st.subheader("📸 풀이 과정 사진 첨부 (선택)")
  photo_method = st.radio(
      "사진 제출 방식을 선택하세요",
      ["제출 안 함", "파일 업로드 (갤러리)", "카메라로 직접 촬영"],
      horizontal=True,
  )

  uploaded_photo = None
  if photo_method == "파일 업로드 (갤러리)":
    uploaded_photo = st.file_uploader(
        "풀이 사진을 선택하세요", type=["png", "jpg", "jpeg"]
    )
  elif photo_method == "카메라로 직접 촬영":
    uploaded_photo = st.camera_input("풀이 과정 촬영")

  if st.button("🚀 과제 제출 및 채점하기", type="primary", use_container_width=True):
    correct_count = 0
    wrong_list = []

    for q_num, user_ans in user_answers.items():
      if user_ans == QUESTIONS[q_num]["ans"]:
        correct_count += 1
      else:
        wrong_list.append(q_num)

    total_q = len(target_keys)
    score = round((correct_count / total_q) * 100, 1)
    wrong_str = ", ".join(wrong_list) if wrong_list else "없음"

    saved_photo_path = ""
    if uploaded_photo is not None:
      file_ext = uploaded_photo.name.split(".")[-1] if hasattr(
          uploaded_photo, "name"
      ) else "png"
      filename = f"{submit_date}_{student_name}_{range_title.replace(' ', '_')}.{file_ext}"
      saved_photo_path = os.path.join(UPLOAD_DIR, filename)
      with open(saved_photo_path, "wb") as f:
        f.write(uploaded_photo.getbuffer())

    new_data = pd.DataFrame([{
        "제출일시": str(submit_date),
        "학생명": student_name,
        "과제범위": range_title,
        "맞은개수": correct_count,
        "전체문항": total_q,
        "환산점수": score,
        "오답문항": wrong_str,
        "사진경로": saved_photo_path,
    }])

    df = df[
        ~(
            (df["학생명"] == student_name)
            & (df["과제범위"] == range_title)
            & (df["제출일시"] == str(submit_date))
        )
    ]
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)

    send_email_notification(
        student_name,
        range_title,
        score,
        correct_count,
        total_q,
        wrong_str,
        saved_photo_path,
    )

    st.balloons()
    st.success(
        f"🎉 {student_name} 학생의 **[{range_title}]** 과제가 성공적으로 제출되었습니다!"
    )

    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("맞은 개수", f"{correct_count} / {total_q}개")
    res_col2.metric("환산 점수", f"{score}점")
    res_col3.metric("틀린 개수", f"{len(wrong_list)}개")

    if wrong_list:
      st.warning(f"❌ **틀린 문항 번호**: {wrong_str}")
    else:
      st.success("💯 만점입니다! 축하합니다!")

# -------------------------------------------------------------------
# 2. 반 전체 대시보드 탭 (선생님 전용) - 비밀번호 통과 시에만 삭제기능 노출
# -------------------------------------------------------------------
with tab2:
  st.subheader("📊 반 전체 과제 제출 현황 (선생님 전용)")
  teacher_pw2 = st.text_input(
      "🔒 선생님 비밀번호를 입력하세요", type="password", key="pw_tab2"
  )

  if teacher_pw2 == TEACHER_PASSWORD:
    if not df.empty:
      selected_view_range = st.selectbox(
          "조회할 과제 범위 선택",
          ["전체 보기", "0021~0050 (Part 1)", "0051~0076 (Part 2)"],
      )

      filtered_df = df.copy()
      if "0021" in selected_view_range:
        filtered_df = filtered_df[
            filtered_df["과제범위"].str.contains("0021~0050")
        ]
      elif "0051" in selected_view_range:
        filtered_df = filtered_df[
            filtered_df["과제범위"].str.contains("0051~0076")
        ]

      if not filtered_df.empty:
        avg_score = round(filtered_df["환산점수"].mean(), 1)
        m1, m2, m3 = st.columns(3)
        m1.metric("평균 점수", f"{avg_score}점")
        m2.metric(
            "제출 건수",
            f"{len(filtered_df['학생명'].unique())} / {len(STUDENTS)}명",
        )
        m3.metric("최고 점수", f"{filtered_df['환산점수'].max()}점")

        fig = px.bar(
            filtered_df,
            x="학생명",
            y="환산점수",
            color="과제범위",
            barmode="group",
            text="환산점수",
            title="학생별 과제 성적 비교",
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)

        st.write("**📝 최근 제출 누적 데이터**")
        st.dataframe(
            filtered_df.sort_values(by="제출일시", ascending=False),
            use_container_width=True,
        )

        # 🗑️ [선생님 전용] 데이터 삭제 기능 (비밀번호 인증 내부)
        st.write("---")
        st.write("🗑️ **[선생님 전용] 제출 데이터 삭제**")

        df_del = df.copy()
        df_del["select_label"] = df_del.apply(
            lambda r: (
                f"{r['학생명']} | {r['제출일시']} | {r['과제범위']} ({r['환산점수']}점)"
            ),
            axis=1,
        )

        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
          selected_del_label = st.selectbox(
              "삭제할 제출 기록을 선택하세요",
              df_del["select_label"].unique(),
              key="del_select",
          )

        with del_col2:
          st.write(" ")
          st.write(" ")
          if st.button(
              "❌ 선택 기록 삭제", type="primary", key="del_btn_action"
          ):
            target_row = df_del[
                df_del["select_label"] == selected_del_label
            ].iloc[0]

            # 사진 파일도 존재하는 경우 함께 삭제
            photo_p = target_row.get("사진경로", "")
            if pd.notna(photo_p) and photo_p and os.path.exists(photo_p):
              try:
                os.remove(photo_p)
              except Exception:
                pass

            df = df[
                ~(
                    (df["학생명"] == target_row["학생명"])
                    & (df["제출일시"] == str(target_row["제출일시"]))
                    & (df["과제범위"] == target_row["과제범위"])
                )
            ]
            save_data(df)
            st.success("해당 과제 제출 기록이 완전히 삭제되었습니다.")
            st.rerun()

      else:
        st.info("선택한 범위의 제출 데이터가 없습니다.")
    else:
      st.info("아직 제출된 과제 데이터가 없습니다.")
  elif teacher_pw2 != "":
    st.error("비밀번호가 올바르지 않습니다.")
  else:
    st.warning("선생님 전용 공간입니다. 비밀번호를 입력해주세요.")

# -------------------------------------------------------------------
# 3. 학생별 오답 분석 탭 (선생님 전용)
# -------------------------------------------------------------------
with tab3:
  st.subheader("👤 개별 학생 오답 리포트 및 풀이 사진 (선생님 전용)")
  teacher_pw3 = st.text_input(
      "🔒 선생님 비밀번호를 입력하세요", type="password", key="pw_tab3"
  )

  if teacher_pw3 == TEACHER_PASSWORD:
    if not df.empty:
      selected_stu = st.selectbox("학생 선택", STUDENTS, key="analyze_stu")
      stu_df = df[df["학생명"] == selected_stu]

      if not stu_df.empty:
        st.write(f"### 📌 {selected_stu} 학생 누적 제출 기록")
        st.dataframe(
            stu_df[
                [
                    "제출일시",
                    "과제범위",
                    "맞은개수",
                    "환산점수",
                    "오답문항",
                    "사진경로",
                ]
            ],
            use_container_width=True,
        )

        st.write("---")
        st.write("🖼️ **제출된 풀이과정 사진 확인**")
        for _, row in stu_df.iterrows():
          photo_p = row.get("사진경로", "")
          if pd.notna(photo_p) and photo_p and os.path.exists(photo_p):
            st.image(
                photo_p,
                caption=f"[{row['제출일시']}] {row['과제범위']} - {selected_stu} 학생 풀이",
                width=500,
            )
          else:
            st.caption(
                f"[{row['제출일시']}] {row['과제범위']} - 제출된 사진 없음"
            )
      else:
        st.warning(f"{selected_stu} 학생의 제출 기록이 없습니다.")
    else:
      st.info("데이터가 없습니다.")
  elif teacher_pw3 != "":
    st.error("비밀번호가 올바르지 않습니다.")
  else:
    st.warning("선생님 전용 공간입니다. 비밀번호를 입력해주세요.")