from  langchain_openai import OpenAIEmbeddings
import os

embedding=OpenAIEmbeddings(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url='https://open.bigmodel.cn/api/paas/v4',
    model='embedding-3'
   
)