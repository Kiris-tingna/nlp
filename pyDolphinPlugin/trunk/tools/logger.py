#-*- coding: UTF-8 -*-
'''
Created on 2016年12月21日

@author: ouyangyu
'''

import logging.handlers  

logger = logging.getLogger()  
logger.setLevel(logging.DEBUG)  

rht = logging.handlers.TimedRotatingFileHandler("dolphinPlugin.log", 'D')  
#fmt = logging.Formatter("%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")  
fmt = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")  
rht.setFormatter(fmt)  
logger.addHandler(rht)  
  
debug = logger.debug  
info = logger.info  
warning = logger.warn  
error = logger.error  
critical = logger.critical  