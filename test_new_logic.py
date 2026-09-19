#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
from mbti_APP import get_mbti_from_ai, parse_mbti_response

print("=" * 60)
print("새로운 MBTI 계산 로직 테스트")
print("=" * 60)

# 테스트 데이터: 외향적이고, 감정 중심, 계획적, 혼자 시간이 불편한 ENFJ
test_answers = """1️⃣ 새로운 사람 만나는 것을 좋아하나요? → 네
2️⃣ 결정할 때 감정적인가요 논리적인가요? → 감정적
3️⃣ 계획을 세우고 따르는 편인가요? → 네
4️⃣ 혼자 있는 시간이 편한가요? → 아니요"""

print("\n입력 데이터:")
print(test_answers)

print("\n" + "=" * 60)
print("MBTI 계산 및 설명 생성 중...")
print("=" * 60)

try:
    response = get_mbti_from_ai(test_answers)
    print("\nAI 응답:")
    print(response)

    print("\n" + "=" * 60)
    print("파싱 결과")
    print("=" * 60)
    parsed = parse_mbti_response(response)
    print(f"MBTI: {parsed.get('mbti')}")
    print(f"별명: {parsed.get('nickname')}")
    print(f"설명: {parsed.get('description')}")
    print(f"해설: {parsed.get('explanation')}")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
