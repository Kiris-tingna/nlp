#-*- coding: UTF-8 -*-
'''
Created on 2016年12月22日

@author: ouyangyu
'''

from session import SessionFactory;
from session import Listener;

if __name__ == '__main__':
    session = SessionFactory.SessionFactory('6B0BE4C6947F8A632AC55AF2FD44C505');
    listener = Listener.Listener();
    session.addListener("matrix", "wechat", listener, False);
    
    while True:
        str  = raw_input("Enter your input: ");
        if str == None or str == '': break;
        
        r = session.dailog("matrix", "wechat", str);
        if r != None:
            print "result:",r; 
        else:
            print '不能正确解析...'
    session.delListener('matrix', 'wechat', True);