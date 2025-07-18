
from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key= "c522b9ed146a4e51ba9d9fa330a1dd87.qJoXCk6aPhqUdQaS",
    base_url= "https://open.bigmodel.cn/api/paas/v4",
    )

def get_llm(prompt, history=None):
    """
    This function takes a user prompt and conversation history,
    sends them to the GPT model, and returns the response.
    """
    if history is None:
        history = []

    # Add the current user input to history
    history.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": "You are a helpful but terse AI assistant who gets straight to the point."}
        ] + history,
        temperature=0.0,
    )

    response = completion.choices[0].message.content


    history.append({"role":"assistant", "content": response})

    return response,history