# -*- coding: utf-8 -*-

import os

input_path = '../../resource/THUOCL_law.txt'  # 清华大学开放中文词库(法律)
output_path = '../../resource/THUOCL_law_lexicon.txt'  # 存储处理后的词典文件


def get_lexicon(input_path, output_path,):
    """获得符合要求的法律词典
    Args:
        input_path: string, 待处理词典文件
        output_path: string, 存储处理后的词典文件
    """
    words = ''
    with open(input_path, 'r', encoding='utf-8') as fin, \
        open(output_path, 'a', encoding='utf-8') as fout:

        for line in fin:
            seg = line.strip('\r\n').split('\t')
            word = seg[0]
            words += word + '\n'

        fout.write(words)
        fout.flush()
        fin.close()
        fout.close()

if __name__ == '__main__':
    # 删除已存在的词典文件并重新创建
    if os.path.exists(output_path) and os.path.isfile(output_path):
        os.remove(output_path)
        # os.mknod(output_path)

    get_lexicon(input_path, output_path)
