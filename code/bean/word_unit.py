class WordUnit:
    """词单元组成"""
    # 定义类变量
    # 当前词在句子中的序号，1开始
    ID = 0
    # 当前词语的原型(或标点)，就是切分后的一个词
    lemma = ''
    # 当前词语的词性
    postag = ''
    # 当前词语的中心词，及当前词的头部词
    head = 0  # 指向词的ID
    head_word = None # 该中心词单元
    # 当前词语与中心词的依存关系
    dependency = '' # 每个词都有指向自己的唯一依存

    def __init__(self, ID, lemma, postag, head=0, head_word=None, dependency=''):
        self.ID = ID
        self.lemma = lemma
        self.postag = postag
        self.head = head
        self.head_word = head_word
        self.dependency = dependency

    def get_id(self):
        return self.ID
    def set_id(self, ID):
        self.ID = ID

    def get_lemma(self):
        return self.lemma
    def set_lemma(self, lemma):
        self.lemma = lemma

    def get_postag(self):
        return self.postag
    def set_postag(self, postag):
        self.postag = postag

    def get_head(self):
        return self.head
    def set_head(self, head):
        self.head = head

    def get_head_word(self):
        return self.head_word
    def set_head_word(self, head_word):
        self.head_word = head_word

    def get_dependency(self):
        return self.dependency
    def set_dependency(self, dependency):
        self.dependency = dependency

    def to_string(self):
        """将word的相关处理结果转成字符串，tab键间隔
        Returns:
            word_str: str，转换后的字符串
        """
        word_str = ''
        word_str += (str(self.ID) + '\t' + self.lemma + '\t' + self.postag + '\t' +
                    str(self.head) + '\t' + self.dependency)
        return word_str


if __name__ == '__main__':
    # 中国首都北京
    word3 = WordUnit(3, '北京', 'ns', 0, None, 'HED')
    word2 = WordUnit(2, '首都', 'ns', 3, word3, 'ATT')
    word1 = WordUnit(1, '中国', 'ns', 2, word2, 'ATT')

    print(word1.lemma + '\t' + word1.postag)
    print(word2.lemma + '\t' + word2.head_word.lemma)
    print(word3.get_lemma() + '\t' + word3.get_postag())

    print(word1.to_string())
    print(word2.to_string())
    print(word3.to_string())

