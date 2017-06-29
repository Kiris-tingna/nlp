#-*- coding: UTF-8 -*-
'''
Created on 2016年12月15日

@author: ouyangyu
'''
import hashlib
from tools import ToSGW
import traceback
import json
import Listener
import tools.logger as Log

class SessionFactory(object):
    '''
    创建会话
    '''
    def __init__(self, token):
        '''
        Constructor
        '''
        self.listeners   = {};
        self.service_SGW = "http://114.55.90.150:5600/v2/message";
        self.token       = token;
        pass
    
    def addListener(self, userid, clientid, listener, forced=False):
        '''
        创建一个监听器
        userid: 用户id
        clientid: 用户使用的设备id
        listener: 监听对象, see Listener对象
        forced: 是否强制增加监听器, true强制增加, false当监听器存在的时候返回false
        return ture 增加监听器成功, false 增加监听器失败
        '''
        name = self.generateName(userid, clientid); #计算监听器名称
        
        #判断监听器是否已经存在
        if self.listeners.has_key(name) and not forced:
            return False;
        
        self.listeners[name] = listener;
        return True;
    
    def delListener(self, userid, clientid, resetSession):
        name = self.generateName(userid, clientid); #计算监听器名称
        if self.listeners.has_key(name):
            del self.listeners[name];
        if resetSession: self.resetSession(userid, clientid);
        
        pass
    
    def resetSession(self, userid, clientid):
        sgw = ToSGW.ToSGW();
        sgw.resetSession(self.token, userid, clientid);
        pass  
    
    def generateName(self, userid, clientid):
        return hashlib.md5(userid + "-" + clientid).hexdigest().upper(); #计算监听器名称
    
    def existListener(self, userid, clientid):
        return self.listeners.has_key(self.generateName(userid, clientid));
    
    def dailog(self, userid, clientid, text):
        '''
        执行对话，userid和clientid共同构成一个会话。
        userid: 用户id
        clientid: 用户使用的设备id
        text: 待语义解析的文本串
        返回显示给客户端的字符串...
        '''
        name     = self.generateName(userid, clientid);
        sgw      = ToSGW.ToSGW();
        
        listener = None;
        if self.listeners.has_key(name): listener = self.listeners[name];

        try:
            if listener != None:
                if not listener.onSendToDolphin(userid, clientid, text):
                    Log.info('中止解析...');
                    self.delListener(userid, clientid, True); #执行删除...
                    return None;
            
            #将用户上行数据送引擎
            r = sgw.semantic2(self.token,  #token
                    userid,   #用户id唯一,用发送方帐号（一个OpenID）代替
                    clientid, #设备id
                    text,     #用户消息
                    True);
            if r == None: raise  Exception("解析%s失败..."%text);
            
            Log.info('analyse result:%s'%json.dumps(r, sort_keys=True, indent=4));
            
            if r['analyse_type'] == 'event':
                return self.operEvents(userid, clientid, r['events']); #operEvents返回的是Result对象
            elif r["analyse_type"] == 'only_qa':
                #命中的是自动问答
                return self.operSophinQA(userid, clientid, r['sophi_qa']);
            elif r["analyse_type"] == 'interactive': 
                #命中交互
                return self.operInquiry(userid, clientid, r['inquiry']);
            elif r["analyse_type"] == 'page': 
                return self.operTuling(userid, clientid, r['pageinfo']);
            elif r["analyse_type"] == 'text':
                return self.operTuling(userid, clientid, {'tip':r['textinfo'],'url':''});
            else:
                raise  Exception("未知的分析结果:%s"%r['analyse_type']);
        except:
            traceback.print_exc();
        return '抱歉，我不懂 "'+text+'" 的意思...';
    
    def operTuling(self, userid, clientid, tuling):
        name = self.generateName(userid, clientid);
        
        listener = None;
        if self.listeners.has_key(name): listener = self.listeners[name];

        r=json.dumps(tuling, sort_keys=True, indent=4);
        if listener != None: r=listener.doEcho(userid, clientid, tuling);
        
        self.resetSession(userid, clientid);
        return r;
    
    def operInquiry(self, userid, clientid, inquiry):
        name = self.generateName(userid, clientid);
        
        listener = None;
        if self.listeners.has_key(name): listener = self.listeners[name];
            
        r = json.dumps(inquiry, sort_keys=True, indent=4);            
        if listener != None: r = listener.doAsk(userid, clientid, inquiry);
         
        return r;
    
    def operSophinQA(self, userid, clientid, qs):
        name = self.generateName(userid, clientid);

        listener = None;
        if self.listeners.has_key(name): listener = self.listeners[name];
        
        #命中的是自动问答
        rsv = 0.00;
        str = "";
        for q in qs:
            if q['rsv'] - rsv > 0.001:
                rsv = q['rsv'];
                str = q['answer']; #q['question'] + '\n' + q['answer']
            pass
        
        r = json.dumps(qs);
        if listener != None: r= listener.doEcho(qs, userid, clientid, str);

        self.resetSession(userid, clientid); #自动问答结束无需重置会话...
        return r;
    
    def operEvents(self, userid, clientid, events):
        name = self.generateName(userid, clientid);
        
        listener = None;
        if self.listeners.has_key(name): listener = self.listeners[name];

        if len(events) > 1:
            Log.warning("收到了从引擎返回的多个语义事件:%s，目前只处理第一个语义事件!"%json.dumps(events));
        elif len(events) == 0:
            Log.error('引擎无语义事件返回');
            return None;
        
        r = json.dumps(events[0]);
        if listener != None: r = listener.doEvent(userid, clientid, events[0]);

        self.resetSession(userid, clientid); #语义事件完成后执行重置会话...
        return r;
    