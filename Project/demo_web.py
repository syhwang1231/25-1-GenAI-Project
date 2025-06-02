import streamlit as st
import os
from transcriber import transcribe_audio
from summarizer import generate_minutes

st.set_page_config(layout = "wide")

st.title("🎙 Whisper-to-GPT - 회의록 작성 및 구조화 AI")
st.caption("\"이 안건 분명히 논의했던 적 있었던 것 같은데.. 회의록에 안 적혀있네?\", \"이야기를 나누느라 회의록에 적어두는 걸 깜빡했다!\"\n이제 회의록 작성은 AI에게 맡겨두고, 맘 편히 회의를 진행하세요.")

# 템플릿 입력
st.subheader("🧾 우리 팀 회의록 템플릿 (Markdown 형식)")
default_template = """첫번째로, 회의 안건에는 회의 내용이 전체적으로 어떤 주제를 다루었는지에 대한 내용이야.
두번째로, 회의 내용은 파트별 회의 내용, 결정 사항으로 나누어. 파트별 회의 내용에서는 서버, 안드로이드, ios, 디자인 파트별로 어떤 이슈가 있었는지에 대해 작성해. 결정 사항에서는 특별히 새로 결정된 사항이나 새로 다룬 내용에 대해 작성해.
마지막으로, 다음 회의에는 다음 회의에 관해 결정된 사항을 정리해. (ex. 다음 회의 날짜, 다음 회의까지 해와야 하는 일 등)

## >> 회의 안건
---
- 

## >> 회의 내용
---
### 파트별 회의 내용
- 서버
    - 
- 안드
    - 
- 아요
    - 
- 디쟌
    - 

### 결정 사항
- 

## >> 다음 회의
---
- 

"""
user_prompt = st.text_area("사용자 지정 템플릿 (프롬프트 포함) - 각각 꼭 들어가야하는 내용을 언급해주면 더 좋아요.", default_template, height=300)

# 업로드 방식 선택
st.subheader("2️⃣ 업로드 방식 선택")
st.caption("⚠️ 음성 파일을 선택할 경우, 텍스트로 변환하는 과정이 필요하므로 시간이 더 소요될 수 있어요.")
upload_method = st.radio("회의 내용 업로드 방식을 선택하세요:", ("음성 파일", "텍스트 파일"))

if upload_method == "음성 파일":
    uploaded_audio = st.file_uploader("음성 파일 업로드", type=["mp3", "wav", "m4a", "mov"])

    if uploaded_audio and "transcribed_text" not in st.session_state:
        with st.spinner("Whisper에게 텍스트 변환 요청 중...💭", show_time=True):
            with open("temp_audio", "wb") as f:
                f.write(uploaded_audio.read())

            text = transcribe_audio("temp_audio")
            st.session_state.transcribed_text = text

    # 변환된 텍스트 가져오기
    if "transcribed_text" in st.session_state:
        text = st.session_state.transcribed_text
        st.subheader("📝 텍스트 변환 결과")
        st.text_area("Transcript", text, height=200)

        if st.button("회의록 생성"):
            with st.spinner("GPT에게 회의록 요약 요청 중...📝", show_time=True):
                summary = generate_minutes(user_prompt, text)
                st.subheader("3️⃣ 📄 생성된 회의록")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 렌더링된 회의록")
                    st.markdown(summary)

                with col2:
                    st.markdown("### Markdown 원문")
                    st.code(summary, language="markdown")

elif upload_method == "텍스트 파일":
    uploaded_text = st.file_uploader("텍스트 파일 업로드", type=["txt"])

    if uploaded_text:
        text = uploaded_text.read().decode("utf-8")
        st.subheader("📝 텍스트 파일 내용")
        st.text_area("Transcript", text, height=200)

        if st.button("회의록 생성"):
            with st.spinner("GPT에게 회의록 요약 요청 중...📝", show_time = True):
                summary = generate_minutes(user_prompt, text)
                st.subheader("3️⃣ 📄 생성된 회의록")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 렌더링된 회의록")
                    st.markdown(summary)

                with col2:
                    st.markdown("### Markdown 원문")
                    st.code(summary, language="markdown")