from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import time 
from llm.glm_llm import glm, client
import logging
import importlib
from pathlib import Path
from agents.create_agent import create_agent
from tools import com_info_tools, com_register_tools, sub_com_info_tools, law_tools
from zhipuai import ZhipuAI
from pprint import pprint
import json
import logging
import time


def call_glm(messages, model="glm-4",
             temperature=0.95,
             tools=None):
    response = client.chat.completions.create(
        model=model,  # 填写需要调用的模型名称
        messages=messages,
        temperature=temperature,
        top_p=0.9,
        tools=tools,
    )
    # print(messages)
    print(response.json())
    return response

def save_log(log_str, log_path):
    with open(log_path, 'a') as f:
        f.write(log_str)
        f.close()



def get_chain_metadata(prompt_fn: Path, retrieve_module: bool = False) -> dict:
    """
    Get the metadata of the chain
    :param prompt_fn: The path to the prompt file
    :param retrieve_module: If True, retrieve the module
    :return: A dict with the metadata
    """
    prompt_directory = str(prompt_fn.parent)
    prompt_name = str(prompt_fn.stem)
    print(prompt_directory)
    print(prompt_name) 
    try:
        spec = importlib.util.spec_from_file_location('output_schemes', prompt_directory + '/output_schemes.py')
        schema_parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(schema_parser)
    except ImportError as e:
        print(f"Error loading module {prompt_directory + '/output_schemes'}: {e}")
    if hasattr(schema_parser, '{}_parser'.format(prompt_name)):
        parser_func = getattr(schema_parser, '{}_parser'.format(prompt_name))
    else:
        parser_func = None
    result = {'parser_func': parser_func}
    if retrieve_module:
        result['module'] = schema_parser
        
    return result





def load_prompt(prompt_path: str, is_template: bool = True ) -> PromptTemplate:
    """
    Reads and returns the contents of a prompt file.
    :param prompt_path: The path to the prompt file
    """
    with open(prompt_path, 'r') as file:
        prompt = file.read().rstrip()
    if is_template:
        return PromptTemplate.from_template(prompt)
    else:
        return prompt



class ChainWrapper:
    """
    A wrapper for a LLM chain
    """

    def __init__(self, prompt_path: str, parser_func=None):
        
        """
        Initialize a new instance of the ChainWrapper class.
        :param llm_config: The config for the LLM
        :param prompt_path: A path to the prompt file (text file)
        :param parser_func: A function to parse the output of the LLM
        """
        self.llm = glm 
        self.parser_func = parser_func
        self.prompt = load_prompt(prompt_path)
        self.prompt_path =  prompt_path
        self.build_chain()

    def build_chain(self):
        #    print("normal chaim")
           self.chain = self.prompt | self.llm 
           
   
    def invoke(self, chain_input: dict) -> dict:
        """
        Invoke the chain on a single input
        :param chain_input: The input for the chain
        :return: A dict with the defined json schema
        """
        count = 0
        while 1:
           try:
                result = self.chain.invoke(chain_input)
                # print(result.content)
                if self.parser_func is not None:
                   result = self.parser_func(result)
                break 
           except Exception as e:
                if "</div>" not in str(e):
                   print("Here is a error\n" ,str(e))
                   count += 1
                   time.sleep(5)
                if count >= 5:
                   logging.error('Error in chain invoke: {}'.format(e.user_message))
                   result = None
                break 
        return result
    


    
class AgentWrapper:
    def __init__(self, prompt_path: str, tools: list, log_path = None,parser_func=None, ):
        
        """
        Initialize a new instance of the ChainWrapper class.
        :param llm_config: The config for the LLM
        :param prompt_path: A path to the prompt file (text file)
        :param parser_func: A function to parse the output of the LLM
        """
        self.llm = glm 
        self.parser_func = parser_func
        self.prompt = load_prompt(prompt_path, is_template=False)
        self.tools = tools 
        self.log_path = log_path
        self.build_agent()
        
        
    def build_agent(self ):
        self.agent =  create_agent(glm, self.tools, self.prompt)
    
    
    def invoke(self, query: str):
        messages =  self.agent.invoke({"messages": [("human", query)]})
        for item in messages['intermediate_steps']:
            # print(item[-1])
            if self.log_path:
                self.last_tool_answer = item[-1]
                save_log(str(item) + '\n', self.log_path)
                # print(item)
                save_log("------------------",self.log_path)
        # print(messages['intermediate_steps'])
        return  messages['output']
    
    
    
class MetaChain:
    """
    A wrapper for the meta-prompts chain
    """
    
    def __init__(self, log_path=None):
        """
        Initialize a new instance of the MetaChain class. Loading all the meta-prompts
        :param config: An EasyDict configuration
        """
        self.prompt_folder = Path("/public/zzy/competition/law_glm_zs/prompt")
        #不需要 init , step_samples
        # self.initial_chain = self.load_chain('initial')
        self.open_or_local_clf = self.load_chain('classification/open_or_local_clf')
        # self.step_samples = self.load_chain('step_samples')
        self.local_question_clf = self.load_chain('classification/local_question_clf')
        
        self.general_knowledge = self.load_chain("general_knowledge/general_knowledge_answer")
        self.log_path = log_path
        self.company_agent = self.load_agent("local_tools/company_info")
        self.sub_company_agent = self.load_agent("local_tools/sub_company_info")
        self.law_agent = self.load_agent("local_tools/law_info") 
        
        self.summary_chain = self.load_chain("summary/summary")
        self.is_omit_clf = self.load_chain('classification/is_omit_clf')
        
         
         
    def load_chain(self, chain_name: str) -> ChainWrapper:
        """
        Load a chain according to the chain name
        :param chain_name: The name of the chain
        """
        metadata = get_chain_metadata( self.prompt_folder / '{}.prompt'.format(chain_name))
        return ChainWrapper(self.prompt_folder  /  '{}.prompt'.format(chain_name),
                            metadata['parser_func'])
        
        
    def load_agent(self, agent_name):
        
        
        
        if "sub_company_info" in agent_name :
            return AgentWrapper(self.prompt_folder  /  '{}.prompt'.format(agent_name), sub_com_info_tools, log_path = self.log_path)
        
        elif "company_info" in agent_name:
            com_all_tools = []
            com_all_tools.extend(com_info_tools)
            com_all_tools.extend(com_register_tools)
            return AgentWrapper(self.prompt_folder  /  '{}.prompt'.format(agent_name), com_all_tools, log_path = self.log_path)
        elif "law_info" in agent_name:
            return AgentWrapper(self.prompt_folder  /  '{}.prompt'.format(agent_name), law_tools, log_path = self.log_path)
            
            




           
   
  
  

