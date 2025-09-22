from langchain_openai import ChatOpenAI
model1=ChatOpenAI(
    # model="GLM-4.5-Flash",
    model="GLM-4.5v",
    temperature=0.7,
    # api_key="39d21d2a55504df58423d1e4f218ec94.OTy73GoacNLqHGuS",
    # api_key=("e0c7cd5ec96c44b8a88873efda1b61ac.fyJdvSoyTAHFNLkM"),
    # api_key="5dd8688cd8b04521ad49546bf0ef37fb.WxHGfeb5a9Iy1mv8",

    # api_key="813e76b1869d4a5f96c57e1ecf420c3a.dmVjLtDCdGZYEf3M",
    api_key="d18e2322042f4cb7a3f18c317f55edb9.NIC2QusqsMb8D69v",
    max_completion_tokens=15000000,
    base_url="https://open.bigmodel.cn/api/paas/v4"
)