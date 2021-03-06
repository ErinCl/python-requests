import unittest
from Logs.log import log1
from Common.Base_test import webrequests

class weather(unittest.TestCase):

    def test_weather(self):
        '''查询天气'''
        case_name = '查询天气'
        log1.info("执行测试用例：%s" % case_name)
        try:
            weather = webrequests()
            url = weather.confige_get('test','url',url='')
            # payloda = {'city':'上海'}
            status_code,response_json =weather.get(url,params='')
            message = weather.getdict(response_json,'message')
            test1 = self.assertEqual(status_code,200)
            test2 = self.assertEqual(message,'Success !')
            if test1 == None and test2 ==None:
                log1.info("测试通过")
        except BaseException as f :
            log1.error("测试用例执行出错: %s" % case_name,exc_info=1)
            raise