#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

# Test 1: JSON 저장/로드 테스트
print("=" * 50)
print("Test 1: JSON 저장/로드 테스트")
print("=" * 50)

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

# 기존 파일이 있으면 백업
if os.path.exists("mbti.json"):
    os.rename("mbti.json", "mbti.json.bak")

# 새 데이터 저장
test_records = [
    {
        "nick": "테스트1",
        "mbti": "INTJ",
        "answers": ["1️⃣ 새로운 사람 만나는 것을 좋아하나요? → 아니요", "2️⃣ 결정할 때 감정적인가요 논리적인가요? → 논리적"],
        "day": "2026-09-19"
    },
    {
        "nick": "테스트2",
        "mbti": "ENFP",
        "answers": ["1️⃣ 새로운 사람 만나는 것을 좋아하나요? → 네", "2️⃣ 결정할 때 감정적인가요 논리적인가요? → 감정적"],
        "day": "2026-09-19"
    }
]

save_records(test_records)
print(f"✅ {len(test_records)}개의 레코드 저장 완료")

# 저장된 데이터 로드
loaded = load_records()
print(f"✅ {len(loaded)}개의 레코드 로드 완료")
print(f"  - 첫 번째: {loaded[0]['nick']} ({loaded[0]['mbti']})")
print(f"  - 두 번째: {loaded[1]['nick']} ({loaded[1]['mbti']})")

# Test 2: MBTI 파싱 테스트
print("\n" + "=" * 50)
print("Test 2: MBTI 파싱 테스트")
print("=" * 50)

def parse_mbti_response(response):
    try:
        lines = response.strip().split("\n")
        result = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "MBTI:" in line:
                mbti = line.split("MBTI:")[-1].strip().split()[0]
                if len(mbti) == 4 and mbti.isupper():
                    result["mbti"] = mbti
            elif "별명:" in line:
                result["nickname"] = line.split("별명:")[-1].strip()
            elif "설명:" in line:
                result["description"] = line.split("설명:")[-1].strip()
            elif "해설:" in line:
                result["explanation"] = line.split("해설:")[-1].strip()

        if not result.get("mbti"):
            result["mbti"] = "UNKNOWN"
        if not result.get("nickname"):
            result["nickname"] = "선택지 없음"
        if not result.get("description"):
            result["description"] = "설명을 생성할 수 없었습니다."
        if not result.get("explanation"):
            result["explanation"] = "해설을 생성할 수 없었습니다."

        return result
    except Exception as e:
        return {
            "mbti": "ERROR",
            "nickname": f"오류 발생",
            "description": "AI 응답 파싱 중 오류가 발생했습니다.",
            "explanation": str(e)
        }

# 테스트 데이터
test_response = """MBTI: INTJ
별명: 통찰력의 리더
설명: 혼자만의 시간을 소중히 여기고 논리적으로 생각하는 타입입니다.
해설: 당신은 독립적이고 자신의 원칙을 중시하며, 깊이 있는 통찰력으로 문제를 해결합니다."""

result = parse_mbti_response(test_response)
print(f"✅ MBTI 파싱 완료:")
print(f"  - MBTI: {result['mbti']}")
print(f"  - 별명: {result['nickname']}")
print(f"  - 설명: {result['description']}")
print(f"  - 해설: {result['explanation'][:30]}...")

# Test 3: AI 호출 테스트 (실제 API)
print("\n" + "=" * 50)
print("Test 3: AI API 호출 테스트")
print("=" * 50)

try:
    from ai_helper import ask_ai

    test_prompt = """다음 4가지 질문에 대한 답변을 바탕으로 사람의 MBTI 유형을 판단해주세요.

답변:
1️⃣ 새로운 사람 만나는 것을 좋아하나요? → 아니요
2️⃣ 결정할 때 감정적인가요 논리적인가요? → 논리적
3️⃣ 계획을 세우고 따르는 편인가요? → 네
4️⃣ 혼자 있는 시간이 편한가요? → 네

정확하게 다음 형식으로 응답해주세요:
MBTI: INTJ
별명: 통찰력의 리더
설명: 혼자만의 시간을 소중히 여기고 논리적으로 생각하는 타입입니다.
해설: 당신은 독립적이고 자신의 원칙을 중시하며, 깊이 있는 통찰력으로 문제를 해결합니다."""

    print("⏳ AI API 호출 중...")
    response = ask_ai(test_prompt)

    print("✅ AI 응답 수신 완료")
    print(f"  응답 길이: {len(response)}자")
    print(f"  첫 50자: {response[:50]}...")

    # 파싱
    parsed = parse_mbti_response(response)
    print(f"  파싱된 MBTI: {parsed['mbti']}")

except Exception as e:
    print(f"❌ AI API 호출 실패: {str(e)}")

print("\n" + "=" * 50)
print("모든 테스트 완료!")
print("=" * 50)

# 백업 파일이 있으면 복원
if os.path.exists("mbti.json.bak"):
    os.remove("mbti.json")
    os.rename("mbti.json.bak", "mbti.json")
    print("원본 파일 복원 완료")
