from brain.Tool import Tool



file_read_prompt = "你是一个内容解读工具，现在，用户将给你一个文件内容，你需要读取文件内容并返回给用户这个内容的总结或解读，并给用户一些建议反馈。"

'''文件解读工具'''
class FileReaderTool(Tool):
    def execute(self, **kwargs):
        try:
            file_path = self.args.get("file_path")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            brain = kwargs.get("llm")
            res = brain(user_input=content,prompt=file_read_prompt)
            # messages = []

            return "文件解读成功，内容如下\n"+res
        except Exception as e:
            return "文件格式不对，请检查文件路径"

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