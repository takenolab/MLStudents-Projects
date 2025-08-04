from langchain_openai import ChatOpenAI
import os

model1=ChatOpenAI(
    model='glm-4',
    api_key=os.getenv('ZHIPUAI_API_KEY'),
    base_url='https://open.bigmodel.cn/api/paas/v4',
    max_completion_tokens=200
)