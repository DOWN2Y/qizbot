from openai import OpenAI
from dotenv import load_dotenv
import os
from src.embedder import Embedder
from src.vector_store import VectorStore

class QABot:
    def __init__(self, vector_store: VectorStore):
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OpenRouter API 키가 설정되지 않았습니다.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.embedder = Embedder()
        self.vector_store = vector_store

    def ask(self, question: str, top_k=3) -> str:
        query_vec = self.embedder.get_embeddings([question])[0]
        retrieved_docs = self.vector_store.search(query_vec, top_k=top_k)
        context = "\n".join(retrieved_docs)

        prompt = f"""
        다음 내용을 바탕으로 사용자의 질문에 답해줘.

        [자료]
        {context}

        [질문]
        {question}
        """

        response = self.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 친절한 교육 도우미입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
