# src/quiz_generator.py

from openai import OpenAI
from dotenv import load_dotenv
import os

class QuizGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OpenRouter API 키가 설정되지 않았습니다.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    def generate_quiz(self, context: str, num_questions=3) -> str:
        prompt = f"""
        다음 내용을 바탕으로 {num_questions}개의 퀴즈를 생성해줘.
        - 문제 유형: 객관식, OX, 빈칸 채우기 혼합
        - 각 문제는 번호로 구분하고, 정답도 함께 제공해줘

        내용:
        {context}
        """
        response = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 교육 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
