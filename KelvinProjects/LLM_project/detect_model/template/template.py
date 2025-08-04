
from langchain.prompts import PromptTemplate
# prompt = """
# You are an AI agent tasked with predicting the disease in an image of a maize plant and providing treatment advice based on available tools.
# You have access to the following tools: {tools}

# Follow the reasoning steps carefully and respond using EXACT formatting:

# Question: {question}
# Image Input: {image_path}
# # Thought:[Your internal reasoning here, based on the image and question]
# Thought: {agent_scratchpad}
# Action:[disease_analysis_tool, get_treatment_advice_tool]
# # Action: [choose one of {tool_names}]
# Action Input: [Provide the necessary input for the chosen tool]
# Observation: [Result from the tool execution]
# Answer: [Your final answer to the user based on the observation]
# Use clear reasoning, and only invoke one tool per step. Do not skip any fields"""



# prompt_query="""
# generate relavant question from the user question """
# prompt = """
# You are an AI agent tasked with predicting the disease in an image of a maize plant and providing treatment advice based on available tools.
# you have the following tools{tools}
# Follow these reasoning steps carefully:
# 1.question:the inpurt question you must answer
# 2. **image_input** :Use the given image path to perform disease prediction.
# 3. **thought** : Reflect on the prediction outcome and what the user might need next
# 4.**action** : the action must be one of the [{tool_names}]
# 5. **action_input** : Specify the inputs required for each tool you invoke.

# 6.**observation**: Record the output from the tool.

# 7. **answer** : Return a complete answer to the user's question using the tools and reasoning above.

# Context:
# -**image_input**:{image_path}
# - **question**: {question}
# - **thought**: {agent_scratchpad}
# """

# prompt.input_variables
# prompt_template = PromptTemplate(
#     input_variables=["tool_names", "tools", "image_path", "question", "agent_scratchpad"],
#     template=prompt
# )

prompt = """
You are an AI agent tasked with predicting the disease in an image of a maize plant and providing treatment advice based on available tools.

Follow these reasoning steps carefully:

1. image_input: Use the given image path to perform disease prediction.  
2. Thought: Reflect on the prediction outcome and what the user might need next.
3. Action: Choose the action to be taken from the available tools {tool_names}.
4.Action Input: Specify the input required for the tool {tools} you invoke, the input image.
# 5. Question: Understand the user's question and connect it to the predicted disease.
# 6.. Action: Select the appropriate tool from {tools} to answer the user's question.
# 6. Action Input: Specify the input required for the tool you invoke.
5. Observation: Record the output from the tool[disease_analysis_tool, get_treatment_advice_tool].
6. Final Answer: Return a complete answer to the user's question using the tools and reasoning above.

Context:
- Image Input: {image_path}
- Question: {question}

{agent_scratchpad}
"""

prompt_template = PromptTemplate(
    input_variables=["tool_names", "tools", "image_path", "question", "agent_scratchpad"],
    template=prompt
)