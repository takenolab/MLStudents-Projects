from langchain_openai import ChatOpenAI
import os


llm = ChatOpenAI(
    model="glm-4.5V",
    temperature=0,
    api_key="c42373cad52843178efda15cf7864d36.mIgXX6WI2xRHDNIA",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)
