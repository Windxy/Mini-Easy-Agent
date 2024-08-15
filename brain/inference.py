from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
import time
from termcolor import colored,cprint
# from markdown import markdown

# 异步调用
PROMPT_SYSTEM = "请问有什么可以帮助您的吗？"


# 异步代码允许在等待 I/O 操作（如网络请求）时执行其他任务，从而提高程序的并发性和性能。同步代码在等待 I/O 操作时会阻塞，无法同时处理其他任务。
# 同步版本会在每个网络请求期间阻塞主线程，因此如果你的应用需要同时处理多个任务（例如处理多个用户请求），可能会导致性能瓶颈。
# async def fetch_openai_response():
#     client = AsyncOpenAI(api_key='YOUR_API_KEY',
#                          base_url='http://0.0.0.0:23333/v1')
#     model_cards = await client.models.list()._get_page()
#     response = await client.chat.completions.create(
#         model=model_cards.data[0].id,
#         messages=[
#             {
#                 'role': 'system',
#                 'content': 'You are a helpful assistant.'
#             },
#             {
#                 'role': 'user',
#                 'content': ' provide three suggestions about time management'
#             },
#         ],
#         temperature=0.8,
#         top_p=0.8)
#     print(response)
# asyncio.run(fetch_openai_response())

# def main():
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(fetch_openai_response())
#     print(result)

# 同步
def fetch_openai_response(user_input,api_key='YOUR_API_KEY',base_url="http://0.0.0.0:23333/v1"):
    if not user_input:
        return "请输入您的问题"
    client = OpenAI(api_key=api_key,base_url=base_url)
    model_name = client.models.list().data[0].id
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.8,  # 随机
        top_p=0.8
    )
    res = response.choices[0].message.content
    # print(res)
    # html = markdown(res)
    # print(html)
    return res

# 同步+流式输出
def fetch_openai_response_stream(messages,api_key='LOCAL_LLM',base_url="http://0.0.0.0:23333/v1",model_name='Qwen/Qwen2-7B-Instruct'):
    client = OpenAI(api_key=api_key,base_url=base_url)
    if not messages:
        return "请输入您的问题"
    if api_key == 'LOCAL_LLM':
        model_name = client.models.list().data[0].id
        
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.8,
        top_p=0.85,
        stream=True
    )
    
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        chunk_message = chunk.choices[0].delta.content  # extract the message
        collected_messages.append(chunk_message)  # save the message
        print(colored(chunk_message, 'yellow'), end='')  # print the delay and text
    print()
    return ''.join(collected_messages)


if __name__ == '__main__':
    user_input = input("请输入您的问题：")
    fetch_openai_response_stream(user_input)
    