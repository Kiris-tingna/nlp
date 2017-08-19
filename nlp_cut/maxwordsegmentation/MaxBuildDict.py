# -*- coding: cp936 -*-
# 最大匹配法进行分词----创建词表文件.
# author 徐能
# date 2013/3/23
import string
import re


# 输入:语料库199801.txt文件; 输出:换行分割后的词表文件dict.txt(已经去重复, 去日期)
def create_dict(filename):
    print("读取文件......")
    src_data = open(filename, 'r', encoding='utf-8').read()
    sp_data = src_data.split()  # 分割

    print("原始词数为:", len(sp_data))
    set_data = set(sp_data)  # 去重复
    data = list(set_data)  # set转换成list, 否则不能索引
    print("去除重复后总词数为:", len(data))

    print("正在建立词表文件......")
    tmp = []
    for i in range(0, len(data)):
        print(data[i])
        # 去除类似这样的词'19980101-01-001-002/m'
        if re.compile(r'\d+\-\S+').match(data[i]):
            continue
        else:
            # 将类似的词'埃特纳/ns'替换为'埃特纳'
            p_ok_data = re.compile(r'\/\w+').sub('\n', data[i])
            # 找到以'['或']'开头的词
            if re.compile(r'(\[\S+)|(\]\S+)').match(p_ok_data):
                # 去除']nt[澳门',']澳门','[澳门'三类词的头部无用部分(先匹配长的部分)
                ok_data = re.compile(r'(\]\w+\[)|(\])|(\[)').sub('\n', p_ok_data)
                tmp.append(ok_data)
                continue
        print(p_ok_data)
        tmp.append(p_ok_data)

    print("最终得到的词表文件中总词数为:", len(tmp))
    open('dict_tmp.txt', 'w', encoding='utf8').writelines(tmp)
    print("初步词表文件建立完成! (dict_tmp.txt)")


# 运行
if __name__ == '__main__':
    create_dict('199801.txt')
