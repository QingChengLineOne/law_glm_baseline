from typing import List, Union
import requests

DOMAIN = "comm.chatglm.cn"
TEAM_TOKEN = ""

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {TEAM_TOKEN}'
}


def get_company_info(query_conds: dict,need_fields: List[str] = []) -> dict:
    """
    根据上市公司名称、简称或代码查找上市公司信息。
    
    参数:
    query_conds -- 查询条件字典，例如{"公司名称": "上海妙可蓝多食品科技股份有限公司"}
    need_fields -- 需要返回的字段列表，例如["公司名称", "公司代码", "主营业务"],need_fields传入空列表，则表示返回所有字段，否则返回填入的字段
    
    例如：
        输入：
        {"公司名称": "上海妙可蓝多食品科技股份有限公司"}
        输出：
        {'公司名称': '上海妙可蓝多食品科技股份有限公司',
         '公司简称': '妙可蓝多',
         '英文名称': 'Shanghai Milkground Food Tech Co., Ltd.',
         '关联证券': '',
         '公司代码': '600882',
         '曾用简称': '大成股份>> *ST大成>> 华联矿业>> 广泽股份',
         '所属市场': '上交所',
         '所属行业': '食品制造业',
         '成立日期': '1988-11-29',
         '上市日期': '1995-12-06',
         '法人代表': '柴琇',
         '总经理': '柴琇',
         '董秘': '谢毅',
         '邮政编码': '200136',
         '注册地址': '上海市奉贤区工业路899号8幢',
         '办公地址': '上海市浦东新区金桥路1398号金台大厦10楼',
         '联系电话': '021-50188700',
         '传真': '021-50188918',
         '官方网址': 'www.milkground.cn',
         '电子邮箱': 'ir@milkland.com.cn',
         '入选指数': '国证Ａ指,巨潮小盘',
         '主营业务': '以奶酪、液态奶为核心的特色乳制品的研发、生产和销售，同时公司也从事以奶粉、黄油为主的乳制品贸易业务。',
         '经营范围': '许可项目：食品经营；食品互联网销售；互联网直播服务（不含新闻信息服务、网络表演、网络视听节目）；互联网信息服务；进出口代理。（依法须经批准的项目，经相关部门批准后方可开展经营活动，具体经营项目以相关部门批准文件或许可证件为准）。一般项目：乳制品生产技术领域内的技术开发、技术咨询、技术服务、技术转让；互联网销售（除销售需要许可的商品）；互联网数据服务；信息系统集成服务；软件开发；玩具销售。（除依法须经批准的项目外，凭营业执照依法自主开展经营活动）',
         '机构简介': '公司是1988年11月10日经山东省体改委鲁体改生字(1988)第56号文批准，由山东农药厂发起，采取社会募集方式组建的以公有股份为主体的股份制企业。1988年12月15日,经中国人民银行淄博市分行以淄银字(1988)230号文批准，公开发行股票。 1988年12月经淄博市工商行政管理局批准正式成立山东农药工业股份有限公司(营业执照:16410234)。',
         '每股面值': '1.0',
         '首发价格': '1.0',
         '首发募资净额': '4950.0',
         '首发主承销商': ''}
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_company_info"

    data = {
        "query_conds":query_conds,
        "need_fields": need_fields
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def search_company_name_by_info(key: str, value: str) -> dict:
    """
    根据公司基本信息某个字段是某个值来查询具体的公司名称。
    可以输入的字段有['上市日期','主营业务','传真','入选指数',
    '公司代码','公司简称','关联证券','办公地址','官方网址',
    '总经理','所属市场','所属行业','曾用简称','机构简介',
    '每股面值','法人代表','注册地址','电子邮箱','经营范围',
    '联系电话','英文名称','董秘','邮政编码','首发主承销商',
    '首发价格','首发募资净额',]

    例如：
        输入：
        {"key": "所属行业",
         "value": "批发业"}
        输出：
        [{'公司名称': '国药集团药业股份有限公司'},
         {'公司名称': '苏美达股份有限公司'},
         {'公司名称': '深圳市英唐智能控制股份有限公司'}]
    """
    url = f"https://{DOMAIN}/law_api/search_company_name_by_info"

    data = {
        "key": key,
        "value": value
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def get_company_register(query_conds: dict,need_fields: List[str] = []) -> dict:
    """
    根据公司名称，查询工商信息。

    参数:
    query_conds -- 查询条件字典，例如{"公司名称": "上海妙可蓝多食品科技股份有限公司"}
    need_fields -- 需要返回的字段列表，例如["公司名称", "公司代码", "主营业务"],need_fields传入空列表，则表示返回所有字段，否则返回填入的字段
    
    例如：
        输入：
        {"公司名称": "上海妙可蓝多食品科技股份有限公司"}
        输出：
        {'公司名称': '上海妙可蓝多食品科技股份有限公司',
         '登记状态': '存续',
         '统一社会信用代码': '91370000164102345T',
         '法定代表人': '柴琇', 
         '注册资本': '51379.1647', 
         '成立日期': '1988-11-29', 
         '企业地址': '上海市奉贤区工业路899号8幢', 
         '联系电话': '021-50185677', 
         '联系邮箱': 'pr@milkground.cn', 
         '注册号': '310000000165830', 
         '组织机构代码': '16410234-5', 
         '参保人数': '370', 
         '行业一级': '科学研究和技术服务业', 
         '行业二级': '科技推广和应用服务业', 
         '行业三级': '其他科技推广服务业', 
         '曾用名': '上海广泽食品科技股份有限公司,\n山东大成农药股份有限公司,\n山东农药工业股份有限公司', 
         '企业简介': '上海妙可蓝多食品科技股份有限公司（简称广泽股份，曾用名：上海广泽食品科技股份有限公司）始创于1998年，总部设在有“东方美谷”之称的上海市奉贤区，系上海证券交易所主板上市公司（证券代码600882）。广泽股份主要生产奶酪和液态奶两大系列产品，拥有“妙可蓝多”“广泽”“澳醇牧场”等国内知名品牌。公司分别在上海、天津、长春和吉林建有4间奶酪和液态奶加工厂，是国内领先的奶酪生产企业。秉承“成为满足国人需求的奶酪专家”的品牌理念，广泽股份一直致力于整合全球资源，为国人提供最好的奶酪产品。公司聘请了一批资深专家加盟，在上海、天津设立了研发中心，并与来自欧洲、澳洲的奶酪公司展开合作，引进了国际先进的生产设备和技术。为从根本上保证产品品质，公司在吉林省建有万头奶牛生态牧场，奶牛全部为进口自澳洲的荷斯坦奶牛，奶质已达欧盟标准。目前，公司可为餐饮和工业客户提供黄油、稀奶油、炼乳、车达和马苏里拉奶酪、奶油芝士、芝士片、芝士酱等产品系列，可直接为消费者提供棒棒奶酪、成长奶酪、三角奶酪、小粒奶酪、新鲜奶酪、慕斯奶酪和辫子奶酪、雪球奶酪等特色产品系列。多年来，广泽股份一直坚持“广纳百川，泽惠四海”的经营理念，恪守“以客户为中心，以奋斗者为本，诚信感恩，务实进取”的核心价值观，努力提高研发和生产技术，不断开发满足消费者需求的奶酪产品，成为深受消费者喜爱的乳品行业知名品牌。', 
         '经营范围': '许可项目：食品经营；食品互联网销售；互联网直播服务（不含新闻信息服务、网络表演、网络视听节目）；互联网信息服务；进出口代理。（依法须经批准的项目，经相关部门批准后方可开展经营活动，具体经营项目以相关部门批准文件或许可证件为准）一般项目：乳制品生产技术领域内的技术开发、技术咨询、技术服务、技术转让；互联网销售（除销售需要许可的商品）；互联网数据服务；信息系统集成服务；软件开发；玩具销售。（除依法须经批准的项目外，凭营业执照依法自主开展经营活动）'
         }
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_company_register"

    data = {
        "query_conds":query_conds,
        "need_fields": need_fields
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def search_company_name_by_register(key: str, value: str) -> dict:
    """
    根据公司注册信息某个字段是某个值来查询具体的公司名称。
    可以输入的字段有['企业类型','区县','参保人数','城市',
    '成立日期','曾用名','注册号','注册资本','登记状态',
    '省份','组织机构代码','统一社会信用代码']

    例如：
        输入：
        {"key": "注册号",
         "value": "440101000196724"}
        输出：
        {"公司名称": "广州发展集团股份有限公司"}
    """
    url = f"https://{DOMAIN}/law_api/search_company_name_by_register"

    data = {
        "key": key,
        "value": value
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def get_listed_company_info(company_name: Union[str, List[str]]) -> dict:
    """
    根据公司名称获得与该公司有关的所有关联上市公司信息。

    例如：
        输入：
        {"company_name": "广东天昊药业有限公司"}
        输出：
        {'上市公司关系': '子公司',
         '上市公司参股比例': '100.0',
         '上市公司投资金额': '7000.00万',
         '公司名称': '广东天昊药业有限公司',
         '关联上市公司全称': '冠昊生物科技股份有限公司',
         '关联上市公司股票代码': '300238',
         '关联上市公司股票简称': '冠昊生物'}
    """
    url = f"https://{DOMAIN}/law_api/get_sub_company_info"

    data = {
        "company_name": company_name
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def search_company_name_by_super_info(key: str, value: str) -> dict:
    """
    根据关联上市公司信息某个字段是某个值来查询具体的公司名称。
    可以输入的字段有['上市公司关系','上市公司参股比例','上市公司投资金额','关联上市公司全称',
    '关联上市公司股票代码','关联上市公司股票简称',]

    例如：
        输入：
        {"key": "关联上市公司全称",
         "value": "冠昊生物科技股份有限公司"}
        输出：
        [{'公司名称': '北昊干细胞与再生医学研究院有限公司'},
         {'公司名称': '北京申佑医学研究有限公司'},
         {'公司名称': '北京文丰天济医药科技有限公司'},
         {'公司名称': '冠昊生命健康科技园有限公司'}]
    """
    url = f"https://{DOMAIN}/law_api/search_company_name_by_sub_info"

    data = {
        "key": key,
        "value": value
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def get_legal_document(case_num: Union[str, List[str]]) -> dict:
    """
    根据案号获得该案所有基本信息。

    例如：
        输入：
        {"case_num": "(2020)赣0191民初1045号"}
        输出：
        {'判决结果': '一、南昌绿地申新置业有限公司于本判决生效之日起十五日内向上海澳辉照明电器有限公司支付本金1179104元。\n'
             '二、南昌绿地申新置业有限公司于本判决生效之日起十五日内向上海澳辉电器有限公司支付利息(以质保金1179104元为基数,按年利率6%,从2019年6月7日起计算至1179104元实际付清之日止)。\n'
             '三、驳回上海澳辉电器有限公司的其他诉讼请求。',
         '原告': '上海澳辉照明电器有限公司',
         '原告律师': '刘某某,北京大成(南昌)律师事务所律师\n罗某某,北京大成(南昌)律师事务所律师',
         '审理法条依据': '无',
         '文书类型': '民事判决书',
         '文件名': '（2020）赣0191民初1045号.txt',
         '标题': '上海澳辉照明电器有限公司与上海建工集团股份有限公司、南昌绿地申新置业有限公司合同纠纷一审民事判决书',
         '案号': '(2020)赣0191民初1045号',
         '案由': '合同纠纷',
         '涉案金额': '1179104',
         '胜诉方': '原告',
         '被告': '上海建工集团股份有限公司\n南昌绿地申新置业有限公司',
         '被告律师': '罗丽萍,公司员工\n李某某,江西豫章律师事务所律师\n蔡某某,江西豫章律师事务所实习律师'}
    """
    if isinstance(case_num, str):
        case_num = case_num.replace('（', '(').replace('）', ')')

    if isinstance(case_num, list):
        new_case_num = []
        for ele in case_num:
            new_case_num.append(ele.replace('（', '(').replace('）', ')'))
        case_num = new_case_num

    url = f"https://{DOMAIN}/law_api/get_legal_document"

    data = {
        "case_num": case_num
    }
    
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def search_case_num_by_legal_document(key: str, value: str) -> dict:
    """
    根据法律文书某个字段是某个值来查询具体的案号。
    可以输入的字段有['判决结果','原告','原告律师','审理法条依据',
    '文书类型','文件名','标题','案由','涉案金额',
    '胜诉方','被告','被告律师',]

    例如：
        输入：
        {"key": "原告",
         "value": "光明乳业股份有限公司"}
        输出：
        [{'案号': '(2020)苏06民初861号'},
         {'案号': '(2021)沪0104民初6181号'},
         {'案号': '(2021)沪0104民初17782号'},
         {'案号': '(2019)湘0111民初3091号'}]
    """
    url = f"https://{DOMAIN}/law_api/search_case_num_by_legal_document"

    data = {
        "key": key,
        "value": value
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()


def search_company_and_registered_capital_by_industry(industry_name: str):
    """根据行业查询属于该行业的公司及其注册资本。"""
    company_names = search_company_name_by_info(key="所属行业", value=industry_name)
    if len(company_names) == 0:
        return []
    company_names = [company_name["公司名称"] for company_name in company_names]
    company_and_registered_capital_list = []
    for company_name in company_names:
        register_info = get_company_register(company_name)
        cnr_info = {
            "公司名称": company_name,
            "注册资本": register_info["注册资本"] if "注册资本" in register_info else None,
        }
        company_and_registered_capital_list.append(cnr_info)
    return company_and_registered_capital_list


