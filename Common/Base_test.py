import unittest
import requests
import json
from Logs.log import log1
import getcwd
import os
import configparser

path = getcwd.get_cwd()
config_path = os.path.join(path, 'Config/config.ini')


class webrequests(unittest.TestCase):

    def get(self, url, params=None, headers=None, files=None):
        '''封装get方法，return响应码和响应内容'''
        try:
            r = requests.get(url, params=params, headers=headers, files=files, timeout=300)
            log1.info("请求的内容：%s" % params)
            status_code = r.status_code  # 获取返回的状态码
            log1.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            log1.info("响应内容：%s" % response_json)
            return status_code, response_json  # 返回响应码，响应内容
        except BaseException as e:
            log1.error("请求失败！", exc_info=1)

    def post(self, url, data=None, headers=None, files=None):
        '''封装post请求，return响应码和响应内容'''
        try:
            r = requests.post(url, data=data, headers=headers, files=files, timeout=300)
            log1.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            log1.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            log1.info("响应内容：%s" % response_json)
            return status_code, response_json  # 返回响应码，响应内容
        except BaseException as e:
            log1.error("请求失败！", exc_info=1)

    def post_json(self, url, data=None, headers=None):
        '''封装post方法，并用json格式传值，return响应码和响应内容'''
        try:
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')  # python数据类型转化为json数据类型
            r = requests.post(url, data=data, headers=headers, timeout=300)
            log1.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            log1.info("获取返回的状态码:%d" % status_code)
            response = r.json()  # 响应内容，json类型转化成python数据类型
            log1.info("响应内容：%s" % response)
            return status_code, response  # 返回响应码，响应内容
        except BaseException as e:
            log1.error("请求失败！", exc_info=1)

    def getdict(self, dict1, obj, default=None):
        ''' 遍历嵌套字典，得到想要的value
            dict1所需遍历的字典
            obj 所需value的键'''
        for k, v in dict1.items():
            if k == obj:
                return v
            else:
                if type(v) is dict:
                    re = self.getdict(v, obj, default)  # 递归
                    if re is not default:
                        return re

    def confige_get(self, section, key, url=None):
        '''读取配置文件字段的值并返回'''
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        if key == 'url':
            config_url = config.get(section, key)
            url = config_url + url
            log1.info("请求的url：%s" % url)
            return url
        else:
            config_get = config.get(section, key)
            return config_get

    def config_write(self, section, key=None, value=None):
        '''往配置文件写入键值'''
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        if key is not None and value is not None:
            config.set(section, key, value)
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)
        else:
            config.add_section(section)
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)

    def config_delete(self, section, key=None):
        '''删除配置文件字段'''
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        if key is not None:
            config.remove_option(section, key)
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)
        else:
            config.remove_section(section)
            with open(config_path, 'w', encoding='utf-8')as f:
                config.write(f)

    def confige_options(self, section):
        '''读取配置文件某section下所有键'''
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8-sig")
        username = config.options(section)
        return username

    def get_addkey(self, user):
        '''遍历获得配置文件收件人email'''
        sum = 0
        L = []
        for i in user:
            if sum < len(user):
                emails = self.confige_get('addressed', i)
                L.append(emails)
                sum += 1
        return L
