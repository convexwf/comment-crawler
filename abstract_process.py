#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from passage import *

class abstract():
    def __init__(self, pid):
        self.pid = pid
        self.sid_set = []
        self.sentence_set = {}
        self.sentence_cost = {}
        self.sentence_voc = {}
        self.vocabulary_dict = {}

    def pre_process(self):
        sentences = Passage.get_sentence_by_pid(self.pid)
        self.sid_set = [item['sentence_id'] for item in sentences]
        _sentence_set = [item['comment'] for item in sentences]
        _sentence_cost = [item['cost'] for item in sentences]
        for index in range(len(self.sid_set)):
            self.sentence_set[self.sid_set[index]] = _sentence_set[index]
            self.sentence_cost[self.sid_set[index]] = _sentence_cost[index]
            self.sentence_voc[self.sid_set[index]] = Passage.get_vocabulary_by_sid(self.sid_set[index])

        vocabularys = Passage.get_vocabulary_by_pid(self.pid)
        for voc in vocabularys:
            self.vocabulary_dict[voc['vocabulary_id']] = voc['TF_IDF']


    def greedy(self, cost_Length):
        value_dict = self.vocabulary_dict.copy()
        R = self.sid_set.copy()
        G = []
        while len(R) > 0:
            si = self.get_maximum(R, value_dict)
            R.remove(si)
            if self.get_cost(G + [si]) <= cost_Length:
                G.append(si)
                self.re_evaluate(value_dict, si)
        return G

    def get_maximum(self, R, value_dict):
        maximum = 0.0
        result_sid = -1
        for sid in R:
            value = self.get_value(value_dict, self.sentence_voc[sid])
            cost = self.sentence_cost[sid]
            if value/cost >= maximum:
                maximum = value/cost
                result_sid = sid
        print('maximum', result_sid, len(R))
        return result_sid

    def re_evaluate(self, value_dict, sid, flag = True):
        for i in self.sentence_voc[sid]:
            vid = i['vocabulary_id']
            value_dict[vid] = 0 if flag else self.vocabulary_dict[vid]


    def get_value(self, value_dict, sen_voc):
        value = 0.0
        for x in sen_voc:
            id = x['vocabulary_id']
            cnt = x['count']
            value += value_dict[id] * cnt
        return value

    def get_cost(self, sid_list):
        cost = 0.0
        for sid in sid_list:
            cost += self.sentence_cost[sid]
        return cost


if __name__ == '__main__':
    #print(Passage.get_pid(0, 10))
    ab = abstract(7968811)
    ab.pre_process()
    result = ab.greedy(100)
    for x in result:
        print(ab.sentence_set[x])
