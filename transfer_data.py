#!/usr/bin/env python3
# coding: utf-8
# File: transfer_data.py


import os

class TransferData:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])  #获取当前文件地址的上级目录
        #对分类进行标记
        self.label_dict = {
                      '检查和检验': 'CHECK',
                      '症状和体征': 'SIGNS',
                      '疾病和诊断': 'DISEASE',
                      '治疗': 'TREATMENT',
                      '身体部位': 'BODY'}

        self.origin_path = os.path.join(cur, 'data_origin')  #原始数据地址
        self.train_filepath = os.path.join(cur, 'train.txt') #转化后的训练数据地址
        return


    def transfer(self):
        f = open(self.train_filepath, 'w+',encoding='utf-8')   #以写入的方式打开训练数据要保存的文件
        count = 0
        for root,dirs,files in os.walk(self.origin_path):
        #for (root, dirs, files) in walk(roots)：
        # roots代表需要遍历的根文件夹；
        # root表示正在遍历的文件夹的名字（根/子）；
        # dirs记录正在遍历的文件夹下的子文件夹集合；
        # files记录正在遍历的文件夹中的文件集合
            for file in files:
                filepath = os.path.join(root, file)
                if 'original' not in filepath:
                    continue
                label_filepath = filepath.replace('.txtoriginal','')
                print(filepath, '\t\t', label_filepath)  #data_origin\一般项目\一般项目-1.txtoriginal.txt 	data_origin\一般项目\一般项目-1.txt
                content = open(filepath,encoding='utf-8').read().strip()  #打开案例描述文件，去掉收尾空格
                res_dict = {}
                for line in open(label_filepath,encoding='utf-8'):  #打开实体类别文件
                    res = line.strip().split('	')  #每个实体描述按空格分隔 ['右髋部'，‘21’，‘23’，‘身体部位’]
                    start = int(res[1])  #实体的其实字符位置
                    end = int(res[2])  #实体的结束字符位置
                    label = res[3]  #实体类别
                    label_id = self.label_dict.get(label)   #返回分类字典中实体类别对应的values，作为实体名称的id
                    for i in range(start, end+1):
                        if i == start:
                            label_cate = label_id + '-B'  #定义实体的首字符
                        else:
                            label_cate = label_id + '-I'  #实体的非首字符
                        res_dict[i] = label_cate   #构建实体字典{位置index:字符}

                for indx, char in enumerate(content):  #indx文本中字符的位置，char字符
                    char_label = res_dict.get(indx, 'O')  #如果indx在字典的key中，则返回字典value；否则返回O，代表非实体
                    print(char, char_label)   #字符：字符实体标注
                    f.write(char + '\t' + char_label + '\n')
        f.close()
        return



if __name__ == '__main__':
    handler = TransferData()
    train_datas = handler.transfer()