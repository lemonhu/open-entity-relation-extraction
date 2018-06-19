# -*- coding: utf-8 -*-

import json
from py2neo import Graph, Node, Relationship, NodeSelector

import sys
sys.path.append("..")  # 先跳出当前目录
from core.nlp import NLP

class WriteToNeo4j:
    """将Json类型的知识三元组导入Neo4j数据库"""
    def __init__(self, triple_path):
        self.entity_set = set()  # 实体节点集合
        self.nlp = NLP()
        # 连接neo4j数据库
        self.graph = Graph(host='localhost',
                      http_port=7474,
                      user='neo4j',
                      password='123456')
        f_in  = open(triple_path, 'r')
        triple_str = f_in.read()  # 读取整个Json
        self.triple = json.loads(triple_str)

    def write_litigant(self, litigants, relation):
        """处理当事人信息(原告和原告)
        Args:
            litigant: list，当事人信息
        """
        for litigant in litigants:
            node_litigant = Node(self.get_label(litigant['名字']), name=litigant['名字'], id=litigant['编号'])
            self.graph.create(node_litigant)
            self.entity_set.add(litigant['名字'])
            node_root = self.graph.find_one('判决书', property_key='name', property_value='判决书001')
            entity_relation = Relationship(node_root, relation, node_litigant, label='relation')
            self.graph.create(entity_relation)

            for item in litigant:
                if item != '名字' and item != '编号':
                    node_repr = Node(self.get_label(litigant[item]), name=litigant[item])  # 负责人，委托代理人
                    self.graph.create(node_repr)
                    self.entity_set.add(litigant[item])
                    entity_relation = Relationship(node_litigant, item, node_repr, label='关系')
                    self.graph.create(entity_relation)

    def get_label(self, word):
        """根据单词获得标签
        Args:
            word: str，单词
        Returns:
            label: str，类型标签
        """
        label = ''
        postag = self.nlp.get_postag(word)
        if postag == 'nh':
            label = '人'
        elif postag == 'ni':
            label = '组织'
        elif postag == 'ns':
            label = '地点'
        else:
            label = '其他'
        return label

    def write(self):
        """写入图数据库"""
        # 根节点
        # 一篇判决书具有"文书编号"，"文书标题"，"按键编号"，"文书类型"，"案件编号"几个属性
        node_root = Node('判决书', name='判决书001', id=self.triple['文书编号'], title=self.triple['文书标题'], type=self.triple['文书类型'], case=self.triple['案件编号'])
        self.graph.create(node_root)
        self.entity_set.add('判决书001')
        node_court = Node('组织', name=self.triple['受理法院'])
        self.graph.create(node_court)
        self.entity_set.add(self.triple['受理法院'])

        entity_rerlation = Relationship(node_root, '受理法院', node_court, label='关系')
        self.graph.create(entity_rerlation)

        # 遍历原告，被告
        plaintiffs = self.triple['原告']
        self.write_litigant(plaintiffs, '原告')
        defendants = self.triple['被告']
        self.write_litigant(defendants, '被告')

        facts = self.triple['案情事实']
        for fact in facts:
            tri = fact['知识']
            entity1 = tri[0]
            relation = tri[1]
            entity2 = tri[2]

            node_list = []
            node1 = Node(self.get_label(entity1), name=entity1)
            if entity1 not in self.entity_set:
                self.graph.create(node1)
                node_list.append(node1)
                self.entity_set.add(entity1)
            else:
                node_list.append(self.graph.find_one(self.get_label(entity1), property_key='name', property_value=entity1))

            node2 = Node(self.get_label(entity2), name=entity2)
            if entity2 not in self.entity_set:
                self.graph.create(node2)
                node_list.append(node2)
                self.entity_set.add(entity2)
            else:
                node_list.append(self.graph.find_one(self.get_label(entity2), property_key='name', property_value=entity2))

            entity_relation = Relationship(node_list[0], relation, node_list[1], label='关系')
            self.graph.create(entity_relation)

