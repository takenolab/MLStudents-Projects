from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool 
from langchain_core.tools import StructuredTool
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent)) 
from router.router import SYSTEM_TEMP,model_chains
from data.employee import  staff
from template.options_template import agent_prompt
from data.KNOWLEDGE import db 
from utilities.llm.llm import llm_model
from memory.memory import load_conversation,save_conversation
from tools.multi_client_email import multi_send_email,MultiSendEmailShema 
from tools.single_client_email import send_single_email , SendSingleEmail
from tools.unseen_email import unseen_conversation , UseenConversationSchema



unseen_msg_tool = StructuredTool(
    name="Useen conversation",
    func=unseen_conversation,
    args_schema=UseenConversationSchema,
    handle_tool_error=True,
    verbose=True,
    handle_validation_error=True
) 

send_msg_tool = StructuredTool(
    name="Send single email",
    func=send_single_email,
    args_schema=SendSingleEmail,
    handle_tool_error=True,
    verbose=True,
    handle_validation_error=True
)

bulk_send_tool = StructuredTool(
    func=multi_send_email,
    name="Bulk email sender",
    args_schema=MultiSendEmailShema,
    handle_tool_error=True,
    verbose=True,
    handle_validation_error=True
) 

TOOLS = [
    bulk_send_tool,
    send_msg_tool,
    unseen_msg_tool
]


import ast

def is_dict_string(s) -> bool:
    try:
        result = ast.literal_eval(s)
        return isinstance(result, dict)
    except (ValueError, SyntaxError):
        return False

def ai(user_text: str) -> tuple[bool,str]:
  
    conversation_history = load_conversation()

 
    agent = initialize_agent(
        llm=llm_model,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=TOOLS,
        verbose =True,
        
        agent_kwargs={
            "prefix": agent_prompt,
         
       }

    )

    try:        
        main_route = SYSTEM_TEMP.invoke({"user": user_text ,  "history": conversation_history})
        chains = model_chains.get(main_route.content)
     
        
        if chains:            
            output = chains.invoke({
                "user": user_text,
                "staff": staff(),
                "db": db(),
                "history": conversation_history
            })    
               
            if is_dict_string(s=output.content):           
                response = agent.invoke({"input": output.content})
                print(is_dict_string(s=output.content))    
                save_conversation("user", user_text)
                save_conversation("ai", response["output"])
                return True, str(response["output"])
            
            elif not is_dict_string(s=output.content):
              save_conversation("user", user_text)
              save_conversation("ai", output.content)
              return True, str(output.content)
          
    except Exception as err:
        print(err)
        return False,"error occured"


# if __name__ == "__main__":
#     while True:
#        x=ai(user_text=input("\nENTER SOMETHING.."))
#        print(x)