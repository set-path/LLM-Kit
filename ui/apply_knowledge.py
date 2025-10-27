import gradio as gr
import os
from utils.ui_utils import chat_base_model
from utils.local_doc import local_doc_qa
from modules.agent.chatdb.mysql import MySQLDB
import pandas as pd

def get_directories(path,unuse):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d not in unuse]

real_path = os.path.split(os.path.realpath(__file__))[0]
new_path = os.path.join(real_path, "..", "models", "LLM")
models = get_directories(new_path,['runs','vector_store'])
new_path = os.path.join(real_path, "..", "models", "LoRA")
loras = get_directories(new_path,[])
new_path = os.path.join(real_path, "..", "models", "Embedding")
embs = get_directories(new_path,[])
new_path = os.path.join(real_path, "..", "data", "documents")
docs = get_directories(new_path,[])

chat_model=chat_base_model()
doc_qa=local_doc_qa()
mysql = MySQLDB()

model_api = ['openai', 'azure openai', 'ernie bot',
             'ernie bot turbo', 'chatglm api', 'spark api','ali api']

embedding_api = ['openai','azure openai']

def refresh_directories_faiss():
    new_path = os.path.join(real_path, "..", "models", "LLM")
    models = get_directories(new_path,['runs','vector_store'])
    new_path = os.path.join(real_path, "..", "models", "LoRA")
    loras = get_directories(new_path,[])
    new_path = os.path.join(real_path, "..", "data", "documents")
    docs = get_directories(new_path,[])
    new_path = os.path.join(real_path, "..", "models", "Embedding")
    embs = get_directories(new_path,[])
    return gr.update(choices=models),gr.update(choices=[None]+loras),gr.update(choices=[None]+docs),gr.update(choices=embs)

def refresh_directories_mysql():
    new_path = os.path.join(real_path, "..", "models", "LLM")
    models = get_directories(new_path,['runs','vector_store'])
    return gr.update(choices=models)

def model_select(api, model, lora):
    if model == None:
        return gr.update(value=api), gr.update(value=model), gr.update(value=lora)
    else:
        return gr.update(value=None), gr.update(value=model), gr.update(value=lora)


def api_select(api, model, lora):
    if api == None:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=model), gr.update(value=lora)
    elif api == 'openai':
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'azure openai':
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'ernie bot':
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'ernie bot turbo':
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'chatglm api':
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False),gr.update(visible=False), gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'spark api':
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False),gr.update(value=api), gr.update(value=None), gr.update(value=None)
    elif api == 'ali api':
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(value=api), gr.update(value=None),gr.update(value=None)
    else:
        pass

def emb_model_select(emb_api_list,emb_model_list):
    if emb_model_list is None:
        return gr.update(value=emb_api_list), gr.update(value=emb_model_list)
    else:
        return gr.update(value=None), gr.update(value=emb_model_list)
    
def emb_api_select(emb_api_list,emb_model_list):
    if emb_api_list is None:
        return gr.update(visible=False),gr.update(visible=False), gr.update(value=emb_api_list), gr.update(value=emb_model_list)
    elif emb_api_list == 'openai':
        return gr.update(visible=True), gr.update(visible=False),gr.update(value=emb_api_list), gr.update(value=None)
    elif emb_api_list == 'azure openai':
        return gr.update(visible=False),gr.update(visible=True), gr.update(value=emb_api_list), gr.update(value=None)
    else:
        pass

def mysql_model_select(api, model):
    if model == None:
        return gr.update(value=api), gr.update(value=model)
    else:
        return gr.update(value=None), gr.update(value=model)
    
def mysql_api_select(api, model):
    if api == None:
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=model)
    elif api == 'openai':
        return gr.update(visible=True), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(value=api), gr.update(value=None)
    elif api == 'azure openai':
        return gr.update(visible=False),gr.update(visible=True), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False),gr.update(visible=False), gr.update(value=api), gr.update(value=None)
    elif api == 'ernie bot':
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=True), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None)
    elif api == 'ernie bot turbo':
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=True),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(value=api), gr.update(value=None)
    elif api == 'chatglm api':
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=True), gr.update(visible=False), gr.update(visible=False),gr.update(value=api), gr.update(value=None)
    elif api == 'spark api':
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=True), gr.update(visible=False),gr.update(value=api), gr.update(value=None)
    elif api == 'ali api':
        return gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(value=api), gr.update(value=None)
    else:
        pass


