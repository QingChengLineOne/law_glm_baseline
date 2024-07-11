import json 
import re 


def local_question_clf_parser(response: dict) -> dict:
    """
    Parse the response from the LLM chain
    :param response: The response from the LLM chain
    :return: The parsed response
    """
    # print(response['text'])
    # print(sql)
    type_str = response.content 
    # print(sql)
    if type_str.startswith("```json"):
        type_str = type_str.strip("`").strip("json").strip("\n").strip()
    type_str_pattern = re.compile(r'"type": "(.*?)"', re.DOTALL)
    match_type = type_str_pattern.search(type_str)
    
    # match_reason = reason_pattern.search(sql)
    if match_type:
        type_str = match_type.group(1)
        # 将转义的换行符 \\n 替换为实际的换行符 \n
        predictions = type_str.replace(r'\n', '\n')
    else:
        predictions = ""
        
    # print({'prediction': predictions, "reason": reason})
    return {'type': predictions}



def open_or_local_clf_parser(response: dict) -> dict:
    """
    Parse the response from the LLM chain
    :param response: The response from the LLM chain
    :return: The parsed response
    """
    # print(response['text'])
    # print(sql)
    type_str = response.content 
    # print(sql)
    if type_str.startswith("```json"):
        type_str = type_str.strip("`").strip("json").strip("\n").strip()
    type_str_pattern = re.compile(r'"type": "(.*?)"', re.DOTALL)
    match_type = type_str_pattern.search(type_str)
    
    # match_reason = reason_pattern.search(sql)
    if match_type:
        type_str = match_type.group(1)
        # 将转义的换行符 \\n 替换为实际的换行符 \n
        predictions = type_str.replace(r'\n', '\n')
    else:
        predictions = ""
        
    # print({'prediction': predictions, "reason": reason})
    return {'type': predictions}


def is_omit_clf_parser(response: dict) -> dict:
    """
    Parse the response from the LLM chain
    :param response: The response from the LLM chain
    :return: The parsed response
    """
    # print(response['text'])
    # print(sql)
    type_str = response.content 
    # print(sql)
    if type_str.startswith("```json"):
        type_str = type_str.strip("`").strip("json").strip("\n").strip()
    type_str_pattern = re.compile(r'"type": "(.*?)"', re.DOTALL)
    match_type = type_str_pattern.search(type_str)
    
    # match_reason = reason_pattern.search(sql)
    if match_type:
        type_str = match_type.group(1)
        # 将转义的换行符 \\n 替换为实际的换行符 \n
        predictions = type_str.replace(r'\n', '\n')
    else:
        predictions = ""
        
    # print({'prediction': predictions, "reason": reason})
    return {'type': predictions}

