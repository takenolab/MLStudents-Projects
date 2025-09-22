from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    memory=memory
)





# import streamlit as st
# import openai

# openai.api_key = st.secrets["OPENAI_API_KEY"]  # or use os.environ

# # Initialize message history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# # Display chat history
# for msg in st.session_state.messages[1:]:  # skip system message
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User input
# user_input = st.chat_input("Ask me anything...")

# if user_input:
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Call OpenAI API with full conversation
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=st.session_state.messages,
#         temperature=0.7
#     )

#     # Extract assistant response
#     assistant_reply = response.choices[0].message.content

#     # Add and display assistant message
#     st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
#     with st.chat_message("assistant"):
#         st.markdown(assistant_reply)
