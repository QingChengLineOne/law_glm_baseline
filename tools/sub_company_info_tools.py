from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from services.sub_company_info_service import *


class CompanyNameInput(BaseModel):
    company_name: str = Field(description="公司名称")

class CompanyInvestNameInput(BaseModel):
    company_name: str = Field(description="公司名称")
    money_threshold: str = Field(description="筛选母公司投资金额的下限，使用万和亿为单位，例如：100万，1亿。如果问题没有把投资金额作为筛选条件，则使用默认值",default="0万")
    rank_name: str = Field(description="根据母公司投资金额/母公司参股比例字段对返回的子公司投资信息列表进行排序。如果问题没有把母公司参股比例作为排序条件，则使用默认值",default="母公司投资金额")

class KeyValueInput(BaseModel):
    key: str = Field(description="键")
    value: str = Field(description="值")


parent_company_info_by_name_getter = StructuredTool.from_function(
    func=get_parent_company_info_by_name_service,
    name="parent_company_info_by_name_getter",
    args_schema=CompanyNameInput,
)

all_sub_company_name_by_name_getter = StructuredTool.from_function(
    func=get_all_sub_company_name_by_name_service,
    name="all_sub_company_name_by_name_getter",
    args_schema=CompanyNameInput,
)

all_sub_company_invest_info_getter = StructuredTool.from_function(
    func=get_all_sub_company_invest_info_service,
    name="all_sub_company_invest_info_getter",
    args_schema=CompanyInvestNameInput,
)

all_sub_company_counter = StructuredTool.from_function(
    func=count_sub_company_num_service,
    name="all_sub_company_counter",
    args_schema=CompanyNameInput,
)

total_amount_invested_in_subsidiaries_getter = StructuredTool.from_function(
    func=query_total_amount_invested_in_subsidiaries,
    name="total_amount_invested_in_subsidiaries_getter",
    args_schema=CompanyNameInput,
)

all_controled_sub_company_invest_info_getter = StructuredTool.from_function(
    func=get_all_controled_sub_company_invest_info_service,
    name="all_controled_sub_company_invest_info_getter",
    args_schema=CompanyInvestNameInput,
)

all_full_controled_sub_company_invest_info_getter = StructuredTool.from_function(
    func=get_all_full_controled_sub_company_invest_info_service,
    name="all_full_controled_sub_company_invest_info_getter",
    args_schema=CompanyInvestNameInput,
)

sub_com_info_tools = [
    parent_company_info_by_name_getter,
    all_sub_company_invest_info_getter,
    # all_sub_company_name_by_name_getter,
    all_controled_sub_company_invest_info_getter,
    all_full_controled_sub_company_invest_info_getter,
    total_amount_invested_in_subsidiaries_getter
]
