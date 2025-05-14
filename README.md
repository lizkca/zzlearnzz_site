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





