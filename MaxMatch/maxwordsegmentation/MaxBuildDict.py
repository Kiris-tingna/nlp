# -*- coding: cp936 -*-
# ���ƥ�䷨���зִ�----�����ʱ��ļ�.
# author ����
# date 2013/3/23
import string
import re


# ����:���Ͽ�199801.txt�ļ�; ���:���зָ��Ĵʱ��ļ�dict.txt(�Ѿ�ȥ�ظ�, ȥ����)
def create_dict(filename):
    print("��ȡ�ļ�......")
    src_data = open(filename, 'r', encoding='utf-8').read()
    sp_data = src_data.split()  # �ָ�

    print("ԭʼ����Ϊ:", len(sp_data))
    set_data = set(sp_data)  # ȥ�ظ�
    data = list(set_data)  # setת����list, ����������
    print("ȥ���ظ����ܴ���Ϊ:", len(data))

    print("���ڽ����ʱ��ļ�......")
    tmp = []
    for i in range(0, len(data)):
        print(data[i])
        # ȥ�����������Ĵ�'19980101-01-001-002/m'
        if re.compile(r'\d+\-\S+').match(data[i]):
            continue
        else:
            # �����ƵĴ�'������/ns'�滻Ϊ'������'
            p_ok_data = re.compile(r'\/\w+').sub('\n', data[i])
            # �ҵ���'['��']'��ͷ�Ĵ�
            if re.compile(r'(\[\S+)|(\]\S+)').match(p_ok_data):
                # ȥ��']nt[����',']����','[����'����ʵ�ͷ�����ò���(��ƥ�䳤�Ĳ���)
                ok_data = re.compile(r'(\]\w+\[)|(\])|(\[)').sub('\n', p_ok_data)
                tmp.append(ok_data)
                continue
        print(p_ok_data)
        tmp.append(p_ok_data)

    print("���յõ��Ĵʱ��ļ����ܴ���Ϊ:", len(tmp))
    open('dict_tmp.txt', 'w', encoding='utf8').writelines(tmp)
    print("�����ʱ��ļ��������! (dict_tmp.txt)")


# ����
if __name__ == '__main__':
    create_dict('199801.txt')
