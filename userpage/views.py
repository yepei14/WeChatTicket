from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User

import urllib

import http.cookiejar

class UserBind(APIView):

    def validate_user(self):
        student_id = self.input['student_id']
        password = self.input['password']
        hosturl = 'http://learn.tsinghua.edu.cn/'
        posturl = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
        cj = http.cookiejar.CookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(cookie_support)
        urllib.request.install_opener(opener)
        urllib.request.urlopen(hosturl)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Referer': 'http://learn.tsinghua.edu.cn/index.jsp'
        }
        postData = {
            'userid': student_id,
            'userpass': password,
        }
        postData = urllib.parse.urlencode(postData).encode('utf-8')
        request = urllib.request.Request(posturl, postData, headers)
        response = urllib.request.urlopen(request)
        if response.read().decode('utf-8').find('loginteacher_action.jsp') == -1:
            raise NotImplementedError('You should implement UserBind.validate_user method')
        else:
            return 0

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()
