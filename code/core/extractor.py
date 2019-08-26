import sys
sys.path.append("..")  # 先跳出当前目录
from bean.word_unit import WordUnit
from bean.sentence_unit import SentenceUnit
from bean.entity_pair import EntityPair
from core.extract_by_dsnf import ExtractByDSNF

class Extractor:
    """抽取生成知识三元组
    Attributes:
        entities: WordUnit list，句子的实体列表
        entity_pairs: EntityPair WordUnit list，句子实体对列表
    """
    entities = []  # 存储该句子中的可能实体
    entity_pairs = []  # 存储该句子中(满足一定条件)的可能实体对

    def extract(self, origin_sentence, sentence, file_path, num):
        """
        Args:
            origin_sentence: string，原始句子
            sentence: SentenceUnit，句子单元
        Returns:
            num： 知识三元组的数量编号
        """
        self.get_entities(sentence)
        self.get_entity_pairs(sentence)
        for entity_pair in self.entity_pairs:
            entity1 = entity_pair.entity1
            entity2 = entity_pair.entity2

            extract_dsnf = ExtractByDSNF(origin_sentence, sentence, entity1, entity2, file_path, num)
            # [DSNF2|DSNF7]，部分覆盖[DSNF5|DSNF6]
            if extract_dsnf.SBV_VOB(entity1, entity2):
                pass
            # [DSNF4]
            if extract_dsnf.SBV_CMP_POB(entity1, entity2):
                pass
            if extract_dsnf.SBVorFOB_POB_VOB(entity1, entity2):
                pass
            # [DSNF1]
            # if not extract_dsnf.E_NN_E(entity1, entity2):
            #     pass
            # [DSNF3|DSNF5|DSNF6]，并列实体中的主谓宾可能会包含DSNF3
            if extract_dsnf.coordinate(entity1, entity2):
                pass
            # ["的"短语]
            if extract_dsnf.entity_de_entity_NNT(entity1, entity2):
                pass

            num = extract_dsnf.num
        return num

    def get_entities(self, sentence):
        """获取句子中的所有可能实体
        Args:
            sentence: SentenceUnit，句子单元
        Returns:
            None
        """
        self.entities.clear()  # 清空实体
        for word in sentence.words:
            if self.is_entity(word):
                self.entities.append(word)

    def get_entity_pairs(self, sentence):
        """组成实体对，限制实体对之间的实体数量不能超过4
        Args:
            sentence: SentenceUnit，句子单元
        """
        self.entity_pairs.clear()  # 清空实体对
        length = len(self.entities)
        i = 0
        while i < length:
            j = i + 1
            while j < length:
                if (self.entities[i].lemma != self.entities[j].lemma and 
                    self.get_entity_num_between(self.entities[i], self.entities[j], sentence) <= 4):
                    self.entity_pairs.append(EntityPair(self.entities[i], self.entities[j]))
                j += 1
            i += 1

    def is_entity(self, entry):
        """判断词单元是否实体
        Args:
            entry: WordUnit，词单元
        Returns:
            *: bool，实体(True)，非实体(False)
        """
        # 候选实体词性列表
        entity_postags = {'nh', 'ni', 'ns', 'nz', 'j'}
        if entry.postag in entity_postags:
            return True
        else:
            return False

    def get_entity_num_between(self, entity1, entity2, sentence):
        """获得两个实体之间的实体数量
        Args:
            entity1: WordUnit，实体1
            entity2: WordUnit，实体2
        Returns:
            num: int，两实体间的实体数量
        """
        num = 0
        i = entity1.ID + 1
        while i < entity2.ID:
            if self.is_entity(sentence.words[i]):
                num += 1
            i += 1
        return num

