from openai import OpenAI

class CurriculumGenerator:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

    def generate_curriculum(self, context: str, max_sections=5) -> str:
        prompt = f"""
        다음 텍스트 내용을 분석하여 {max_sections}개의 학습 섹션(토픽)을 도출하고, 
        각 섹션마다 학습 목표를 간단히 정리해줘.

        [자료]
        {context[:3000]}  
        """
        response = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 교육 콘텐츠 기획자입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