def load_faiss_params(api_list, model_list, lora_list, *args):
    params = {}
    if api_list is not None:
        if api_list == 'openai':
            params['name'] = 'openai'
            params['api_key'] = args[0]
            params['port'] = args[1]
            params['api_base'] = args[2]
            params['api_model'] = args[3]
        elif api_list == 'azure openai':
            params['name'] = 'azure openai'
            params['api_key'] = args[4]
            params['endpoint'] = args[5]
            params['engine'] = args[6]
        elif api_list == 'ernie bot':
            params['name'] = 'ernie bot'
            params['api_key'] = args[7]
            params['secret_key'] = args[8]
            params['temperature'] = args[9]
            params['top_p'] = args[10]
            params['penalty_score'] = args[11]
        elif api_list == 'ernie bot turbo':
            params['name'] = 'ernie bot turbo'
            params['api_key'] = args[12]
            params['secret_key'] = args[13]
        elif api_list == 'chatglm api':
            params['name'] = 'chatglm api'
            params['api_key'] = args[14]
            params['temperature'] = args[15]
            params['top_p'] = args[16]
            params['type'] = args[17]
        elif api_list == 'spark api':
            params['name'] = 'spark api'
            params['appid'] = args[18]
            params['api_key'] = args[19]
            params['secret_key'] = args[20]
            params['api_version'] = args[21]
            params['temperature'] = args[22]
            params['top_k'] = args[23]
            params['max_tokens'] = args[24]
        elif api_list == 'ali api':
            params['name'] = 'ali api'
            params['api_key'] = args[25]
            params['top_p'] = args[26]
            params['top_k'] = args[27]
            params['kuake_search'] = args[28]
        else:
            pass
        return chat_model.load_api_params(params)
    elif model_list is not None:
        params['name'] = model_list
        params['lora'] = lora_list
        params['quantization'] = args[29]
        params['max_length'] = args[30]
        params['top_p'] = args[31]
        params['temperature'] = args[32]
        params['use_deepspeed'] = args[33]
        return chat_model.load_model(params)
    raise gr.Error('请选择API或模型')
    
def load_embedding_params(doc1,k,score_threshold,chunk_size,chunk_conent,emb_api_list,emb_model_list,*args):
    params = {}
    params['doc'] = doc1
    params['k'] = k
    params['score_threshold'] = score_threshold
    params['chunk_size'] = chunk_size
    params['chunk_conent'] = chunk_conent
    if emb_api_list is not None:
        if emb_api_list == 'openai':
            params['name'] = 'openai'
            params['api_key'] = args[0]
            params['port'] = args[1]
            params['api_base'] = args[2]
            params['api_model'] = args[3]
        elif emb_api_list == 'azure openai':
            params['name'] = 'azure openai'
            params['api_key'] = args[4]
            params['endpoint'] = args[5]
            params['engine'] = args[6]
        else:
            pass
    elif emb_model_list is not None:
        params['name'] = emb_model_list
    if doc_qa.load(params):
        return '',[],[]

def load_mysql_params(mysql_api_list,mysql_model_list,*args):
    params = {}
    if mysql_api_list is not None:
        if mysql_api_list == 'openai':
            params['name'] = 'openai'
            params['api_key'] = args[0]
            params['port'] = args[1]
            params['api_base'] = args[2]
            params['api_model'] = args[3]
        elif mysql_api_list == 'azure openai':
            params['name'] = 'azure openai'
            params['api_key'] = args[4]
            params['endpoint'] = args[5]
            params['engine'] = args[6]
        elif mysql_api_list == 'ernie bot':
            params['name'] = 'ernie bot'
            params['api_key'] = args[7]
            params['secret_key'] = args[8]
            params['temperature'] = args[9]
            params['top_p'] = args[10]
            params['penalty_score'] = args[11]
        elif mysql_api_list == 'ernie bot turbo':
            params['name'] = 'ernie bot turbo'
            params['api_key'] = args[12]
            params['secret_key'] = args[13]
        elif mysql_api_list == 'chatglm api':
            params['name'] = 'chatglm api'
            params['api_key'] = args[14]
            params['temperature'] = args[15]
            params['top_p'] = args[16]
            params['type'] = args[17]
        elif mysql_api_list == 'spark api':
            params['name'] = 'spark api'
            params['appid'] = args[18]
            params['api_key'] = args[19]
            params['secret_key'] = args[20]
            params['api_version'] = args[21]
            params['temperature'] = args[22]
            params['top_k'] = args[23]
            params['max_tokens'] = args[24]
        elif mysql_api_list == 'ali api':
            params['name'] = 'ali api'
            params['api_key'] = args[25]
            params['top_p'] = args[26]
            params['top_k'] = args[27]
            params['kuake_search'] = args[28]
        else:
            pass
        return chat_model.load_api_params(params)
    elif mysql_model_list is not None:
        params['name'] = mysql_model_list
        params['quantization'] = args[29]
        params['max_length'] = args[30]
        params['top_p'] = args[31]
        params['temperature'] = args[32]
        params['use_deepspeed'] = args[33]
        return chat_model.load_model(params)
    raise gr.Error('请选择API或模型')

