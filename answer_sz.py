from llm.router_chain import MetaChain 
import jsonlines
from tqdm import tqdm
from utils import read_jsonl
import json 
log_path = 'log06_28_02.log'
test_chain = MetaChain(log_path)

def postprocess_answer(answer, last_tool_answer):
    if "：" in answer:
        pre_ans = answer.split("：")[0] 
    else:
        pre_ans = answer.split(":")[0] 
        
    post_ans_raw = last_tool_answer.split("\n")[0]
    data_list = json.loads(post_ans_raw)
    # 转换为另一种格式
    formatted_data = []
    for index, item in enumerate(data_list, start=1):
        company_name = item["公司名称"]
        share_ratio = item["母公司参股比例"]
        if share_ratio is None:
            share_ratio_text = "None"
        else:
            share_ratio_text = f"{share_ratio}%"
        formatted_data.append(f"{index}. {company_name}，母公司参股比例{share_ratio_text}")
    post_ans = "\n".join(formatted_data)
    return pre_ans + "：\n" + post_ans


def save_log(log):
    with open(log_path, 'a', encoding='utf-8') as f:
        # print(log)
        f.write(log)
        f.close()        

def answer(query: str):
    save_log("####### 问题： " + query  +"#######\n" )
    
    # 分别是通识问题还是本地数据库问题
    question_dict = {"question": query}
    clf1_type =  test_chain.open_or_local_clf.invoke(question_dict)['type']
    
    if clf1_type == "open":
        save_log("#######" + "该问题属于通识问题" +"#######\n" )
        final_answer = test_chain.general_knowledge.invoke(question_dict)
        save_log("####### 最终结果" + final_answer.content +"#######\n" )
        return final_answer.content 
    else :
        # 初始化 raw_answer 以防万一
        raw_answer = ""
        # 区分问题类型属于那种Local Question   
        clf2_type = test_chain.local_question_clf.invoke(question_dict)['type']
        if clf2_type == 'a':
            save_log("#######" + "该问题属于公司查询问题" +"#######\n" )
            raw_answer = test_chain.company_agent.invoke(query)
            # last_tool_anseer = test_chain.company_agent.last_tool_answer 
        elif clf2_type == 'b':
            save_log("#######" + "该问题属于法律案件查询问题" +"#######\n" )
            raw_answer = test_chain.law_agent.invoke(query)
            # last_tool_anseer = test_chain.law_agent.last_tool_answer 
            
        elif clf2_type == 'c':
            save_log("#######" + "该问题属于子公司查询问题" +"#######\n" )
            raw_answer = test_chain.sub_company_agent.invoke(query)
            # last_tool_answer = test_chain.sub_company_agent.last_tool_answer

            
            # qa_dict = {"question": query, "answer": raw_answer}
            # clf3_type = test_chain.is_omit_clf.invoke(qa_dict)['type']
            
            # save_log("-------" + clf3_type + "----------------")
            # if clf3_type == 'Yes':
            #     save_log("####### Raw answer " + raw_answer  +"#######\n" )
            #     try:
            #         raw_answer = postprocess_answer(raw_answer, last_tool_answer)
            #     except:
            #         raw_answer = raw_answer
        save_log("####### Raw answer " + raw_answer  +"#######\n" )      
        return raw_answer
            
        
        
        # save_log("#######" + "总结" +"#######\n" )
        # answer_dict = {"question":query, "answer": raw_answer}
            
        # 做总结简化答案
        # final_answer = test_chain.summary_chain.invoke(answer_dict)
        # save_log("####### 最终结果" + final_answer.content +"#######\n" )
        
        save_log("#######" + "问题结束" +"#######\n" )
    # return final_answer.content
    


if __name__ == '__main__':
    question_file = "./data/questions/question.jsonl"
    # 修改输出文件
    result_file = "./data/results/result_0628_02.json"
    queries = read_jsonl(question_file)

    # 生成答案
    save_log("Start generating answers...")

    for query in tqdm(queries):
        # 如果中断，可以从这里开始
        if query["id"] < 11:
            continue
        response = answer(query["question"])
        content = {
            "id": query["id"],
            "question": query["question"],  
            "answer": response
        }
        with jsonlines.open(result_file, "a") as json_file:
            json_file.write(content)