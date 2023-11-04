import time
import os
from github import Github
import help

def get_commit_history(repo):
    # 获取提交记录
    commits = repo.get_commits()
    # 检查到2次 [发布] 就停止 获取
    commit_history = ""
    k = 0
    for commit in commits:
        commit_info = f"{commit.author.name}|{commit.commit.message}|{commit.sha[:7]}|{commit.commit.author.date.strftime('%Y-%m-%d %H:%M')}|{commit.sha}\n"
        commit_history += commit_info
        if commit.commit.message.startswith('[发布]'):
            k += 1
            if k == 2:
                break
    return commit_history

def calculate_time_difference(time1, time2):
    timestamp1 = time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M"))
    timestamp2 = time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M"))
    time_difference_seconds = abs(timestamp1 - timestamp2)
    minutes = time_difference_seconds // 60
    hours = minutes // 60
    days = hours // 24
    if days > 0:
        formatted_time = f"{int(days)}天"
    elif hours > 0:
        formatted_time = f"{int(hours)}小时"
    elif minutes > 0:
        formatted_time = f"{int(minutes)}分钟"
    else:
        formatted_time = "一会儿"
    return formatted_time



if __name__ == '__main__':

    GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
    INPUT_TOKEN = os.environ.get('INPUT_GITHUB_TOKEN')
    g = Github(INPUT_TOKEN)
    repo = g.get_repo(GITHUB_REPOSITORY)
    # 通过 Github 获取提交记录生成如下格式的文本
    # 命令的结果 git log --pretty=format:"%an | %s | %h | %ad | %H" --date=format:'%Y-%m-%d %H:%M' $(git describe --tags --abbrev=0)^..HEAD
    # 多啦b梦|[发布]全新的版本ggg|f81cf92|2023-11-05 23:22|f81cf921090609288061e77f53ba472858b133a6
    # 多啦b梦|[新增]独特的功能|cee5f90|2023-11-05 01:22|cee5f90469c13ff3d3ba41424773439033a1e029
    # 多啦b梦|[修复]一个神器的bug|60472ca|2023-11-05 01:21|60472ca310df178cd5f3ccb740c0b5e86ced62f9
    # 多啦b梦|[新增]嘻嘻嘻功能|d99add4|2023-11-05 01:21|d99add4025f41622dbc1985083a35bf5a676f1fa
    # 多啦b梦|[加强]笑嘻嘻的|d99add4|2023-11-05 01:21|d99add4025f41622dbc1985083a35bf5a676f1fa
    # 多啦b梦|[发布]全新牛逼plus的 加入了自动更新|2a2a82a|2023-11-05 01:19|2a2a82a71dd177379147d51846f08804e11be9b8

    result = get_commit_history(repo)
    print(result)


    # #执行命令获取结果
    # cmd = """git log --pretty=format:"%an | %s | %h | %ad | %H" --date=format:'%Y-%m-%d %H:%M' $(git describe --tags --abbrev=0)^..HEAD"""
    #
    # try:
    #     result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, text=True)
    #     git_log_output = result.stdout
    #     print(git_log_output)
    # except subprocess.CalledProcessError as e:
    #     # 如果命令运行失败，捕获异常
    #     print(f"Error: {e}")
    #     exit(0)

    text = """多啦b梦|[发布]全新的版本ggg|f81cf92|2023-11-05 23:22|f81cf921090609288061e77f53ba472858b133a6
多啦b梦|[新增]独特的功能|cee5f90|2023-11-05 01:22|cee5f90469c13ff3d3ba41424773439033a1e029
多啦b梦|[修复]一个神器的bug|60472ca|2023-11-05 01:21|60472ca310df178cd5f3ccb740c0b5e86ced62f9
多啦b梦|[新增]嘻嘻嘻功能|d99add4|2023-11-05 01:21|d99add4025f41622dbc1985083a35bf5a676f1fa
多啦b梦|[加强]笑嘻嘻的|d99add4|2023-11-05 01:21|d99add4025f41622dbc1985083a35bf5a676f1fa
多啦b梦|[发布]全新牛逼plus的 加入了自动更新|2a2a82a|2023-11-05 01:19|2a2a82a71dd177379147d51846f08804e11be9b8"""

    text = result

    # 作者|提交信息|段hash|时间|完整hash
    # 参数分割出来
    text = text.split('\n')
    result = []
    for i in text:
        i = i.split('|')
        if len(i) < 5:
            continue
        author = i[0]
        message = i[1]
        short_hash = i[2]
        date = i[3]
        full_hash = i[4]
        # 如果 message 为[发布] 则不添加LinkMsg
        linkMsg = f"""[{{author}} {{short_hash}}](https://github.com/{GITHUB_REPOSITORY}/commit/{{hash}}) {{date}}"""
        message = message + linkMsg.format(author=author, short_hash=short_hash, hash=full_hash, date=date)

        result.append(
            {'author': author, 'message': message, 'short_hash': short_hash, 'time': date, 'full_hash': full_hash})
    # 获取最后提交时间 和 第一条提交时间 计算相差多久 要好友的显示 比如 多少分钟,小时,天
    last_time = result[0]['time']
    first_time = result[-1]['time']

    用了多少时间 = calculate_time_difference(last_time,first_time)

    # 删除result数组的最后一个元素
    del result[-1]
    # print(result)

    # 获取 message 包含[]的内容 获取中括号的内容作为标签 [标签] 分类后
    # 内容格式
    # ### 新增
    # - message的内容
    # - message的内容
    # ### 修复
    # - message的内容
    # - message的内容

    最新发布信息 = ""
    result_group = {}
    for i in result:
        message = i['message']
        if message.startswith('[发布]'):
            最新发布信息 = message.replace('[发布]', '')
            continue

        tag = message.split('[')[1].split(']')[0]
        if tag not in result_group:
            result_group[tag] = []
        result_group[tag].append(message.replace(f'[{tag}]', ''))

    # 输出结果
    变更内容 = ""
    for tag, messages in result_group.items():
        变更内容 += f"### {tag}\n"
        for msg in messages:
            变更内容 += f"- {msg}\n"

    textTMP = f"""# GoEasyDesigner 窗口设计师

奋斗了{{用了多少时间}}，本次更新内容如下：

{{最新发布信息}}

{{变更内容}}"""
    textTMP = textTMP.format(用了多少时间=用了多少时间, 最新发布信息=最新发布信息, 变更内容=变更内容)
    print(textTMP)
    help.Github输出变量多行文本("Body",textTMP)