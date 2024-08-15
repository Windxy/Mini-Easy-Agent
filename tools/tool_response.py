from brain.Tool import Tool

'''
该类可以当作一个模板
- Tool类是所有工具的父类
- before_execution方法用于在执行工具之前打印工具的名称和参数
- after_execution方法用于在执行工具之后打印工具的名称和返回的信息
- execute类继承自Tool类，用于返回执行结果
- pipeline方法搭建了整个工具的执行流程
'''
class ResponseTool(Tool):
    def execute(self, **kwargs):
        return self.args["text"]

    def before_execution(self, **kwargs):
        super().before_execution(**kwargs)
        pass

    def after_execution(self, response, **kwargs):
        super().after_execution(response, **kwargs)
        pass

    def pipeline(self, response, **kwargs):
        self.before_execution(**kwargs)
        response = self.execute(**kwargs)
        self.after_execution(response, **kwargs)
        return response