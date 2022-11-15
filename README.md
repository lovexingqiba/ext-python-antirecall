# ext-python-antirecall
基于ext框架的应用，可以监控指定群消息，把其它群成员撤回的消息转发保存
## 运行环境
* python3.8
* websocket-client 1.4.2
* ext框架 3.7.5.2
* 微信PC 3.7.5.23
* 其它版本请自行测试

## 使用方法
编辑config.py文件。  
chatroom_name_list：需要检测的微信群名称列表  
send_to_wxid：检测到撤回信息后，需要转发的好友id，留空则转发到对应群  
plugin_info：插件说明。插件启动后会发送到文件传输助手。  


