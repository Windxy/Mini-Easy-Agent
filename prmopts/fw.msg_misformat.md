回复格式错误。严格按照系统提示的JSON消息格式进行格式化。具体示例如下：
~~~json
{
    "thoughts": [
        "step1.用户请求提取昨天下载的zip文件。",
        "step2.解决方案的步骤是...",
        "step3.我将逐步处理...",
        "step4.步骤分析...",
        "..."
    ],
    "tool_name": "name_of_tool",
    "tool_args": {
        "arg1": "val1",
        "arg2": "val2"
    }
}
~~~

code_excute示例如下
~~~json
{
    "thoughts": [
        "step1.用户想要绘制...",
        "step2.我将使用..."
    ],
    "tool_name": "code_excute",
    "tool_args": {
        "runtime": "python",
        "code":"import matplotlib...",
        // "if_excute":False
    }
}
~~~