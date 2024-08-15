# 构建一个Tool类（所有工具的父类）
# 该类包含一个抽象方法execute，一个before_execution方法和一个after_execution方法
# before_execution方法用于在执行工具之前打印工具的名称和参数
# after_execution方法用于在执行工具之后打印工具的名称和返回的信息
# ResponseTool类继承自Tool类，用于返回一个Response对象

from termcolor import colored,cprint
from abc import abstractmethod

class Tool:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name

    @abstractmethod # 抽象方法,子类必须实现
    def execute(self,**kwargs):
        raise NotImplementedError

    def before_execution(self, **kwargs):
        '''在执行工具之前打印工具的名称和参数'''
        cprint(f"使用工具： '{self.name}'", 'green')
        # if self.args and isinstance(self.args, dict):
        #     for key, value in self.args.items():
        #         cprint(f"{key}: ", 'blue', end='')
        #         cprint(value, 'blue')

    def after_execution(self, response, **kwargs):
        cprint(f"使用工具 '{self.name}'成功", 'green')
        # cprint(response, 'blue')

        return response
    
    def pipeline(self,response, **kwargs):
        self.before_execution(**kwargs)
        self.execute(response,**kwargs)
        response = self.after_execution(response, **kwargs)

        return response