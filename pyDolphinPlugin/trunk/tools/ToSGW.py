#-*- coding: UTF-8 -*-
'''
Created on 2016年12月19日

@author: ouyangyu
'''
import json
import time
import httplib
import sys
import urlparse
import tools.logger as Log

class ToSGW(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        用于实现STT本地语义交互的语义解析接口
        接口采用的是语义网关的《知言语义分析接口协议2.0》
        {
            respcode: 响应码 int， 0表示成功, 其余表示失败
            reqtext:  对应请求的语言文本 string
            token:    对应请求的token
            analyse_result: { //语义分析结果
            analyse_type: 分析结果类型 string, event 表示返回的是事件, interactive 表示进入交互逻辑, text 文本结果, page 网页
            events: 命中的语义事件 [], 仅在analyse_type=event有效
                [
                    {
                        name: 语义事件名称 string
                        inputs: { //输入参数
                            <参数名称>: {
                                type: 类型 string, text表示文本, number表示数量, datetime表示日期时间
                                val: {
                                    根据不同type，val存在下面三种格式:
                                    type = text时,   text: 字符串值 string
                                    type = number时, from.val: 起始值, from.unit: 起始值单位, to.unit: 截止值, to.unit: 截止值单位
                                    type = datetime时, from.begin: 开始时间起始点, from.end: 开始时间截止点, to.begin: 截止时间开始点, to.end: 截止时间截止点
                                }
                            },
                            ...
                        }
                        outputs: [ //输出参数
                            保留
                        ]
                        caption: 触发语义事件的自然语句
                    }
                ],
                inquiry: 询问或提示信息 {}, 仅在analyse_type=interactive有效,
                textinfo: 直接显示在人机界面上的文字信息 string, 仅在analyse_type=text有效,
                pageinfo: 返回一个url链接，指向某个结果页面 {tip: 提示信息 string, url: 指向某个结果页面的链接 string}, 仅在analyse_type=page有效,
                <p>
            }
        }
        '''
        self.service_smanticAnalyse = "http://114.55.90.150:5600/v2/message";
        self.service_resetSession   = "http://114.55.90.150:5600/v2/message/closesession?v=1&p=2";
        pass
    
    def httpSend(self, method, service, msg):
        headers = {"Content-type": "application/x-www-form-urlencoded"};
        Log.info("send to %s:%s"%(service, msg));
        
        params  = json.dumps(msg);
        #print params;
        
        u=urlparse.urlsplit(service); #返回地址元组: 0:协议, 1:远端地址和端口, 2:服务路径
        #print u;
          
        conn = httplib.HTTPConnection(u[1]);
        if method == "POST":
            path = u[2];
            if u[3] != '': path = u[2] + "?" + u[3];
            conn.request(method, path, params, headers);
            r = conn.getresponse(); #r.status, r.reason
            if r.status != 200:
                Log.error('error:' + r.reason);
                return '';
        elif method == "GET":
            conn.request(method, u[2], params, headers);
            pass
        else:
            Log.error('unknow method:'+method);
            return '';

        
        data = r.read();
        conn.close();
        
        return data;

    def analyze(self, token, userid, clientid, reqtext, interactive):
        o = {};
        o["reqtime"] = int(time.time());
        o["access_token"]  = token;
        o["user_id"]       = userid;
        o["client_id"]     = clientid;
        o["reqtext"]       = reqtext;
        o["enable_interactive"] = str(interactive);
        o["enable_verify"] = "false";
        o["comm_key_id"]   = "";
        o["verify_sum"]    = "";
        o["action"]        = "text";

        return self.httpSend("POST", self.service_smanticAnalyse, o);
    
    def semantic2(self, token, userid, clientid, text, interactive=True):
        rcvmsg = self.analyze(token, userid, clientid, text, interactive);
        #print "analyze result:"+rcvmsg;
        o = json.loads(rcvmsg);
        if o.has_key("respcode") and o["respcode"] != 0:
            Log.error("解析失败：%s"%o["message"].encode("utf8"));
            return None;
        return o["analyse_result"];
    
    def resetSession(self, token, userid, clientid):
        o = {};
        o["reqtime"] = int(time.time());
        o["access_token"] = token;
        o["user_id"] = userid;
        o["client_id"] = clientid;
        o["enable_verify"] = "false";
        o["comm_key_id"] = "";
        o["verify_sum"] = "";

        rcvmsg = self.httpSend("POST", self.service_resetSession, o);
        return rcvmsg;