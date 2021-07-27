## 关于

基于Python 3.7实现了轨迹聚类算法，并基于Flask和React开发了一个包含前后端程序的DEMO。

github: https://github.com/explosionsinthesky/TRACLUS_IMPLEMENTATION

## 使用

### 后端程序

进入`traclus-api`目录下，执行`pip install -r requirements.txt`安装相关依赖

执行`python manage.py runserver`启动算法计算服务

### 前端

直接进入`traclus-app/build`目录下，浏览器打开`index.html`文件即可

或者在`traclus-app`目录下，执行`yarn`安装依赖，再执行`yarn build`打包应用，然后在`build`目录下找到`index.html`打开

### 测试数据

启动后端服务，并打开页面后，点击操作框文件上传按钮上传测试数据文件夹下的`test_data.json`文件，并在参数输入框依次输入`参数.txt`中的指定参数或自行指定，点击确定提交参数。

再依次点击计算与显示框下的按钮，可以在地图上查看计算结果。

### 测试图

![原始数据](.\picture\1.png)

![轨迹分段](.\picture\2.PNG)

![轨迹聚类](.\picture\3.PNG)![代表性轨迹](.\picture\4.PNG)

## THANKS

https://github.com/apolcyn/traclus_impl

https://github.com/luborliu/TraClusAlgorithm

本项目参考了以上两个项目的代码。
