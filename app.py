import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPEN_AI_KEY"])  # 또는 직접 문자열 입력

st.set_page_config(page_title="AI 헬스트레이너", layout="wide")
st.title("💪 AI 헬스 트레이너")
st.markdown("당신의 운동 목표에 맞춘 트레이닝 플랜과 식단을 추천해드립니다!")

# 입력 UI
goal = st.selectbox("🏆 운동 목표를 선택하세요", ["다이어트", "근육 증가", "체력 증진"])
experience = st.radio("🏋️ 운동 경력", ["초보", "중급", "고급"])
days = st.slider("📆 주당 운동 횟수", 1, 7, 3)

if st.button("트레이닝 플랜 받기"):
    with st.spinner("GPT가 맞춤형 플랜을 생성 중입니다..."):
        user_prompt = f"""
운동 목표: {goal}
운동 경력: {experience}
주당 운동 횟수: {days}

위 정보를 바탕으로 아래 JSON 형식으로 트레이닝 계획을 추천해줘:

{{
  "운동 루틴": [],
  "식단 추천": [],
  "주의사항": ""
}}
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "너는 피트니스 전문가야. 사용자에게 맞는 운동/식단/주의사항을 JSON으로 추천해줘."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            result = response.choices[0].message.content
            st.subheader("📋 추천 결과:")
            st.code(result, language="json")

            try:
                parsed = json.loads(result)
                st.json(parsed)
            except json.JSONDecodeError:
                st.error("❌ GPT 응답이 JSON 형식이 아닙니다.")
        except Exception as e:
            st.error(f"오류 발생: {e}")
