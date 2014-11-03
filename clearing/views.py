#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
from . import clearing
from flask import request, jsonify, g, current_app
from .models import Member, Order, Eater, connection
from mongokit import ObjectId

import time


@clearing.route('/<member>/xiaoer/', methods=['GET'])
def index(member):
    return clearing.send_static_file('index.html')


@clearing.route('/<member>/xiaoer/add_order/')
def show(member):
    member = member

    return clearing.send_static_file('show.html')










@clearing.route('/<member>/profile/', methods=['GET'])
def get_profile(member):
    profile = connection.clearing.find_one_by_app_and_uid(member,uid)
    if profile is None:
        return jsonify({'note':'member not found'})
    params= {'link': profile['link'], 'size': profile['size'], 'number': profile['number'],
             'content_visible': profile['content_visible']}
    return jsonify({'params':params})

@clearing.route('/<member>/profile/', methods=['POST'])
def set_profile(member):
    user = get_current_user()
    uid = user["_id"]
    params=request.json
    if not params:
        return jsonify({'note':u'error:receive no json params'})
    if int(params['number'])>20:
        return jsonify({'note':u'error: num cannot be bigger than 20'})
    profile = connection.clearing.find_one_by_app_and_uid(member,uid)
    if profile is None:
        return jsonify({'note':u'member not found'})
    for k in params:
        profile[k]=params[k]
    profile.save()
    return jsonify({'note':u'ok'})



@clearing.route('/get/<to_user_name>/<from_user_name>/<site>/<num>/xml')
def xml(site, to_user_name, from_user_name, num):
    new_xml = ET.Element('xml')
    tun = ET.SubElement(new_xml, 'ToUserName')
    tun.text = '<![CDATA[%s]]>' % to_user_name
    fun = ET.SubElement(new_xml, 'FromUserName')
    fun.text = '<![CDATA[%s]]>' % from_user_name
    ct = ET.SubElement(new_xml, 'CreateTime')
    ct.text = '<![CDATA[%s]]>' % str(int(time.time()))
    mt = ET.SubElement(new_xml, 'MsgType')
    mt.text = '<![CDATA[%s]]>' % 'news'
    ac = ET.SubElement(new_xml, 'ArticleCount')
    ac.text = num
    articles = ET.SubElement(new_xml, 'Articles')
    data = urllib2.urlopen('http://' + site + '.clearing.com/api/read').read()
    tree = ET.fromstring(data)
    a = tree.find('posts').findall('post')
    for index, i in enumerate(a):
        if index == (int(num)):
            break
        # for pic in i:
        # if pic.get('max-width') == '500':
        # p = pic.text
        item = ET.SubElement(articles, 'item')
        # title = ET.SubElement(item, 'Title')
        # title.text = '<![CDATA[%s]]>' % i.find('photo-caption').text
        # description = ET.SubElement(item, 'Description')
        # description.text = '<![CDATA[%s]]>' % i.find('description').text
        picurl = ET.SubElement(item, 'PicUrl')
        picurl.text = '<![CDATA[%s]]>' % i.findall('photo-url')[1].text
        url = ET.SubElement(item, 'Url')
        url.text = '<![CDATA[%s]]>' % i.get('url')
    return Response(ET.tostring(new_xml), mimetype='application/xml')
