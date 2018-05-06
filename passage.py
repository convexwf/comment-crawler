#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import mysql.connector

class Passage():
    # __tablename__ = 'passage'
    # passage_id = Column(VARCHAR(16), primary_key=True)
    # author = Column(VARCHAR(30), nullable=False)
    # star = Column(VARCHAR(5), nullable=False)
    # issueTime = Column(DateTime(), nullable=False)
    # title = Column(text, nullable=False)
    # comment = Column(text, nullable=False)
    # useful = Column(Integer, nullable=False)
    # unuseful = Column(Integer, nullable=False)
    # reply = Column(Integer, default=0)

    @staticmethod
    def execute_proc(pid, sen, voc):
        #print(passage_dict)
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306, database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        # 插入一行记录，注意MySQL的占位符是%s:
        try:
            cursor.execute('call Auto_update(%s,%s,%s)',
                           [pid, sen, voc])
        except Exception as e:
            print(e)
        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()

    @staticmethod
    def insert(passage_dict):
        #print(passage_dict)
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306, database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        if passage_dict['useful'] == '':
            passage_dict['useful'] = '0'
        if passage_dict['unuseful'] == '':
            passage_dict['unuseful'] = '0'
        if passage_dict['reply'] == '':
            passage_dict['reply'] = '0'
        # 插入一行记录，注意MySQL的占位符是%s:
        try:
            cursor.execute('insert into passage (passage_id, author, star, issueTime, title, comment, useful, unuseful, reply) '
                           'values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           [passage_dict['passage_id'],
                            passage_dict['author'],
                            passage_dict['star'],
                            passage_dict['issueTime'],
                            passage_dict['title'],
                            passage_dict['comment'],
                            int(passage_dict['useful']),
                            int(passage_dict['unuseful']),
                            int(passage_dict['reply'])])
        except mysql.connector.errors.IntegrityError:
            pass
        except Exception as e:
            print(e)
        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()

    @staticmethod
    def select(start, num):
        item_list = []
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select * from passage order by useful DESC, reply DESC, unuseful DESC, passage_id ASC limit %s, %s' % (start, num)
        cursor.execute(sql)
        for each in cursor.fetchall():
            item = {}
            item['passage_id'] = each[0]
            item['author'] = each[1]
            item['star'] = each[2]
            item['issueTime'] = each[3]
            item['title'] = each[4]
            item['comment'] = each[5]
            item['useful'] = each[6]
            item['unuseful'] = each[7]
            item['reply'] = each[8]
            item_list.append(item)



        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
        return item_list

    @staticmethod
    def get_pid(start, num):
        item_list = []
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select distinct passage_id from TF_IDF order by passage_id limit %s, %s' % (start, num)
        cursor.execute(sql)
        for each in cursor.fetchall():
            item = {}
            item['passage_id'] = each[0]
            item_list.append(item)
        return item_list


        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
        return item_list

    @staticmethod
    def get_sentence_by_pid(pid):
        item_list = []
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select * from sentence where passage_id=%s' % (pid)
        cursor.execute(sql)
        for each in cursor.fetchall():
            item = {}
            item['sentence_id'] = each[0]
            item['comment'] = each[2]
            item['cost'] = float(each[3])
            item_list.append(item)
        return item_list

        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
        return item_list

    @staticmethod
    def get_vocabulary_by_pid(pid):
        item_list = []
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select * from TF_IDF where passage_id=%s' % (pid)
        cursor.execute(sql)
        for each in cursor.fetchall():
            item = {}
            item['vocabulary_id'] = each[1]
            item['TF_IDF'] = float(each[2]) * float(each[3])
            item_list.append(item)
        return item_list

        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
        return item_list

    @staticmethod
    def get_vocabulary_by_sid(sid):
        item_list = []
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select * from map where sentence_id=%s' % (sid)
        cursor.execute(sql)
        for each in cursor.fetchall():
            item = {}
            item['vocabulary_id'] = each[1]
            item['count'] = each[2]
            item_list.append(item)
        return item_list

        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()
        return item_list

class Sentence():
    # __tablename__ = 'passage'
    # passage_id = Column(VARCHAR(16), primary_key=True)
    # author = Column(VARCHAR(30), nullable=False)
    # star = Column(VARCHAR(5), nullable=False)
    # issueTime = Column(DateTime(), nullable=False)
    # title = Column(text, nullable=False)
    # comment = Column(text, nullable=False)
    # useful = Column(Integer, nullable=False)
    # unuseful = Column(Integer, nullable=False)
    # reply = Column(Integer, default=0)

    @staticmethod
    def insert(sentence_dict):
        #print(passage_dict)
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306, database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        # 插入一行记录，注意MySQL的占位符是%s:
        try:
            cursor.execute('insert into sentence (passage_id, comment) '
                           'values (%s, %s)',
                           [sentence_dict['passage_id'],
                            sentence_dict['comment']])
        except mysql.connector.errors.IntegrityError:
            pass
        except Exception as e:
            print(e)
        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()

class Vocabulrary():
    @staticmethod
    def insert(vocabulary_dict):
        # print(passage_dict)
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        # 插入一行记录，注意MySQL的占位符是%s:
        try:
            cursor.execute('insert into vocabulary(comment) '
                           'values (%s)',
                           [vocabulary_dict['comment']])
        except mysql.connector.errors.IntegrityError:
            pass
        except Exception as e:
            print(e)
        # 提交事务:
        conn.commit()
        # 关闭Cursor和Connection:
        cursor.close()
        conn.close()

    @staticmethod
    def select(vocabulary_dict):
        conn = mysql.connector.connect(user='root', password='root', host='110.64.69.104', port=3306,
                                       database='BigFish_Comment', charset='utf8')
        cursor = conn.cursor()
        sql = 'select * from vocabulary where comment = %s' % (vocabulary_dict['comment'])
        cursor.execute(sql)
        item = {}
        for each in cursor.fetchall():
            item['vocabulary_id'] = each[0]
            item['comment'] = each[1]
        return item

if __name__ == '__main__':
    #Sentence.insert({'passage_id':'7904416','comment': '刚刚'})
    print(Passage.select(100, 10))
