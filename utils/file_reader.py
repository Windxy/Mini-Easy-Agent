# 本文件用于文件的读、写操作
# 执行本文件，会打印当前文件的上级目录、拼接的绝对路径、文件是否存在
import os,re

def read_file(abs_path):
    # 提供绝对路径，读取文件内容
    with open(abs_path) as f:
        content = f.read()
    content = remove_code_fences(content)
    
    return content

def remove_code_fences(text):
    return re.sub(r'~~~\w*\n|~~~', '', text)

def write_file(abs_path, content):
    # 提供绝对路径，写入文件内容
    with open(abs_path, "w") as f:
        f.write(content)

def get_abs_path(*relative_paths):
    # 获取相对路径对应的绝对路径,*代表可变参数，可以接受多个参数
    return os.path.join(get_base_dir(), *relative_paths)

def get_base_dir():
    # 获取当前执行的文件所在目录的上级目录
    base_dir = os.path.dirname(os.path.abspath(os.path.join(__file__,"../")))
    return base_dir

def exists(*relative_paths):
    # 判断文件是否存在
    path = get_abs_path(*relative_paths)
    return os.path.exists(path)

if __name__ == "__main__":
    # 测试代码
    print(get_base_dir())
    print(get_abs_path("data", "test.txt"))
    print(exists("data", "test.txt"))
    content = read_file(get_abs_path("agent.tools_v1.md"))
    print(remove_code_fences(content))