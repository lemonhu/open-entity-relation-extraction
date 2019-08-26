# import pynlpir
import jieba
from ctypes import c_char_p

from pyltp import SentenceSplitter, Postagger, NamedEntityRecognizer, Parser

import os

import sys
sys.path.append("..")  # 先跳出当前目录
from bean.word_unit import WordUnit
from bean.sentence_unit import SentenceUnit
from core.entity_combine import EntityCombine


class NLP:
    """进行自然语言处理，包括分词，词性标注，命名实体识别，依存句法分析
    Attributes:
        default_user_dict_dir: str，用户自定义词典目录
        default_model_dir: str，ltp模型文件目录
    """
    default_user_dict_dir = '../../resource/'  # 默认的用户词典目录，清华大学法律词典
    default_model_dir = '../../model/'  # ltp模型文件目录
    
    def __init__(self, user_dict_dir=default_user_dict_dir, model_dir=default_model_dir):
        self.default_user_dict_dir = user_dict_dir
        self.default_model_dir = model_dir
        # 初始化分词器
        # pynlpir.open()  # 初始化分词器
        # 添加用户词典(法律文书大辞典与清华大学法律词典)，这种方式是添加进内存中，速度更快
        files = os.listdir(user_dict_dir)
        for file in files:
            file_path = os.path.join(user_dict_dir, file)
            # 文件夹则跳过
            if os.path.isdir(file):
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                    word = line.strip('\n').strip()
                    jieba.add_word(word)
                    # print(c_char_p(word.encode()))
                    # pynlpir.nlpir.AddUserWord(c_char_p(word.encode()))
                    line = f.readline()

        # 加载ltp模型
        # 词性标注模型
        self.postagger = Postagger()
        postag_flag = self.postagger.load(os.path.join(self.default_model_dir, 'pos.model'))
        # 命名实体识别模型
        self.recognizer = NamedEntityRecognizer()
        ner_flag = self.recognizer.load(os.path.join(self.default_model_dir, 'ner.model'))
        # 依存句法分析模型
        self.parser = Parser()
        parse_flag = self.parser.load(os.path.join(self.default_model_dir, 'parser.model'))

        if postag_flag or ner_flag or parse_flag:
            print('load model failed!')

    def segment(self, sentence, entity_postag=dict()):
        """采用NLPIR进行分词处理
        Args:
            sentence: string，句子
            entity_postag: dict，实体词性词典，默认为空集合，分析每一个案例的结构化文本时产生
        Returns:
            lemmas: list，分词结果
        """
        # 添加实体词典
        if entity_postag:
            for entity in entity_postag:
                # pynlpir.nlpir.AddUserWord(c_char_p(entity.encode()))
                jieba.add_word(entity)
        # pynlpir.nlpir.AddUserWord(c_char_p('前任'.encode()))  # 单个用户词加入示例
        # pynlpir.nlpir.AddUserWord(c_char_p('习近平'.encode()))  # 单个用户词加入示例
        # 分词，不进行词性标注
        # lemmas = pynlpir.segment(sentence, pos_tagging=False)
        lemmas = jieba.lcut(sentence)
        # pynlpir.close()  # 释放
        return lemmas

    def postag(self, lemmas):
        """对分词后的结果进行词性标注
        Args:
            lemmas: list，分词后的结果
            entity_dict: set，实体词典，处理具体的一则判决书的结构化文本时产生
        Returns:
            words: WordUnit list，包含分词与词性标注结果
        """
        words = []  # 存储句子处理后的词单元
        # 词性标注
        postags = self.postagger.postag(lemmas)
        for i in range(len(lemmas)):
            # 存储分词与词性标记后的词单元WordUnit，编号从1开始
            word = WordUnit(i+1, lemmas[i], postags[i])
            words.append(word)
        # self.postagger.release()  # 释放
        return words

    def get_postag(self, word):
        """获得单个词的词性标注
        Args:
            word: str，单词
        Returns:
            post_tag: str，该单词的词性标注
        """
        post_tag = self.postagger.postag([word, ])
        return post_tag[0]

    def netag(self, words):
        """命名实体识别，并对分词与词性标注后的结果进行命名实体识别与合并
        Args:
            words: WordUnit list，包含分词与词性标注结果
        Returns:
            words_netag: WordUnit list，包含分词，词性标注与命名实体识别结果
        """
        lemmas = []  # 存储分词后的结果
        postags = []  # 存储词性标书结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 命名实体识别
        netags = self.recognizer.recognize(lemmas, postags)
        # print('\t'.join(netags))  # just for test
        words_netag = EntityCombine().combine(words, netags)
        # self.recognizer.release()  # 释放
        return words_netag

    def parse(self, words):
        """对分词，词性标注与命名实体识别后的结果进行依存句法分析(命名实体识别可选)
        Args:
            words_netag: WordUnit list，包含分词，词性标注与命名实体识别结果
        Returns:
            *: SentenceUnit，该句子单元
        """
        lemmas = []  # 分词结果
        postags = []  # 词性标注结果
        for word in words:
            lemmas.append(word.lemma)
            postags.append(word.postag)
        # 依存句法分析
        arcs = self.parser.parse(lemmas, postags)
        for i in range(len(arcs)):
            words[i].head = arcs[i].head
            words[i].dependency = arcs[i].relation
        # self.parser.release()
        return SentenceUnit(words)

    def close(self):
        """关闭与释放nlp"""
        # pynlpir.close()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()


if __name__ == '__main__':
    nlp = NLP()
    # 分词测试
    print('***' + '分词测试' + '***')
    # sentence = '国家主席习近平视察中国福建厦门。'
    sentence = '奥巴马毕业于哈弗大学'
    lemmas = nlp.segment(sentence)
    # 输出：['国家主席', '习近平', '视察', '中国', '福建', '厦门', '。']
    print(lemmas)
    
    # 词性标注测试
    print('***' + '词性标注测试' + '***')
    words = nlp.postag(lemmas)
    for word in words:
        print(word.to_string())

    print('"中国"的词性: ' + nlp.get_postag('中国'))

    # 命名实体识别与合并测试
    print('***' + '命名实体识别测试' + '***')
    # 合并后的分词结果变为：['国家主席', '习近平', '视察', '中国福建厦门', '。']
    words_netag = nlp.netag(words)
    for word in words_netag:
        print(word.to_string())

    # 依存句法分析测试
    print('***' + '依存句法分析测试' + '***')
    sentence = nlp.parse(words_netag)
    print(sentence.to_string())
    print('sentence head: ' + sentence.words[0].head_word.lemma)
    
