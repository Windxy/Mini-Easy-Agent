# 构建Agent类，用于与OpenAI交互
# - “大脑”功能，用于调用OpenAI接口
# - 记忆功能，用于记录对话历史
# - 交互功能，用于处理用户输入,输出对话结果
# - 状态功能，用于记录对话状态
# - 评估功能，用于评估对话结果

from utils.file_reader import read_file
from utils.json_parse import DirtyJson
from utils.fixed_deque import FixedFrontDeque

from brain.inference import fetch_openai_response_stream, fetch_openai_response
from collections import deque
import json
from termcolor import colored,cprint
import os
import traceback # 记录错误

def json_parse_dirty(json:str):
    ext_json = extract_json_object_string(json)
    if ext_json:
        # ext_json = fix_json_string(ext_json)
        data = DirtyJson.parse_string(ext_json)
        if isinstance(data,dict) and 'tool_name' not in data:
            return None
        if isinstance(data,dict): 
            return data
        
    return None

def extract_json_object_string(content):
    start = content.find('{')
    if start == -1:
        return ""
    # Find the first '{'
    end = content.rfind('}')
    if end == -1:
        # If there's no closing '}', return from start to the end
        return content[start:]
    else:
        # If there's a closing '}', return the substring from start to end
        return content[start:end+1]

class Agent:
    def __init__(self):
        self.tools = {}
        self.output = []
        # self.brain =
        self.status = []
        self.evaluation = []
        self.prompt_system = read_file('./prmopts/agent.system.md')
        self.prompt_tool = read_file('./prmopts/agent.tools.md')
        self.msg_misformat = read_file('./prmopts/fw.msg_misformat.md')
        self.prompt = self.prompt_tool+self.prompt_tool
        self.init_tools()
        self.messages = FixedFrontDeque([{"role": "system", "content": self.prompt}],maxlen=10) # 用于记录对话历史，最多10条
        self.api_key =   'LOCAL_LLM'                # 'sk-xxx'  本地则使用LOCAL_LLM
        self.base_url =  "http://0.0.0.0:23333/v1"  # 如'https://api.deepseek.com'
        self.model_name = 'Qwen/Qwen2-7B-Instruct'  # 如'deepseek-chat'
        
        '''
            {"role": "user", "content": user_input}
            {"role": "assistant", "content": response}
        '''
        # self.messages.append({"role": "system", "content": self.prompt})

    def init_tools(self):
        # 工具都在tools文件夹下，需要动态加载
        '''每个工具都是一个类，继承自Tool类，实现execute方法，./tools/tool_response.py示例如下
        from brain.Tool import Tool

        class ResponseTool(Tool):
            def execute(self, **kwargs):
                return self.args["text"]

            def before_execution(self, **kwargs):
                pass

            def after_execution(self, response, **kwargs):
                pass
        '''
        tools = os.listdir('./tools')
        for tool in tools:
            if 'tool' in tool and tool.endswith('.py') and tool != '__init__.py':
                tool_name = tool.split('.')[0].split('tool_')[-1]
                # 加载模块
                module = __import__(f'tools.tool_{tool_name}', fromlist=[tool_name])
                # 加载类：类名 = tool_name去掉下划线并每个首字母大写+Tool,如tool_response.py对应ResponseTool，tool_get_weather.py对应GetWeatherTool
                class_name = ''.join([i.capitalize() for i in tool_name.split('_')])
                tool_class = getattr(module, class_name+'Tool')
                # 实例化
                tool_instance = tool_class(tool_name)
                self.tools[tool_name] = tool_instance
                cprint(f"加载工具{tool_name}成功",'green')
        # print(self.tools)


    def enter(self):
        while True:
            user_input = input('请输入您的问题：\n1.如果想退出，请输入exit >>>')
            if user_input == "exit":
                break
            circle_times = 0
            while True:
                if circle_times > 10:
                    cprint(f"超过10次，放弃解答",'red')
                    break
                circle_times += 1
                response = self.brain(user_input)

                response_json = json_parse_dirty(response)
                self.messages.append({
                    "role": "assistant",
                    "content": response
                })
                # 根据res_json指定tool
                if response_json is not None:
                    # response_json_str = json.dumps(response_json, indent=2, ensure_ascii=False)
                    if_finish = self.interaction(response_json)
                    if if_finish:
                        break
                else:
                    cprint(f"返回结果不符合固定格式,正在尝试让agent重新运行",'red')
                    self.messages.append({
                        "role": "system",
                        "content": self.msg_misformat  # 女朋友过七夕，送什么礼物比较好    你好，我想给我的女朋友写一篇情书，请帮我写一篇    我想写一个汉罗塔的python脚本
                    })

    def brain(self, user_input=None):
        # try:
        if not user_input:
            return "请输入您的问题"
        
        self.messages.append(
            {"role": "user", "content": user_input }
        )
        # 回复
        response = fetch_openai_response_stream(self.messages,self.api_key,self.base_url,self.model_name)
        res_dict = json_parse_dirty(response)

        if res_dict is None:
            return response

        elif 'if_update' in res_dict and res_dict['if_update'] is True:
            self.prompt_system = read_file('./prmopts/agent.system.md')
            self.prompt_tool = read_file('./prmopts/agent.tools.md')
            self.prompt = self.prompt_tool+self.prompt_tool
            self.messages = deque(maxlen=10)
            self.messages.append({"role": "system", "content": self.prompt})
            cprint('💡系统提示已更新',color='red',on_color='on_light_yellow')
        
        return response
        # except Exception as e:
        #     cprint(f"brain方法出现错误：{e}",'red')
        #     cprint(f'错误行数：{e.__traceback__.tb_lineno}', 'red')
        #     return None

    def memory(self):
        pass

    def interaction(self,response_json:dict):
        try:
            # print(response_json) # 
            if 'tool_name' in response_json:
                tool_name = response_json['tool_name']
                tool = self.tools.get(tool_name)
                # cprint(tool,'yellow')
                if tool is not None:
                    tool.args = response_json['tool_args']
                    response = tool.pipeline(tool.args,llm=fetch_openai_response)
                    self.messages.append({
                        "role": "system",
                        "content": response
                    })
                    self.messages.append({
                        "role": "system",
                        "content": "上述给到的答案是否满足用户的需求？如果能，请直接返回yes，如果不能，请输入no"
                    })
                    res = fetch_openai_response_stream(self.messages,self.api_key,self.base_url,self.model_name)
                    if res == 'yes':
                        cprint(f"用户需求得到满足",'green')
                        cprint(f"结果如下\n{response}",'light_yellow')
                        return True
                else:
                    cprint(f"未找到工具{tool_name}",'red')
                    self.messages.append({
                        "role": "system",
                        "content": "没有在工具库中找到对应的工具，尝试重新运行，请稍等"
                    })
                return False
            else:
                cprint(f"未找到工具",'red')
                return False
        except Exception as e:
            cprint(f"interaction出现错误：{e}",'red')
            traceback.print_exc()
            return False
        
    def status(self):
        pass

    def evaluation(self):
        pass

def main():
    agent = Agent()
    agent.brain("你好")
    
if __name__ == "__main__":
    main()