# coding: utf-8
# __author__ = 'zhangguoze'

import sys
import jieba

from libshorttext.libshorttext.analyzer import *
from libshorttext.libshorttext.classifier import *
from libshorttext.libshorttext.converter import *

reload(sys)
sys.setdefaultencoding('utf-8')


def comma_tokenizer(text):
    return jieba.cut(text)

train_file = 'train_file.txt'
test_file = 'test_file.txt'
model_file = 'train_file.model'


def precision_recall(predict_result):
    label_dct = {}
    for idx, r in enumerate(predict_result.predicted_y):
        predicted_label = predict_result.predicted_y[idx]
        true_label = predict_result.true_y[idx]
        if predicted_label not in label_dct:
            label_dct[predicted_label] = [0, 0, 0]
        if true_label not in label_dct:
            label_dct[true_label] = [0, 0, 0]
        if predict_result.predicted_y[idx] == predict_result.true_y[idx]:
            label_dct[predicted_label][0] += 1
        label_dct[predicted_label][1] += 1
        label_dct[true_label][2] += 1
    accuracy_lst = []
    for key, val in label_dct.iteritems():
        accuracy_lst.append((key, float(val[0]) / val[1], float(val[0]) / val[2]))
    sorted_lst = sorted(accuracy_lst, key=lambda x: x[1])
    with open('precision_recall.txt', 'w') as f:
        for s in sorted_lst:
            f.write('%s\t%s\t%s\n' % (s[0], format(s[1], '.2%'), format(s[2], '.2%')))


def analyze_confusion(model, predict_result):
    analyzer = Analyzer(model)
    insts = InstanceSet(predict_result).select(wrong, with_labels(['sports', 'movie', 'star']))
    analyzer.gen_confusion_table(insts)


def analyze_single(model, single_text):
    analyzer = Analyzer(model)
    analyzer.analyze_single(single_text, output='features.txt')


def get_decvals(model, predict_result):
    tlst = zip(model.get_labels(), predict_result.decvals)
    tlst = sorted(tlst, key=lambda x: x[1])
    with open('decvals.txt', 'w') as f:
        for t in tlst:
            f.write('%s\t%s\n' % (t[0], t[1]))


def train():
    text_converter = Text2svmConverter()
    text_converter.text_prep.tokenizer = comma_tokenizer
    svm_file = 'train_file.svm'
    convert_text(train_file, text_converter, svm_file)
    liblinear_arguments = ''
    feature_arguments = ''
    model = train_converted_text(svm_file, text_converter, train_arguments=liblinear_arguments,
                                 feature_arguments=feature_arguments)
    predict_result = predict_text(test_file, model, svm_file='test_file.svm')
    print("Accuracy = {0:.4f}% ({1}/{2})".format(
        predict_result.get_accuracy() * 100,
        sum(ty == py for ty, py in zip(predict_result.true_y, predict_result.predicted_y)),
        len(predict_result.true_y)))


def test():
    model = TextModel()
    model.load(model_file)
    model.text_converter.text_prep.tokenizer = comma_tokenizer
    single_text = '阿森纳曝3200万报价巴萨飞翼已达协议 本周亲劝其加盟_2014世界杯_新浪体育'
    predict_result = predict_single_text(single_text, model)
    get_decvals(model, predict_result)
    analyze_single(model, single_text)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python lst_classifier.py [train/test]'
    cmd = sys.argv[1]
    locals()[cmd]()