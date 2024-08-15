from brain.Tool import Tool
import requests
from termcolor import cprint
import subprocess
import os
    
class CodeExcuteTool(Tool):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, **kwargs)
    
    def execute_python(self, code):
        try:
            res = self.execute_python_code(code)
            # print(res)
            return "code_excute调用成功，结果为"+ str(res)
        except Exception as e:
            cprint(f"Error: {e}", 'red')
            return "报错了,Error: "+ str(e) + "请检查代码"
    
    def excute_terminal(self, code):
        try:
            # 终端执行命令
            res = os.system(code)
            return "code_excute调用成功"+str(res)
        except Exception as e:
            cprint(f"Error: {e}", 'red')
            return "报错了,Error: "+ str(e) + "请检查代码"
        
    def execute_python_code(self, code):
        """
        执行生成的Python代码并捕获输出结果
        参数:
        code (str): 需要执行的Python代码
        返回:
        str: 代码执行结果
        """
        try:
            # 写入临时文件
            with open("temp_python_code.py", "w") as f:
                f.write(code)
            # 执行临时文件中的代码
            result = subprocess.run(["python", "temp_python_code.py"], capture_output=True, text=True)
            cprint("执行代码成功"+result.stdout, 'light_green')
            # 捕获标准输出和错误输出
            output = result.stdout + result.stderr
            return output
        
        except Exception as e:
            return f"Error: {str(e)}"
    def execute(self, **kwargs):
        runtime = self.args.get("runtime")
        code = self.args.get("code")
        if runtime == 'python':
            response = self.execute_python(code) # 我想写一个1加到100的代码
            return response
        if runtime == 'terminal':
            response = self.excute_terminal(code)
            return response
        return "暂不支持该语言"

    def before_execution(self, **kwargs):
        super().before_execution(**kwargs)
        
    
    def after_execution(self, response, **kwargs):
        super().after_execution(response, **kwargs)
    
    def pipeline(self, response, **kwargs):
        self.before_execution(**kwargs)
        response = self.execute(**kwargs)
        self.after_execution(response, **kwargs)
        return response