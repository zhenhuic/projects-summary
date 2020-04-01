# Angle Detection
This is a program used to detect the angle of the picture.

### 检测程序主要流程
1. 获取工件长度
2. 等待拍照
3. 拍照检测
4. 检测结果保存在数据库(数据库分为两个部分：mysql(我们自己的数据库)和sql server(楼上用来展示的数据))
5. 一轮结束重新开始步骤 1-4

### 程序主界面
![main window printscreen](main%20window%20printscreen.png)

### 程序运行方式

* 方式一：双击运行 start(或start.bat) 文件，点击界面窗口上方三角播放按钮开始检测；
* 方式二：命令行键入`python angle_start.py`(angle_start.py 即是程序入口), 点击界面窗口上方三角播放按钮开始检测。
