#!/usr/bin/env python
# encoding: utf-8

from mongokit import Document, Connection, ObjectId
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'eat2pay'


#多团队版本，需添加team，

#Member未来可以扩展个人信息字段，手机号、邮箱等。
class Member(Document):
    __database__ = MONGODB_DATABASE
    __collection__ = 'member'
    structure = {
        "member_id": unicode,
        "member_name": unicode,
        "member_balance": float
    }
    indexes = [
        {
            'fields': ['member_id'],
            'unique': True,
        }
    ]
    def find_one_by_member_id(self, member_id):
        return self.one({
            "member_id": member_id
        })

#Order保存订单公共基本信息，具体的每个[member-monoy-note]放在eater里面
class Order(Document):
    __database__ = MONGODB_DATABASE
    __collection__ = 'order'
    structure = {
        "total_money": unicode,
        "payer_id": unicode,
        "time": unicode
    }
    indexes = [
        {
            'fields': ['app_slug','uid'],
            'unique': True,
        }
    ]
    def find_one_by_app_id(self, app_id):
        return self.one({
            "app_id": app_id
        })

# 关于订单信息有误，回退及修改这个逻辑，暂时不做太复杂，由线下沟通，小二重新修改订单，不走系统。
# 具体的每个member的[member-monoy-note]
class Eater(Document):
    __database__ = MONGODB_DATABASE
    __collection__ = 'eater'
    structure = {
        "order_id": ObjectId,   #订单的ID，作为
        "member_id": unicode,
        "money": float,
        "note": unicode,        # 备注、留言，对话形式，未来订单未确认的回退修改反馈也在这里完成。
        "state": bool           # 订单状态：确认True，未确认False
    }
    def find_one_by_order_id(self, order_id):
        return self.one({
            "order_id": order_id
        })
    def find_one_by_member_id(self, member_id):
        return self.one({
            "member_id": member_id
        })

connection = Connection(host=MONGODB_HOST,port=MONGODB_PORT)
model_list = [Order, Member, Eater]
connection.register(model_list)
for m in model_list:
    collection = connection[m.__database__][m.__collection__]
    m.generate_index(collection)