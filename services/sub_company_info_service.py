import json

from apis import (
    get_listed_company_info,
    search_company_name_by_super_info,
    search_company_name_by_info
)
from utils import convert_to_float, convert_to_str,compare_rank_name



def _get_full_name(company_name: str) -> str:
    """根据公司名称、公司简称或英文名称，获取该公司的全称。"""
    company_info_json = search_company_name_by_info(key="公司简称", value=company_name)
    if "公司名称" in company_info_json:
        company_name = company_info_json["公司名称"]
        return company_name
    company_info_json = search_company_name_by_info(key="英文名称", value=company_name)
    if "公司名称" in company_info_json:
        company_name = company_info_json["公司名称"]
        return company_name
    return company_name


def get_parent_company_info_by_name_service(company_name: str) -> str:
    """
    根据子公司的公司名称，查询该公司的母公司信息，或者说查询该公司是哪家公司旗下的子公司。
    母公司信息包括'母公司名称'、'母公司参股比例'、'母公司投资金额'。
    """
    company_name = _get_full_name(company_name)
    rsp = get_listed_company_info(company_name)
    ret = {
        "公司名称": company_name
    }
    if "关联上市公司全称" in rsp:
        ret["母公司名称"] = rsp["关联上市公司全称"]
    if "上市公司参股比例" in rsp:
        ret["母公司参股比例"] = rsp["上市公司参股比例"]
    if "上市公司投资金额" in rsp:
        ret["母公司投资金额"] = rsp["上市公司投资金额"]
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str



def get_all_sub_company_name_by_name_service(company_name: str) -> str:
    """
    根据母公司的公司名称，获得该公司旗下的所有子公司的名称。
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    for item in rsp:
        sub_company_name = item["公司名称"]
        del item["公司名称"]
        item["子公司名称"] = sub_company_name
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def get_all_sub_company_invest_info_service(company_name: str,money_threshold: str = "0万",rank_name: str = "母公司投资金额") -> str:
    """
    根据母公司的公司名称，获得该公司的所有子公司的参股和投资信息，以及子公司的总数量。
    包括'公司名称'、"母公司名称"、"母公司参股比例"、"母公司投资金额"
    输出按照如下要求：
    1、母公司投资金额大于输入参数money_threshold。
    2、按照母公司投资金额/母公司参股比例从小到大排序。
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    sub_company_name_list = [item["公司名称"] for item in rsp]
    listed_company_info_list = []
    
    new_list = []
    for item in sub_company_name_list:
        listed_company_info_list.append(get_listed_company_info(item))
    for listed_company_info in listed_company_info_list:
        item = {"公司名称":listed_company_info['公司名称'] }
        if "关联上市公司全称" in listed_company_info:
            item["母公司名称"] = listed_company_info["关联上市公司全称"]
        if "上市公司参股比例" in listed_company_info:
            item["母公司参股比例"] = listed_company_info["上市公司参股比例"]
        if "上市公司投资金额" in listed_company_info:
            item["母公司投资金额"] = listed_company_info["上市公司投资金额"]
        if  (item["母公司投资金额"] is not None) and convert_to_float(item["母公司投资金额"]) > convert_to_float(money_threshold):
            new_list.append(item)
    if rank_name == "母公司投资金额":
        new_list = sorted(new_list, key=lambda x: convert_to_float(x["母公司投资金额"]), reverse=False)
    else:
        new_list = sorted(new_list, key=lambda x: float(x["母公司参股比例"]), reverse=False)
    json_str = json.dumps(new_list, ensure_ascii=False)
    json_str += f"\n子公司总数量：{len(new_list)}"
    return json_str


def count_sub_company_num_service(company_name: str) -> str:
    """
    根据母公司的公司名称，统计该公司所有子公司的数量。
    """
    company_name = _get_full_name(company_name)
    all_sub_company_name = search_company_name_by_super_info("关联上市公司全称", company_name)
    ret = {
        "公司名称": company_name,
        f"{company_name}所有子公司的数量": len(all_sub_company_name)
    }
    json_str = json.dumps(ret, ensure_ascii=False)
    return json_str


