#-*- coding: UTF-8 -*-
'''
Created on 2016年12月18日

@author: ouyangyu
'''
import tools.logger as Log;
import json
                
class Listener(object):
    '''
    监听器
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def onSendToDolphin(self, userid, clientid, msg):
        '''
        插件在发送给解析引擎之前，会调用本方法。通过这个方法开发者可以决定是否插入一些处理，并决定是否继续解析。
        响应Result对象, see Result
        '''
        Log.info("call Listener onSendToDolphin:%s/%s-%s"%(userid, clientid, msg));

        return True; #False 中止解析, True 继续解析
    
    def doEvent(self, userid, clientid, event):
        '''
        引擎准确解析出语义事件后，会通过这个方法回调给开发者处理。开发者可以利用这个方法执行语义事件，并将语义事件响应的结果返回给客户
        响应Result对象, see Result
        '''
        Log.info("call Listener doEvent:%s/%s-%s"%(userid, clientid, json.dumps(event, sort_keys=True, indent=4)));
        
        return json.dumps(event, sort_keys=True, indent=4).encode('utf-8');
    
    def doAsk(self, userid, clientid, msg):
        '''
        引擎因为存在歧义，必要参数缺失时，会触发这个调用，开发者可以决定是否启用个性化的对话提示
        响应Result对象, see Result
        '''
        Log.info("call Listener doAsk:%s/%s-%s"%(userid, clientid, json.dumps(msg, sort_keys=True, indent=4)));
                
        optionstr = '';
        options   = msg['options'];
        for option in options:
            if optionstr != '': optionstr = optionstr + '\n';
                
            optiontext = option['option_text'].replace(',', '');
            optionstr = optionstr + str(option['seqno']);
            optionstr = optionstr + '. ';
            optionstr = optionstr + optiontext.split("(")[0]
            pass
            
        head_text = msg['head_text'];
        tail_text = '';
        if options!=None and len(options) > 1: head_text = "似乎存在%d种选择"%len(options);
            
        if msg.has_key('tail_text'): tail_text =msg['tail_text'];
        #print '%s-%s-%s'%(head_text, tail_text.encode('utf8'), optionstr.encode('utf8'))
        return  head_text + '\n' + tail_text.encode('utf8') + '\n' + optionstr.encode('utf8');
    
    def doEcho(self, userid, clientid, msg):
        '''
        通常在自动问答时，引擎会触发这个调用
        响应Result对象, see Result
        '''
        Log.info("call doEcho:%s"%msg);
        
        vvv = msg["tip"];
        if msg.has_key("url"): vvv = vvv + ":" + msg["url"];
        
        return vvv;