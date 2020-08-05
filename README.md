# Raspberry_demo

#### 介绍
基于树莓派的智能箱包

#### 软件架构
文件名|内容说明
:-:|:-:
autosh.sh|自动运行脚本
change_GPS.py|GPS坐标转换
crthtml|生成HMML测试文件
getGPSinfoByUart.py|串口方式获取GPS信息
getGPSinfoByUSB|USB接口获取GPS信息
inquiry-with-rssi.py|获取蓝牙信号强度
MarkPoint.html|定位标记网页
msmtprc|邮箱配置信息
sendmail.py|发送邮件测试文件
webio.py|网页IO控制测试文件

#### 使用说明
##### 1.换源，更新
编辑软件源文件
`sudo nano /etc/apt/source.list`

替换内容为
```
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free
deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free
```

编辑系统更新源文件
`sudo nano /etc/apt/sources.list.d/raspi.list`

替换内容为:
`deb http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/ stretch main ui`

安装输入法
`sudo apt-get install fcitx fcitx-googlepinyin fcitx-module-cloudpinyin fcitx-sunpinyin`

安装完毕，重启树莓派
##### 2.安装pybluez
`git clone https://github.com/karulis/pybluez`

`sudo python setup.py build`

`sudo python setup.py install`

##### 3.安装GPS库
`sudo apt-get install gpsd gpsd-clients python-gps`

##### 4.安装yagmail
`pip install yagmail`

##### 5.安装蓝牙驱动与A2DP支持
蓝牙驱动
`sudo apt-get install pi-bluetooth bluez bluez-firmware blueman`   

`sudo usermod -G bluetooth -a pi `    

`sudo systemctl start bluetooth`     

`sudo reboot`

A2DP支持
`git clone https://github.com/bareinhard/super-simple-raspberry-pi-audio-receiver-install`     

`cd super-simple-raspberry-pi-audio-receiver-install`     

`git checkout stretch-fix`     

`sudo ./install.sh`     

`（1）Car和Home，我选的Home`     

`（2）Device name和AirPlay Device Name，写PiMusic`     

`（3）密码，不输入`     

`（4）Do you want all the Devices to use the same name? (y/n) : Choose y or n，选n`     

`（5）Which Sound Card are you using? (0/1/2/3/4/5/6/7/8/9/10/11)，写0`
##### 6.安装webiopi
`git clone https://github.com/thortex/rpi3-webiopi`     

`cd rpi3-webiopi/webiopi_0.7.1`     

`sudo ./setup.sh`

修改密码：

`sudo webiopi-passwd`

启动webiopi     

`sudo webiopi 8000`     

让webopio后台运行，否则按ctarl+c就会断掉     

`sudo /etc/init.d/webiopi start`     

设置webopio随系统启动     

`sudo update-rc.d webiopi defaults`

登陆网址：树莓派IP:8000    

用户名：webiopi     

默认密码：raspberry