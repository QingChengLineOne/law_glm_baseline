from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from services.law_service import *


class CaseNumInput(BaseModel):
    case_num: str = Field(description="案号")


class CauseOfActionInput(BaseModel):
    cause_of_action: str = Field(description="案由")


class PlaintiffInput(BaseModel):
    plaintiff: str = Field(description="原告")


class DefendantInput(BaseModel):
    defendant: str = Field(description="被告")
    
class CompanyInput(BaseModel):
    company: str = Field(description="公司")


class KeyValueInput(BaseModel):
    key: str = Field(description="键")
    value: str = Field(description="值")


amount_involved_getter = StructuredTool.from_function(
    func=get_amount_involved_by_case_num_service,
    name="amount_involved_getter",
    args_schema=CaseNumInput,
)

legal_document_getter = StructuredTool.from_function(
    func=get_legal_document_service,
    name="legal_document_getter",
    description="""
    根据案号获得该案所有基本信息，包括'判决结果','原告','原告律师','审理法条依据',
    '文书类型','文件名','标题','案由','涉案金额','胜诉方','被告','被告律师'。
    """,
    args_schema=CaseNumInput,
)

case_number_counter_by_cause = StructuredTool.from_function(
    func=count_case_number_by_cause_service,
    name="case_number_counter_by_cause",
    args_schema=CauseOfActionInput,
)

case_num_retriever_by_legal_document = StructuredTool.from_function(
    func=search_case_num_by_legal_document_service,
    name="case_num_retriever_by_legal_document",
    args_schema=KeyValueInput,
)

plaintiff_lawyer_counter = StructuredTool.from_function(
    func=count_plaintiff_lawyer_service,
    name="plaintiff_lawyer_counter",
    args_schema=PlaintiffInput,
)


plaintiff_lawyer_company_counter = StructuredTool.from_function(
    func=count_plaintiff_lawyer_company_service,
    name="plaintiff_lawyer_company_counter",
    args_schema=PlaintiffInput,
)

# plaintiff_lawyer_company_counter = StructuredTool.from_function(
#     func=count_plaintiff_lawyer_company_service,
#     name="plaintiff_lawyer_company_counter",
#     args_schema=PlaintiffInput,
# )

defendant_lawyer_counter = StructuredTool.from_function(
    func=count_defendant_lawyer_service,
    name="defendant_lawyer_counter",
    args_schema=DefendantInput,
)


defendant_lawyer_company_counter = StructuredTool.from_function(
    func=count_defendant_lawyer_company_service,
    name="defendant_lawyer_company_counter",
    args_schema=DefendantInput,
)


lawyer_company_counter = StructuredTool.from_function(
    func=count_lawyer_company_service,
    name="lawyer_company_counter",
    args_schema=CompanyInput,
)


law_tools = [
    amount_involved_getter,
    legal_document_getter,
    case_number_counter_by_cause,
    case_num_retriever_by_legal_document,
    # plaintiff_lawyer_counter,
    # defendant_lawyer_counter,
    plaintiff_lawyer_company_counter,
    defendant_lawyer_company_counter,
    # lawyer_company_counter
]
