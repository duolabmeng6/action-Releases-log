import os


def Github输出变量(name,value):
    GITHUB_OUTPUT = os.getenv("GITHUB_OUTPUT", "")
    with open(GITHUB_OUTPUT, "a") as file:
        file.write(f"{name}={value}\n")

def Github输出变量多行文本(name, value):
    GITHUB_OUTPUT = os.getenv("GITHUB_OUTPUT", "")
    with open(GITHUB_OUTPUT, "a") as file:
        file.write(f"{name}<<EOF\n{value}\nEOF\n")
    
    # # 读取这个文件内容看看
    # with open(GITHUB_OUTPUT, 'r') as file:
    #     content = file.read()
    #     print(content)



def Github输出状态(name,value):
    GITHUB_STATE = os.getenv("GITHUB_STATE", "")
    with open(GITHUB_STATE, "a") as file:
        file.write(f"{name}={value}\n")

# def main():
#     # print(os.environ)
#     GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
#     # print("GITHUB_REPOSITORY",GITHUB_REPOSITORY)
#     INPUT_TOKEN = os.environ.get('INPUT_TOKEN')
#     Github输出变量("NewVersion",新版本号)