def query_total_amount_invested_in_subsidiaries(company_name: str) -> str:
    """根据母公司的公司名称、公司简称或英文名称，查询该公司在子公司投资的总金额。"""
    full_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", full_name)
    total_amount = 0
    for item in rsp:
        sub_company_name = item["公司名称"]
        listed_company_info = get_listed_company_info(sub_company_name)
        if "上市公司投资金额" not in listed_company_info:
            continue
        amount = listed_company_info["上市公司投资金额"]
        if amount is None:
            continue
        total_amount += convert_to_float(amount)
    rsp = {
        "公司名称": company_name,
        "在子公司投资的总金额": convert_to_str(total_amount)
    }
    json_str = json.dumps(rsp, ensure_ascii=False)
    return json_str


def get_all_controled_sub_company_invest_info_service(company_name: str,money_threshold: str = "0万",rank_name: str = "母公司投资金额") -> str:
    """
    根据母公司的公司名称，获得该公司的所有控股子公司的参股和投资信息，以及控股子公司的总数量。
    包括'公司名称'、"母公司名称"、"母公司参股比例"、"母公司投资金额"
    输出按照如下要求：
    1、母公司投资金额大于输入参数money_threshold。
    2、按照母公司投资金额/母公司参股比例从小到大排序。
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    sub_company_name_list = [item["公司名称"] for item in rsp]
    listed_company_info_list = []
    
    new_list = []
    for item in sub_company_name_list:
        listed_company_info_list.append(get_listed_company_info(item))
    for listed_company_info in listed_company_info_list:
        item = {"公司名称":listed_company_info['公司名称'] }
        if "关联上市公司全称" in listed_company_info:
            item["母公司名称"] = listed_company_info["关联上市公司全称"]
        if "上市公司参股比例" in listed_company_info:
            item["母公司参股比例"] = listed_company_info["上市公司参股比例"]
        if "上市公司投资金额" in listed_company_info:
            item["母公司投资金额"] = listed_company_info["上市公司投资金额"]
        if (item["母公司投资金额"] is not None) and (item["母公司参股比例"] is not None) and convert_to_float(item["母公司投资金额"]) > convert_to_float(money_threshold) and float(item["母公司参股比例"]) > 50 :
            new_list.append(item)
    if rank_name == "母公司投资金额":
        new_list = sorted(new_list, key=lambda x: convert_to_float(x["母公司投资金额"]), reverse=False)
    else:
        new_list = sorted(new_list, key=lambda x: float(x["母公司参股比例"]), reverse=False)
    json_str = json.dumps(new_list, ensure_ascii=False)
    json_str += f"\n控股子公司总数量：{len(new_list)}"
    return json_str

def get_all_full_controled_sub_company_invest_info_service(company_name: str,money_threshold: str = "0万",rank_name: str = "母公司投资金额") -> str:
    """
    根据母公司的公司名称，获得该公司的所有全资子公司的参股和投资信息，以及全资子公司的总数量。
    包括'公司名称'、"母公司名称"、"母公司参股比例"、"母公司投资金额"
    输出按照如下要求：
    1、母公司投资金额大于输入参数money_threshold。
    2、按照母公司投资金额/母公司参股比例从小到大排序。
    """
    company_name = _get_full_name(company_name)
    rsp = search_company_name_by_super_info("关联上市公司全称", company_name)
    sub_company_name_list = [item["公司名称"] for item in rsp]
    listed_company_info_list = []
    
    new_list = []
    for item in sub_company_name_list:
        listed_company_info_list.append(get_listed_company_info(item))
    for listed_company_info in listed_company_info_list:
        item = {"公司名称":listed_company_info['公司名称'] }
        if "关联上市公司全称" in listed_company_info:
            item["母公司名称"] = listed_company_info["关联上市公司全称"]
        if "上市公司参股比例" in listed_company_info:
            item["母公司参股比例"] = listed_company_info["上市公司参股比例"]
        if "上市公司投资金额" in listed_company_info:
            item["母公司投资金额"] = listed_company_info["上市公司投资金额"]
        if (item["母公司投资金额"] is not None) and (item["母公司参股比例"] is not None) and convert_to_float(item["母公司投资金额"]) > convert_to_float(money_threshold) and float(item["母公司参股比例"]) == 100 :
            new_list.append(item)
    if rank_name == "母公司投资金额":
        new_list = sorted(new_list, key=lambda x: convert_to_float(x["母公司投资金额"]), reverse=False)
    else:
        new_list = sorted(new_list, key=lambda x: float(x["母公司参股比例"]), reverse=False)
    json_str = json.dumps(new_list, ensure_ascii=False)
    json_str += f"\n全资子公司总数量：{len(new_list)}"
    return json_str
