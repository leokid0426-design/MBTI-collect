#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ai_helper import ask_ai
from mbti_APP import parse_mbti_response

prompt = """MBTI 유형을 판단해주고, 다음 형식으로 정확히 응답해주세요:
MBTI: ISTJ
별명: 논리적 실행자
설명: 책임감 있는 타입
해설: 당신은 신뢰할 수 있습니다."""

print("=" * 60)
print("AI 응답 (Raw)")
print("=" * 60)
response = ask_ai(prompt)
print(repr(response))

print("\n" + "=" * 60)
print("AI 응답 (Formatted)")
print("=" * 60)
print(response)

print("\n" + "=" * 60)
print("파싱 결과")
print("=" * 60)
parsed = parse_mbti_response(response)
for key, value in parsed.items():
    print(f"{key}: {value}")
