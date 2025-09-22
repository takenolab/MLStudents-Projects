from langchain_openai import ChatOpenAI
model1=ChatOpenAI(
    # model="GLM-4.5-Flash",
    model="GLM-4.5v",
    temperature=0.7,
    max_completion_tokens=15000000,
    base_url="https://open.bigmodel.cn/api/paas/v4"
)