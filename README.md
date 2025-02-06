##  简介

Alice Engine（v0.1）是一个文字游戏引擎，旨在让游戏开发者简便地开发属于自己的文字游戏。引擎使用python语言开发，操作简单，新手可轻松上手。

## 使用方式

在进行开发前，请确认是否已经安装好了引擎所需的python库（tkinter、queue）
将上述三个文件置于同一目录，再在同一目录下新建一个文件“script.as”，使用记事本打开，就可以在里面编写脚本了。
Alice Engine引擎运行的基本单位是节点（Point)，节点分属着各自的选项（Choice），选项再链接到各自的节点。
当游戏开始时，游戏画面会显示此时的节点文本，下面会列出一系列选项。当玩家点击一个选项后，游戏会跳转到选项所对应的节点。
引擎使用如下的语法定义一个节点：

`{节点文本...`
`#选项一...`
`#选项二...`
`#...`
`}`

其中，换行和缩进是可选的，合适的换行和缩进可以让脚本文件更具可读性。
而选项的语法为：

`\#选项名
{对应的节点...
}`

最后，不要忘记在脚本文件的开头加上游戏名。
设置游戏名的格式为：

`游戏名&`

以下为一个script.as脚本文件示例：
`#script.as`
`新游戏&`
`{这是文本A`
`#选项一`
`    {这是文本B`
`    #选项二`
`    }`
`#选项三`
`}`
游戏运行后，效果如下：
![d2ViXzMwMDFfNzU4MTg5OV8wXzE3Mzg3Nzg4NTYyNTBfNDNlNjBjYzg](https://github.com/user-attachments/assets/a84f1a88-648a-453a-8b80-2fad4ac434df)
点击“选项一”后，会显示：
![d2ViXzMwMDFfNzU4MTg5OV8wXzE3Mzg3Nzg4OTMwMzJfNjEzOTA2YjU](https://github.com/user-attachments/assets/c1cc9519-00e8-4e44-acb0-48ae9c8d4fe5)

## 未来开发计划

未来的更新方向可能包括：
1.使游戏文本的大小、字体和颜色可以被开发者调整。
2.引入定义和使用变量、条件判断等操作。
