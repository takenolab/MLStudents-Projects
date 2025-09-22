from langchain_core.prompts import PromptTemplate
import pathlib
c=pathlib.Path(__file__).resolve().parents[1]
import sys 
sys.path.append(str(c))
from utilities.llm.llm import llm_model
from template.fallback_template import fallback_template 
from template.model_temp import model_temp 
from template.single_client_template import single_email_template
from template.multi_client_template import multi_recipient_template 
from template.search_mail_template import search_new_messages_template 



email_clients_bulk_chain = PromptTemplate.from_template(template=multi_recipient_template) | llm_model
email_client_single_chain = PromptTemplate.from_template(template=single_email_template) | llm_model
search_client_messages_chain = PromptTemplate.from_template(template=search_new_messages_template) | llm_model
company_chat_fallback_chain = PromptTemplate.from_template(template=fallback_template) | llm_model


SYSTEM_TEMP = PromptTemplate(
    template=model_temp,
    input_variables=["user","history"],
    validate_template=True
) | llm_model



model_chains = {
    "email_clients_bulk": email_clients_bulk_chain,
    "email_client_single": email_client_single_chain,
    "search_client_messages": search_client_messages_chain,
    "company_chat_fallback": company_chat_fallback_chain
}
