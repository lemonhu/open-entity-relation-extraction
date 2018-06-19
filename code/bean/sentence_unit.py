import sys
sys.path.append("..")  # 先跳出当前目录
from bean.word_unit import WordUnit

class SentenceUnit:
    """句子单元组成，每行为一个词单元，并获得每个词头部的词单元
    Attributes:
        words: WordUnit list，词单元列表
    """
    words = None
    def __init__(self, words):
        self.words = words
        for i in range(len(words)):
            self.words[i].head_word = self.get_word_by_id(self.words[i].head)
        
    def get_word_by_id(self, id):
        """根据id获得词单元word
        Args:
            id: int，词单元ID
        Returns:
            word: 词单元
        """
        for word in self.words:
            if word.ID == id:
                return word
        return None

    def get_head_word(self):
        """获得整个句子的中心词单元
        Returns:
            head_word: WordUnit，中心词单元
        """
        for word in self.words:
            if word.head == 0:
                return word
        return None

    def to_string(self):
        """将一句中包含的word转成字符串，词单元之间换行
        Returns:
            words_str: str，转换后的字符串
        """
        words_str = ''
        for word in self.words:
            words_str += word.to_string() + '\n'
        return words_str.rstrip('\n')

    def get_lemmas(self):
        """获得句子的分词结果
        Returns:
            lemmas: str，该句子的分词结果
        """
        lemmas = ''
        for word in self.words:
            lemmas += word.lemma + '\t'
        return lemmas.rstrip('\t')

if __name__ == '__main__':
    # 中国首都北京
    word3 = WordUnit(3, '北京', 'ns', 0, None, 'HED')
    word2 = WordUnit(2, '首都', 'ns', 3, None, 'ATT')
    word1 = WordUnit(1, '中国', 'ns', 2, None, 'ATT')

    words = []  # 句子的词单元
    words.append(word1)
    words.append(word2)
    words.append(word3)

    sentence = SentenceUnit(words)
    print(sentence.to_string())
    
    print('句子分词结果: ' + sentence.get_lemmas())
    print('"首都"的中心词lemma: ' + sentence.words[1].head_word.lemma)

    print('句子的中心词: ' + sentence.get_head_word().to_string())

