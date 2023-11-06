# 自动生成发布日志适用于简单的软件提交记录

自动统计所有的提交记录 最新一次[发布] 和上一次之间的内容

例如下面的提交记录

[发布]xxxx
[新增]某一个功能
[修复Bug]引起异常
[修复Bug]引起异常
[新增]第二个功能
[优化]加快运行速度

最终汇总变成版本发布日志

```
name: test_auto_tags

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  jobs_v:
    name: 构建版本号和变更信息
    runs-on: ubuntu-latest
    outputs:
      NewVersion: ${{ steps.create_version.outputs.NewVersion }} 
      Body: ${{ steps.create_body.outputs.Body }} 
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      - name: 检查是否 "发布"
        run: |
          echo "New Body: ${{ steps.jobs_v.outputs.newBody }}"
          
          latest_commit_message=$(git log -1 --pretty=%B)
          if [[ $latest_commit_message == *"发布"* ]]; then
            echo "找到发布关键字继续工作流"
          else
            echo "没有找到发布关键字停止工作流"
            exit 1  # 停止工作流程
          fi
      - name: 递增版本号
        id: create_version
        uses: duolabmeng6/action-autotag-python@master
        with:
          token: ${{ secrets.GITHUB_TOKEN }}


      - name: 获取更新日志
        id: create_body
        uses: duolabmeng6/action-Releases-log@main
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FILE: .github/releasesText.md
          KEYS: bug,改进,优化,新增,删除

      - name: 查看版本号和更新日志
        run: |
          echo ${{ format('version={0}', steps.create_version.outputs.NewVersion ) }}
          echo "${{ steps.create_body.outputs.Body }}"
          echo "${{ steps.releasesText.outputs.releasesText }}"

      - name: 发布文件
        uses: ncipollo/release-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          allowUpdates: true # 覆盖文件
          #draft: true # 草稿 自己可见 版本号会保持一样 默认是自动发布 latest
          #prerelease: true # 预发布 别人可以看到 版本号会继续加
          tag: ${{ steps.create_version.outputs.NewVersion }} # 版本号 v0.1.0
          body: ${{ steps.create_body.outputs.Body }}
          artifacts: "macos/*.zip,macos/*.dmg,window/*.exe,window/*.zip"


```

```
      - name: 获取更新日志
        id: create_body
        uses: duolabmeng6/action-Releases-log@main
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FILE: .github/releasesText.md
          KEYS: bug,改进,优化,新增,删除
```

FILE内容是

```
# GoEasyDesigner 窗口设计师

奋斗了{{用了多少时间}}，本次更新内容如下：

{{最新发布信息}}

{{变更内容}}
```

KEYS 用逗号分割 用作分组的关键字 检查到关键字就作为标签加入 这样子方便输入
同时 提交中出现 [标签] 中括号包含的也会100%作为标签 以便想在更新记录加入新标签的时候要修改脚本 这样子直接兼容


