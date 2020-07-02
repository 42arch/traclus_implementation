## 关于

我的硕士毕业设计，基于Python 3.x实现了轨迹聚类算法，并开发了一个包含前后端程序的DEMO。代码写的有点乱，而且有很多要改进的地方，但是时间原因加上基本可以实现算法功能应付毕业，所以没怎么维护过。答辩已经完成了，就将所有代码公开出来吧。

## 使用

### 后端程序

进入`traclus_api`目录下，执行`pip install -r requirements.txt`安装相关依赖

执行`python manage.py runserver`启动算法计算服务

### 前端

直接进入`traclus_page/dist`目录下，浏览器打开`index.html`文件即可

或者在`traclus_page`目录下，执行`npm install`安装前端依赖，再执行`npm build`，然后在`dist`目录下找到`index.html`打开

### 测试数据

启动后端服务，并打开页面后，将测试数据文件夹下的`test_data.json`中的内容复制到原始数据输入框，并在参数输入框依次输入`参数.txt`中的指定参数，点击确定。

依次点击计算与显示框下的按钮，可以在地图上查看计算结果。

### 图

![原始数据](.\picture\1.png)

![轨迹分段](.\picture\2.PNG)

![轨迹聚类](.\picture\3.PNG)![代表性轨迹](.\picture\4.PNG)

## THANKS

