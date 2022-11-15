import json
import config
import os
import re
import base64


class AntiRecall:
    def __init__(self, uri):
        self.uri = uri
        self.send_to_wxid = None
        self.atid = None
        self.ws = None

    @staticmethod
    def __reg_get_newmsg_id(str_msg):
        pattern = re.compile(r'\<newmsgid\>(\d+)\<\/newmsgid\>')
        m = pattern.search(str_msg)
        return m.group(1)

    @staticmethod
    def __base64str_to_image(base64_str):
        img_data = base64.b64decode(base64_str)
        save_name = 'dat_saved.jpg'
        with open(save_name, 'wb') as f:
            f.write(img_data)
        return os.path.abspath(save_name)

    # 解析getfile_Recv类型的消息
    def analyse_getfile_recv(self, msg):
        if msg['method'] == 'getfile_Recv':
            img_file = self.__base64str_to_image(msg['base64'])
            p = {
                'method': 'sendImage',
                'wxid': self.send_to_wxid,
                'img': img_file,
                'imgType': 'file',
                'pid': 0
            }
            self.ws.send(json.dumps(p))

    # 解析getMsg_Recv类型的消息
    def analyse_getmsg_recv(self, msg):
        # 暂时只处理文字和图片消息
        if msg['method'] == 'getMsg_Recv':
            msg_type = msg['data'][0]['type']
            if msg_type in ['1', '3']:
                self.send_to_wxid = config.send_to_wxid if config.send_to_wxid else msg['data'][0]['fromid']
                self.atid = msg['data'][0]['memid']
                if msg_type == "1":
                    # 文本消息
                    reply_msg = '撤回了一条文字消息\n========\n'
                    reply_msg += msg['data'][0]['msg']
                    p = {
                        'method': 'sendText',
                        'wxid': self.send_to_wxid,
                        'msg': reply_msg,
                        'atid': self.atid,
                        'pid': 0
                    }
                    self.ws.send(json.dumps(p))
                elif msg_type == '3':
                    # 图片消息
                    p = {
                        'method': 'sendText',
                        'wxid': self.send_to_wxid,
                        'msg': '撤回了一条图片消息',
                        'atid': self.atid,
                        'pid': 0
                    }
                    self.ws.send(json.dumps(p))
                    img_dat = msg['data'][0]['ext1']
                    p = {'method': 'getfile', 'path': img_dat}
                    self.ws.send(json.dumps(p))

    def on_message(self, ws, message):
        # print(message)
        self.ws = ws
        msg = json.loads(message)
        self.analyse_getmsg_recv(msg)
        self.analyse_getfile_recv(msg)
        # 处理撤回消息
        if msg['method'] == 'newmsg' \
                and msg['type'] == 10002 \
                and '撤回了一条消息' in msg['data']['msg'] \
                and msg['data'].get('memid'):
            chatroom_name = msg['data']['nickName']
            if chatroom_name in config.chatroom_name_list:
                # 通过主动获取消息的接口，获取被撤回消息的详细内容
                p = {"method": "getMsg", "type": 1, "sid": str(self.__reg_get_newmsg_id(msg['data']['msg']))}
                self.ws.send(json.dumps(p))

    def on_open(self, ws):
        self.ws = ws
        plugin_info = config.plugin_info
        p = {'method': 'sendText',
             'wxid': 'filehelper',
             'msg': plugin_info,
             'pid': 0}
        self.ws.send(json.dumps(p))
