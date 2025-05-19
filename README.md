# Django 项目

## 项目简介
这是一个使用Django 5.2.1开发的Web应用项目。

## 环境要求
- Python 3.x
- Django 5.2.1

## 安装步骤
1. 克隆项目到本地
```bash
git clone [你的项目仓库地址]

# 有用资源
- 1.pythonanywhere
- 2.dj4e.com
- 3.https://www.obeythetestinggoat.com/pages/book.html
- 4.https://programming-24.mooc.fi/
- 5.https://learn.deeplearning.ai/

# 要点
- 1.记录一些要点，以后整理成一开源书。
- 2.非专业开发者，利用Trae，开发一个帮助自己学习外语的网站。部署在pythonanywhere上，配置了域名zzlearnzz.com。 
- 3.用测试驱动的方式开发。
- 4.似乎很难找到一个真实的，用django5开发的例子。
- 5.思考如何形成原子网络，留住用户3分钟以上。
- 6.用户为工具而来，为网络而留。
- 7.可以增加积分功能，增加用户之间的互动功能。
- 8.学习日历功能。记录用户每天学了什么。
- 9.语音博客。
- 10.每个new feature完成后，就tag一个新的版本。v1,v2,v3....(initial 可以tag为v0)
- 11.先添加什么feature好呢，还是从MVP开始吧。我的这个APP，最小可用的提供什么功能呢。我自己用这个APP，最小的可以的功能是什么。
- 12.最核心的是，学习的本质是测试。也就是要提供某种形式的测试，使得我能学习外语。
- 13.配置在pythonanywhere是，wsgi.py是位于/var下面的，而不是项目里面的那个。
- 14.今晚似乎有点不想做。那你做个开头也可以啊。甚至稍微起个头也好啊。
- 15.还是不行。是不是因为我的项目名称包含下划线。zzlearnzz_site，与其有冲突啊。/var/www/www_my_domain_com_wsgi.py。重新创建一个不包括下划线的项目试试。
- 16.没道理不行的啊。你应该像个侦探一样，从蛛丝马迹中，找到答案。/
- 17.教程里，为何是path = os.path.expanduser('~/django_projects/mysite')；不应该是'~/lienxiong/django_projects/mysite'吗？但是确实，前者才可行啊。
- 18.you're going to https://webapp-xxxxxx.pythonanywhere.com directly in your browser, that will always give you a "Coming soon" page. Basically the webapp-xxxxx... domain is just an identifier for the load-balancer associated with your web app. om a terminal/command prompt on your local machine: ping webapp-XXXXXX.pythonanywhere.com
Open your hosts file, which is /etc/hosts on Linux or OS X, or c:\Windows\system32\drivers\etc 
- 19.你现在的部署流程是，你git clone https://github.com/lizkca/zzlearnzz_site.git，然后当你增加新的功能后，你就rm -rf zzlearnzz_site ，再重新git clone https://github.com/lizkca/zzlearnzz_site.git。那么，当真的有用户的时候，那你删去就的目录，会不会对用户已有的数据造成影响。该如何解决这个问题呢。
- 20.问AI，如何写一个好的prompt
- 21.编写一个好的 Prompt是与AI 高效交互的关键。一个好的 Prompt 能够引导 AI 更准确、更有效地理解你的意图，并生成期望的输出。以下是一些编写优秀 Prompt 的技巧和最佳实践：

    - 1. 清晰具体 (Clear and Specific) ：
       - 明确你的目标 ：在写 Prompt 之前，先想清楚你希望 AI 完成什么任务，得到什么样的结果。
       - 使用精确的语言 ：避免模糊不清或有歧义的词汇。越具体，AI 理解得越好。
       - 提供足够的细节 ：如果任务复杂，确保给出所有必要的细节。例如，不要只说“写一个故事”，而是说“写一个关于一只勇敢的小猫在魔法森林中寻找丢失的铃铛的短篇奇幻故事，目标读者是儿童”。
    - 2. 提供上下文 (Provide Context) ：
       - 背景信息 ：如果你的请求与特定背景相关，请提供这些背景信息。
       - 相关知识 ：如果 AI 需要某些特定领域的知识才能完成任务，可以简要提及或提供关键信息。
    - 3. 设定角色 (Assign a Role) ：
       - 告诉 AI 它应该扮演什么角色。例如：“你是一位经验丰富的旅行规划师，请帮我规划一次为期七天的日本东京家庭旅行。” 或者 “你是一位专业的 Python 程序员，请帮我审查以下代码并指出潜在的 bug。”
       - 角色设定有助于 AI 调整其回答的语气、风格和专业程度。
    - 4. 指定输出格式 (Specify Output Format) ：
       - 明确你希望输出的格式，例如：列表、段落、JSON、代码块、表格、邮件格式等。
       - 示例：“请用无序列表的形式列出五个提高工作效率的方法。”
   - 5. 给出示例 (Provide Examples - Few-shot Prompting) ：
       - 对于复杂的或需要特定风格的任务，提供一两个输入和期望输出的示例，AI 可以从中学习模式。
       - 示例：
         我：将英文翻译成法文。
         sea otter -> loutre de mer
         peppermint -> menthe poivrée
         cheese -> ?
         AI：fromage
    - 6. 使用约束和指令 (Use Constraints and Instructions) ：
       - 正面指令 ：明确告诉 AI 要做什么 。
       - 负面指令 (可选，但有时有用)：明确告诉 AI 不要做什么 。例如，“不要使用俚语”，“答案长度不要超过 200 字”。
       - 步骤指引 ：对于多步骤任务，可以引导 AI 按步骤思考或输出。
    - 7. 迭代和优化 (Iterate and Refine) ：
       - 很少有 Prompt 第一次就能完美工作。尝试不同的措辞、增加或减少细节、调整指令，看看哪种效果最好。
       - 分析 AI 的不理想输出来改进你的 Prompt。
    - 8. 控制长度和复杂度 (Manage Length and Complexity) ：
       - 简洁明了 ：尽量让 Prompt 简洁，避免不必要的冗余信息。
       - 分解任务 ：如果任务非常复杂，可以将其分解成几个更小、更简单的子任务，分别用不同的 Prompt 来处理。
    - 9. 明确语气和风格 (Define Tone and Style) ：
       - 如果你对输出的语气有要求（例如：正式、非正式、幽默、严肃），请在 Prompt 中说明。
    - 10. 使用分隔符 (Use Delimiters) ：
        - 当 Prompt 中包含不同部分的信息（如指令、上下文、输入数据）时，使用清晰的分隔符（如三重引号 """ """ ，XML 标签 <tag></tag> ，或者简单的标记如 上下文： , 指令： ）可以帮助 AI 更好地区分它们。
    一个好的 Prompt 结构示例：
    角色：你是一位资深的营销文案撰写人。
    任务：为一款名为“ChronoWatch X”的新型智能手表撰写一段吸引人的产品描述。
    目标受众：热爱科技、注重健康和时尚的年轻专业人士。
    核心卖点：
    1.  超长续航（7天）
    2.  精准健康监测（心率、睡眠、血氧）
    3.  时尚简约设计，多种表带可选
    4.  高清AMOLED触摸屏
    5.  智能通知和快捷回复
    要求：
    - 语气：现代、积极、略带科技感。
    - 长度：150-200字。
    - 格式：一段式描述。
    - 避免：使用过于夸张或不实的宣传语。
    请开始撰写。
记住，编写 Prompt 是一门艺术，也是一门科学，多加练习和尝试是提高的关键
- 22.智能体给出的路径有误。直接告诉它，结果也能调整正确。
- 23.忘了，要先编写测试，再实现功能。
- 24.用AI编程，还是要看一下。你有时候会发现一些很明显，很离谱，很幼稚的错误。相对于，你完全不看，只是按AI生成的东西用上去。你会发现后者更好，因为把这些错误一排除，你觉得用AI编程，挺完美的。
- 25.可以面对面，介绍，推销。（例如，美国的国家公园，你要用英语介绍）
- 26.编写测试和不编写测试大不一样啊。有时候，你让AI编写了个测试，然后运行测试，就会报错。然后，你根据运行测试的结果反馈给AI，它就修改得比较好。你没让AI编写测试，然后运行看结果，有时候，反而没那么容易找到问题的所在的。
- 27.突然可以了，是因为确实要这么长时间吗，还是因为我更新系统，重启了一遍电脑呢。
- 28.虽然，我在浏览器上输入www.zzlearnzz.com会自动跳转到zzlearnzz.com。但是，我还是得在浏览器中输入www.zzlearnzz.com，不然就上不了。




