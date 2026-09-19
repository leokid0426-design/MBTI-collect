import streamlit as st
import json
from datetime import datetime
from ai_helper import ask_ai
from collections import Counter

st.set_page_config(page_title="우리반 MBTI수집소", layout="wide")

def load_records():
    try:
        with open("mbti.json", encoding="utf-8") as f:
            return json.load(f)["records"]
    except FileNotFoundError:
        return []

def save_records(records):
    data = {"title": "우리 반 MBTI 수집소", "records": records}
    with open("mbti.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_mbti_from_ai(answers_text):
    # 답변 분석해서 MBTI 계산
    answers_lower = answers_text.lower()

    # E/I 판단: 새로운 사람 만나는 것을 좋아하나? (네=E, 아니요=I)
    q1_ye = "네" in answers_text.split("\n")[0]

    # T/F 판단: 논리적인가? (논리적=T, 감정적=F)
    q2_logical = "논리적" in answers_text or ("논리" in answers_text and "감정" not in answers_text)

    # J/P 판단: 계획적인가? (네=J, 아니요=P)
    q3_plan = "네" in answers_text.split("\n")[2] if len(answers_text.split("\n")) > 2 else True

    # S/N 판단: 현재 감각 중심 vs 직관 (간단히 하기 위해 임의로)
    q4_alone = "네" in answers_text.split("\n")[3] if len(answers_text.split("\n")) > 3 else True

    # MBTI 조합
    mbti_code = (
        ("E" if q1_ye else "I") +
        ("N" if q4_alone else "S") +
        ("T" if q2_logical else "F") +
        ("J" if q3_plan else "P")
    )

    # MBTI별 별명 및 설명 정의
    mbti_data = {
        "INTJ": ("통찰력의 전략가", "혼자만의 시간을 소중히 여기고 깊이 있는 통찰력으로 미래를 계획하는 타입입니다."),
        "INTP": ("창의적인 아이디어맨", "논리적 분석을 좋아하고 새로운 개념 탐구를 즐기는 독립적인 타입입니다."),
        "ENTJ": ("카리스마 있는 리더", "목표 달성을 위해 체계적으로 행동하며 팀을 이끄는 주도적인 타입입니다."),
        "ENTP": ("재기 발랄한 토론자", "새로운 아이디어와 논쟁을 즐기며 유연하게 대처하는 활동적인 타입입니다."),
        "INFJ": ("따뜻한 카운슬러", "타인의 감정을 잘 이해하고 의미 있는 관계를 소중히 하는 공감 능력이 뛰어난 타입입니다."),
        "INFP": ("이상주의적 몽상가", "자신의 가치관과 신념을 중시하며 창의적으로 자신을 표현하는 감성적인 타입입니다."),
        "ENFJ": ("사려 깊은 외교관", "타인의 성장을 도우며 조화로운 관계를 만드는 따뜻하고 리더십 있는 타입입니다."),
        "ENFP": ("열정적인 활동가", "새로운 경험을 사랑하고 긍정적이며 창의적으로 주변을 밝히는 외향적인 타입입니다."),
        "ISTJ": ("책임감 있는 관리자", "체계적이고 신뢰할 수 있으며 책임을 다하는 실질적이고 신중한 타입입니다."),
        "ISFJ": ("헌신적인 수호자", "타인을 돌보는 것을 즐기며 안정감 있고 따뜻한 분위기를 만드는 성실한 타입입니다."),
        "ESTJ": ("강단 있는 지휘관", "효율성을 중시하고 명확한 목표를 향해 주도적으로 행동하는 실행력 있는 타입입니다."),
        "ESFJ": ("사교적인 주최자", "타인의 필요를 챙기고 팀을 하나로 모으는 따뜻하고 책임감 있는 타입입니다."),
        "ISTP": ("현실적인 장인", "실제 문제를 논리적으로 분석하고 실행하는 독립적이고 실용적인 타입입니다."),
        "ISFP": ("겸손한 예술가", "현재를 충실하게 살며 타인의 감정을 존중하는 따뜻하고 섬세한 타입입니다."),
        "ESTP": ("대담한 사업가", "순간을 즐기며 현실적으로 문제를 해결하는 활동적이고 모험심 있는 타입입니다."),
        "ESFP": ("명랑한 연예인", "사람들과 함께하는 것을 즐기고 즐거움을 나누며 현재에 집중하는 쾌활한 타입입니다."),
    }

    nickname, description = mbti_data.get(mbti_code, ("분석 불가", "분석할 수 없습니다."))

    # AI에 해설 요청
    explanation_prompt = f"{mbti_code} 타입: {nickname}의 특징을 2-3줄로 간단히 설명해주세요."
    try:
        explanation = ask_ai(explanation_prompt)
        # 첫 2-3문장만 추출
        explanation = ". ".join(explanation.split(".")[:2]) + "."
    except:
        explanation = f"당신은 {nickname}입니다."

    return f"MBTI: {mbti_code}\n별명: {nickname}\n설명: {description}\n해설: {explanation}"

def parse_mbti_response(response):
    try:
        lines = response.strip().split("\n")
        result = {}

        for line in lines:
            if line.startswith("MBTI:"):
                result["mbti"] = line.split(":")[-1].strip()
            elif line.startswith("별명:"):
                result["nickname"] = line.split(":")[-1].strip()
            elif line.startswith("설명:"):
                result["description"] = line.split(":")[-1].strip()
            elif line.startswith("해설:"):
                result["explanation"] = line.split(":")[-1].strip()

        return result
    except Exception as e:
        return {
            "mbti": "ERROR",
            "nickname": "오류 발생",
            "description": "응답 파싱 중 오류가 발생했습니다.",
            "explanation": str(e)
        }

def analyze_class_atmosphere(records):
    if not records:
        return "아직 참여한 친구가 없습니다."

    mbti_list = [r.get("mbti", "Unknown") for r in records]
    prompt = f"""우리 반 친구들의 MBTI 분포:
{', '.join(mbti_list)}

이 분포를 보고 우리 반의 대체적인 분위기와 특징을 분석해주세요. (3-5줄)"""

    return ask_ai(prompt)

st.title("🎯 우리반 MBTI수집소")

tab1, tab2 = st.tabs(["내 유형 찾기", "우리 반 분석"])

with tab1:
    st.subheader("📝 내 정보 입력")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름", placeholder="이름을 입력하세요")
    with col2:
        today = st.text_input("날짜", value=datetime.now().strftime("%Y-%m-%d"), disabled=True)

    st.subheader("❓ 다음 질문에 답해주세요")

    questions = [
        "1️⃣ 새로운 사람 만나는 것을 좋아하나요?",
        "2️⃣ 결정할 때 감정적인가요 논리적인가요?",
        "3️⃣ 계획을 세우고 따르는 편인가요?",
        "4️⃣ 혼자 있는 시간이 편한가요?"
    ]

    answers = []
    for i, question in enumerate(questions):
        answer = st.radio(
            question,
            ("네", "아니요"),
            key=f"q{i}"
        )
        answers.append(f"{question} → {answer}")

    if st.button("🚀 내 MBTI 찾기", width='stretch'):
        if not name:
            st.error("이름을 입력해주세요!")
        else:
            with st.spinner("AI가 분석 중입니다..."):
                try:
                    answers_text = "\n".join(answers)
                    ai_response = get_mbti_from_ai(answers_text)
                    mbti_data = parse_mbti_response(ai_response)

                    if "mbti" in mbti_data:
                        st.success("✅ 분석 완료!")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("당신의 MBTI", mbti_data.get("mbti", "Unknown"))
                        with col2:
                            st.metric("별명", mbti_data.get("nickname", "Unknown"))

                        st.info(f"**설명**: {mbti_data.get('description', '')}")
                        st.write(f"**해설**: {mbti_data.get('explanation', '')}")

                        if st.button("💾 결과 저장", width='stretch'):
                            records = load_records()
                            records.append({
                                "nick": name,
                                "mbti": mbti_data.get("mbti", "Unknown"),
                                "answers": answers,
                                "day": today
                            })
                            save_records(records)
                            st.success("저장되었습니다!")
                    else:
                        st.error("MBTI 분석에 실패했습니다. 다시 시도해주세요.")
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")

with tab2:
    records = load_records()

    st.subheader(f"👥 참여한 친구들 ({len(records)}명)")

    if records:
        st.dataframe(
            [{
                "이름": r["nick"],
                "MBTI": r["mbti"],
                "날짜": r["day"]
            } for r in records],
            width='stretch'
        )

        st.subheader("🌟 우리 반 분위기 분석")
        with st.spinner("분석 중..."):
            atmosphere = analyze_class_atmosphere(records)
            st.write(atmosphere)

        st.divider()
        st.subheader("🗑️ 기록 관리")
        if records:
            target = st.selectbox("지울 기록", [r["nick"] for r in records])
            if st.button("선택한 기록 삭제", width='stretch'):
                records = [r for r in records if r["nick"] != target]
                save_records(records)
                st.success("삭제되었습니다!")
                st.rerun()
    else:
        st.info("아직 참여한 친구가 없습니다. '내 유형 찾기' 탭에서 시작해보세요!")