def get_databases(host,user,password,port):
    mysql.connect(host,user,password,port)
    databases = mysql.get_databases()
    return gr.update(choices=databases)

def show_tables(host,user,password,port,database):
    mysql.connect(host,user,password,port,database)
    tables = mysql.get_tables(database)
    return gr.update(choices=tables)

def show_table_data(host,user,password,port,database,table):
    if table is None:
        return gr.update(visible=False)
    mysql.connect(host,user,password,port,database)
    result = mysql.get_table_data(table)
    # 将result转成DataFrame
    df = pd.DataFrame(result)
    # 判断df的长度
    if len(df) == 0:
        fields = mysql.get_fields(table)
        # 将fields转成DataFrame，数据为None
        df = pd.DataFrame(columns=fields)
    return gr.update(value=df,visible=True)

def vec_search(faiss_user_input, faiss_chatbot, history,faiss_net,faiss_search,faiss_search_key,faiss_result_len,doc1):
    if doc1 is None:
        raise gr.Error('请先选择向量知识库')
    for chatbot, history, user_input in chat_model.predict(faiss_user_input, faiss_chatbot, history,faiss_net,faiss_search,faiss_search_key,faiss_result_len,doc=doc1,doc_type='faiss'):
        yield chatbot, history, user_input

def apply_knowledge(localizer):
    with gr.Tab("FAISS"):
        with gr.Row():
            with gr.Column(scale=4):
                faiss_chatbot = gr.Chatbot()
                faiss_user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10,elem_id='faiss-user-input')
                with gr.Accordion(label='',visible=False,elem_id='faiss-submitGroup') as faiss_submitGroup:
                    faiss_submitBtn = gr.Button(localizer("提交"), variant="primary",elem_id='faiss-submitBtn')
                    faiss_emptyBtn = gr.Button(localizer("清除历史"))
            with gr.Column(scale=1):
                with gr.Accordion('',open=True):
                    faiss_Refresh = gr.Button(localizer("刷新"))
                with gr.Accordion(localizer("*选择模型"),open=True):
                    with gr.Tab(localizer("API列表")):
                        faiss_api_list = gr.Radio(model_api, show_label=False, value=None)
                        with gr.Accordion(localizer("openai参数"), open=True, visible=False) as faiss_openai_params:
                            faiss_openai_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*openai_api_key:", type='password')
                            faiss_openai_port = gr.Textbox(
                                lines=1, value='', label="*VPN proxyPort:")
                            faiss_openai_api_base = gr.Textbox(
                                lines=1, value='', label="API base:")
                            faiss_openai_api_model = gr.Radio(
                                ['gpt-3.5-turbo','gpt-4'], label=localizer("API模型"), value='gpt-3.5-turbo')
                        with gr.Accordion(localizer("azure openai参数"), open=True, visible=False) as faiss_azure_openai_params:
                            faiss_azure_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*azure_api_key:", type='password')
                            faiss_azure_endpoint = gr.Textbox(
                                lines=1, value='', label="*endpoint:(azure openai)")
                            faiss_azure_engine = gr.Textbox(
                                lines=1, value='', label="*engine:(azure openai)")
                        with gr.Accordion(localizer("ernie bot参数"), open=True, visible=False) as faiss_ernie_bot_params:
                            faiss_ernie_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            faiss_ernie_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                            faiss_ernie_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                            faiss_ernie_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top P", interactive=True)
                            faiss_ernie_penalty_score = gr.Slider(
                                1, 2, value=1, step=0.05, label="Penalty Score", interactive=True)
                        with gr.Accordion(localizer("ernie bot turbo参数"), open=True, visible=False) as faiss_ernie_bot_turbo_params:
                            faiss_ernie_turbo_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            faiss_ernie_turbo_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                        with gr.Accordion(localizer("chatglm参数"), open=True, visible=False) as faiss_chatglm_params:
                            faiss_chatglm_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            faiss_chatglm_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                            faiss_chatglm_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top P", interactive=True)
                            faiss_chatglm_type = gr.Radio(
                                ['lite', 'std', 'pro'], label=localizer("模型类型"), value='std')
                        with gr.Accordion(localizer("spark api参数"), open=True, visible=False) as faiss_spark_params:
                            faiss_spark_appid = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*appid:", type='password')
                            faiss_spark_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            faiss_spark_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                            faiss_spark_api_version = gr.Radio(["V1.5","V2.0"],label=localizer("API版本"),value="V1.5")
                            faiss_spark_temperature = gr.Slider(
                                0, 1, value=0.5, step=0.05, label="Temperature", interactive=True)
                            faiss_spark_top_k = gr.Slider(
                                1, 6, value=4, step=1, label="Top K", interactive=True)
                            faiss_spark_max_tokens = gr.Slider(
                                0, 4096, value=2048, step=256, label="Maximum tokens", interactive=True)
                        with gr.Accordion(localizer("ali api参数"), open=True, visible=False) as faiss_ali_params:
                            faiss_qwen_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            faiss_ali_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top p", interactive=True,elem_id='chat_ali_top_p')
                            faiss_ali_top_k = gr.Slider(
                                1, 100, value=100, step=1, label="Top k", interactive=True,elem_id='chat_ali_top_k')
                            faiss_ali_kuake_search = gr.Checkbox(label=localizer("联网搜索"))
                    with gr.Tab(localizer("模型列表")):
                        faiss_model_list = gr.Radio(models, show_label=False, value=None)
                        faiss_quantization = gr.Radio([None,'4 bit','8 bit'],value=None,label=localizer("量化方式(不支持Windows)"))
                        faiss_lora_list = gr.Radio(
                            [None]+loras, label=localizer("LoRA模型列表"), value=None)
                        faiss_use_deepspeed = gr.Checkbox(label=localizer('使用deepspeed'))
                        with gr.Accordion(localizer('模型参数'), open=True):
                            faiss_max_length = gr.Slider(
                                0, 4096, value=2048, step=256, label="Maximum length", interactive=True)
                            faiss_top_p = gr.Slider(0, 1, value=0.7, step=0.05,
                                            label="Top P", interactive=True)
                            faiss_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                    faiss_save = gr.Button(localizer("确定"), variant="primary")
                    faiss_emptymodelBtn = gr.Button(localizer("清空"))
                with gr.Accordion(localizer("本地知识库"),open=False):
                    with gr.Tab('*Embedding API'):
                        emb_api_list = gr.Radio(embedding_api, show_label=False,value=None)
                        with gr.Accordion(localizer("openai参数"), open=True, visible=False) as emb_openai_params:
                            embedding_openai_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*openai_api_key:", type='password')
                            embedding_openai_port = gr.Textbox(
                                lines=1, value='', label="*VPN proxyPort:")
                            embedding_openai_api_base = gr.Textbox(
                                lines=1, value='', label=localizer("API base:"))
                            embedding_openai_api_model = gr.Radio(
                                    ['text-embedding-ada-002'], label=localizer("API模型"), value='text-embedding-ada-002')
                        with gr.Accordion(localizer("azure openai参数"), open=True, visible=False) as emb_azure_openai_params:
                            embedding_azure_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*azure_api_key:", type='password')
                            embedding_azure_endpoint = gr.Textbox(
                                lines=1, value='', label="*endpoint:(azure openai)")
                            embedding_azure_engine = gr.Textbox(
                                lines=1, value='', label="*engine:(azure openai)")
                    with gr.Tab(localizer("*嵌入式模型")):
                        emb_model_list = gr.Radio(embs, show_label=False,value=None)
                    with gr.Accordion(localizer('*选择向量知识库'),open=False):
                        doc1 = gr.Radio(docs, show_label=False,value=None)
                    k = gr.Slider(1, 20, value=3, step=1, label=localizer("使用前几条相关文本"), interactive=True)
                    score_threshold = gr.Slider(0, 1100, value=500, step=1, label=localizer("相似度阈值(0不生效)"), interactive=True)
                    chunk_size = gr.Slider(1, 2048, value=250, step=1, label=localizer("每条文本长度"), interactive=True)
                    chunk_conent = gr.Checkbox(label=localizer('相似文本是否启用上下文查询'))
                    save0 = gr.Button(localizer("确定知识库"),variant="primary")
                    emptymodelBtn0 = gr.Button(localizer("取消知识库"))
                with gr.Accordion(localizer("联网搜索"),open=False):
                    faiss_net = gr.Checkbox(label=localizer("联网搜索"))
                    faiss_search = gr.Radio(['bing','google'], label=localizer("选择搜索引擎"))
                    faiss_search_key=gr.Textbox(lines=1, placeholder="Write Here...",label=localizer("*联网key:"),type= 'password')
                    faiss_result_len = gr.Slider(1, 20, value=3, step=1, label=localizer("搜索条数:"), interactive=True)
    with gr.Tab("MySQL"):
        with gr.Row():
            with gr.Column(scale=4):
                    mysql_chatbot = gr.Chatbot()
                    mysql_user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10,elem_id='mysql-user-input')
                    with gr.Accordion(label='',visible=False,elem_id='mysql-submitGroup') as mysql_submitGroup:
                        mysql_submitBtn = gr.Button(localizer("提交"), variant="primary",elem_id='mysql-submitBtn')
                        mysql_emptyBtn = gr.Button(localizer("清除历史"))
            with gr.Column(scale=1):
                with gr.Accordion('',open=True):
                    mysql_Refresh = gr.Button(localizer("刷新"))
                with gr.Accordion(localizer("*选择模型"),open=True):
                    with gr.Tab(localizer("API列表")):
                        mysql_api_list = gr.Radio(model_api, show_label=False, value=None)
                        with gr.Accordion(localizer("openai参数"), open=True, visible=False) as mysql_openai_params:
                            mysql_openai_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*openai_api_key:", type='password')
                            mysql_openai_port = gr.Textbox(
                                lines=1, value='', label="*VPN proxyPort:")
                            mysql_openai_api_base = gr.Textbox(
                                lines=1, value='', label="API base:")
                            mysql_openai_api_model = gr.Radio(
                                ['gpt-3.5-turbo','gpt-4'], label=localizer("API模型"), value='gpt-3.5-turbo')
                        with gr.Accordion(localizer("azure openai参数"), open=True, visible=False) as mysql_azure_openai_params:
                            mysql_azure_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*azure_api_key:", type='password')
                            mysql_azure_endpoint = gr.Textbox(
                                lines=1, value='', label="*endpoint:(azure openai)")
                            mysql_azure_engine = gr.Textbox(
                                lines=1, value='', label="*engine:(azure openai)")
                        with gr.Accordion(localizer("ernie bot参数"), open=True, visible=False) as mysql_ernie_bot_params:
                            mysql_ernie_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            mysql_ernie_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                            mysql_ernie_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                            mysql_ernie_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top P", interactive=True)
                            mysql_ernie_penalty_score = gr.Slider(
                                1, 2, value=1, step=0.05, label="Penalty Score", interactive=True)
                        with gr.Accordion(localizer("ernie bot turbo参数"), open=True, visible=False) as mysql_ernie_bot_turbo_params:
                            mysql_ernie_turbo_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            mysql_ernie_turbo_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                        with gr.Accordion(localizer("chatglm参数"), open=True, visible=False) as mysql_chatglm_params:
                            mysql_chatglm_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            mysql_chatglm_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                            mysql_chatglm_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top P", interactive=True)
                            mysql_chatglm_type = gr.Radio(
                                ['lite', 'std', 'pro'], label=localizer("模型类型"), value='std')
                        with gr.Accordion(localizer("spark api参数"), open=True, visible=False) as mysql_spark_params:
                            mysql_spark_appid = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*appid:", type='password')
                            mysql_spark_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            mysql_spark_secret_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*secret_key:", type='password')
                            mysql_spark_api_version = gr.Radio(["V1.5","V2.0"],label=localizer("API版本"),value="V1.5")
                            mysql_spark_temperature = gr.Slider(
                                0, 1, value=0.5, step=0.05, label="Temperature", interactive=True)
                            mysql_spark_top_k = gr.Slider(
                                1, 6, value=4, step=1, label="Top K", interactive=True)
                            mysql_spark_max_tokens = gr.Slider(
                                0, 4096, value=2048, step=256, label="Maximum tokens", interactive=True)
                        with gr.Accordion(localizer("ali api参数"), open=True, visible=False) as mysql_ali_params:
                            mysql_qwen_api_key = gr.Textbox(
                                lines=1, placeholder="Write Here...", label="*api_key:", type='password')
                            mysql_ali_top_p = gr.Slider(
                                0, 1, value=0.8, step=0.05, label="Top p", interactive=True,elem_id='chat_ali_top_p')
                            mysql_ali_top_k = gr.Slider(
                                1, 100, value=100, step=1, label="Top k", interactive=True,elem_id='chat_ali_top_k')
                            mysql_ali_kuake_search = gr.Checkbox(label=localizer("联网搜索"))
                    with gr.Tab(localizer("模型列表")):
                        mysql_model_list = gr.Radio(models, show_label=False, value=None)
                        mysql_quantization = gr.Radio([None,'4 bit','8 bit'],value=None,label=localizer("量化方式(不支持Windows)"))
                        mysql_use_deepspeed = gr.Checkbox(label=localizer('使用deepspeed'))
                        with gr.Accordion(localizer('模型参数'), open=True):
                            mysql_max_length = gr.Slider(
                                0, 4096, value=2048, step=256, label="Maximum length", interactive=True)
                            mysql_top_p = gr.Slider(0, 1, value=0.7, step=0.05,
                                            label="Top P", interactive=True)
                            mysql_temperature = gr.Slider(
                                0, 1, value=0.95, step=0.05, label="Temperature", interactive=True)
                    mysql_save = gr.Button(localizer("确定"), variant="primary")
                    mysql_emptymodelBtn = gr.Button(localizer("清空"))
                with gr.Accordion(localizer("MySQL知识库"),open=False):
                    # 数据库地址、端口、用户名、密码、数据库名称
                    host = gr.Textbox(lines=1, label=localizer("*数据库地址"), value='localhost')
                    user = gr.Textbox(lines=1, label=localizer("*用户名"), value='')
                    password = gr.Textbox(lines=1, label=localizer("*密码"), type='password', value='')
                    port = gr.Textbox(lines=1, label=localizer("*端口"), value='3306')
                    connect = gr.Button(localizer("连接数据库"), variant="primary")
                    doc0 = gr.Radio(label=localizer("*选择SQL知识库"),value=None)
                    mysql_tables = gr.Radio(label=localizer("选择表"),choices=[],value=None)
        with gr.Row():
            table_data = gr.DataFrame(interactive=False,visible=False)


    history = gr.State([])


    # FAISS
    fasiss_total_params = [faiss_openai_api_key, faiss_openai_port, faiss_openai_api_base, faiss_openai_api_model, faiss_azure_api_key, faiss_azure_endpoint, faiss_azure_engine, faiss_ernie_api_key, faiss_ernie_secret_key, faiss_ernie_temperature, faiss_ernie_top_p, faiss_ernie_penalty_score, faiss_ernie_turbo_api_key, faiss_ernie_turbo_secret_key, faiss_chatglm_api_key, faiss_chatglm_temperature, faiss_chatglm_top_p, faiss_chatglm_type, faiss_spark_appid, faiss_spark_api_key, faiss_spark_secret_key, faiss_spark_api_version, faiss_spark_temperature, faiss_spark_top_k, faiss_spark_max_tokens,faiss_qwen_api_key,faiss_ali_top_p,faiss_ali_top_k,faiss_ali_kuake_search,faiss_quantization,faiss_max_length,faiss_top_p,faiss_temperature,faiss_use_deepspeed]
    embedding_total_params = [embedding_openai_api_key, embedding_openai_port, embedding_openai_api_base, embedding_openai_api_model, embedding_azure_api_key, embedding_azure_endpoint, embedding_azure_engine]
    faiss_Refresh.click(refresh_directories_faiss, outputs=[faiss_model_list,faiss_lora_list,doc1,emb_model_list])
    faiss_save.click(load_faiss_params, [faiss_api_list,faiss_model_list,faiss_lora_list]+fasiss_total_params, [faiss_user_input,faiss_submitGroup],show_progress=True)
    faiss_submitBtn.click(vec_search, [faiss_user_input, faiss_chatbot, history,faiss_net,faiss_search,faiss_search_key,faiss_result_len,doc1], [faiss_chatbot, history,faiss_user_input],show_progress=True)

    faiss_emptyBtn.click(chat_model.reset_state, outputs=[faiss_chatbot,history,faiss_user_input])
    faiss_emptymodelBtn.click(chat_model.clear, outputs=[faiss_chatbot,history,faiss_user_input,faiss_api_list,faiss_model_list,faiss_lora_list,faiss_submitGroup])

    save0.click(load_embedding_params, [doc1,k,score_threshold,chunk_size,chunk_conent,emb_api_list,emb_model_list]+embedding_total_params, [faiss_user_input,faiss_chatbot,history],show_progress=True)
    emptymodelBtn0.click(doc_qa.clear,outputs=[doc1,emb_api_list,emb_model_list])

    faiss_model_list.change(model_select, inputs=[faiss_api_list,faiss_model_list,faiss_lora_list], outputs=[faiss_api_list,faiss_model_list,faiss_lora_list])
    faiss_api_list.change(api_select, inputs=[faiss_api_list,faiss_model_list,faiss_lora_list], outputs=[faiss_openai_params, faiss_azure_openai_params, faiss_ernie_bot_params, faiss_ernie_bot_turbo_params, faiss_chatglm_params, faiss_spark_params, faiss_ali_params,faiss_api_list, faiss_model_list, faiss_lora_list])

    emb_model_list.change(emb_model_select, inputs=[emb_api_list,emb_model_list], outputs=[emb_api_list,emb_model_list])
    emb_api_list.change(emb_api_select, inputs=[emb_api_list,emb_model_list], outputs=[emb_openai_params,emb_azure_openai_params,emb_api_list,emb_model_list])

    # # MySQL
    mysql_total_params = [mysql_openai_api_key, mysql_openai_port, mysql_openai_api_base, mysql_openai_api_model, mysql_azure_api_key, mysql_azure_endpoint, mysql_azure_engine, mysql_ernie_api_key, mysql_ernie_secret_key, mysql_ernie_temperature, mysql_ernie_top_p, mysql_ernie_penalty_score, mysql_ernie_turbo_api_key, mysql_ernie_turbo_secret_key, mysql_chatglm_api_key, mysql_chatglm_temperature, mysql_chatglm_top_p, mysql_chatglm_type, mysql_spark_appid, mysql_spark_api_key, mysql_spark_secret_key, mysql_spark_api_version, mysql_spark_temperature, mysql_spark_top_k, mysql_spark_max_tokens,mysql_qwen_api_key,mysql_ali_top_p,mysql_ali_top_k,mysql_ali_kuake_search,mysql_quantization,mysql_max_length,mysql_top_p,mysql_temperature,mysql_use_deepspeed]
    connect.click(get_databases, inputs=[host,user,password,port],outputs=[doc0])
    mysql_Refresh.click(refresh_directories_mysql, outputs=[mysql_model_list])
    mysql_save.click(load_mysql_params, [mysql_api_list,mysql_model_list]+mysql_total_params, [mysql_user_input,mysql_submitGroup],show_progress=True)
    mysql_submitBtn.click(chat_model.query_from_mysql, [mysql_user_input,mysql_chatbot,doc0,host,
                                         user, password, port,doc0,mysql_tables], [mysql_chatbot,mysql_user_input,doc0,mysql_tables,table_data],show_progress=True)

    mysql_emptyBtn.click(chat_model.reset_state, outputs=[mysql_chatbot,history,mysql_user_input])
    mysql_emptymodelBtn.click(doc_qa.clear_mysql, outputs=[mysql_chatbot,history,mysql_user_input,mysql_api_list,mysql_model_list,mysql_submitGroup])

    doc0.change(show_tables, inputs=[host,user,password,port,doc0],outputs=[mysql_tables])
    mysql_tables.change(show_table_data, inputs=[host,user,password,port,doc0,mysql_tables],outputs=[table_data])

    mysql_model_list.change(mysql_model_select, inputs=[mysql_api_list,mysql_model_list], outputs=[mysql_api_list,mysql_model_list])
    mysql_api_list.change(mysql_api_select, inputs=[mysql_api_list,mysql_model_list], outputs=[mysql_openai_params, mysql_azure_openai_params, mysql_ernie_bot_params, mysql_ernie_bot_turbo_params, mysql_chatglm_params, mysql_spark_params,mysql_ali_params, mysql_api_list,mysql_model_list])

