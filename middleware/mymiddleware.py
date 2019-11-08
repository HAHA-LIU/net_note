from django.http import HttpResponseRedirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMW(MiddlewareMixin):
    def process_request(self,request):
        # 校验用户信息
        # 白名单
        w_list = ['/user/reg','/user/login','/user/logout','/user/test','/note/page_test',]

        if request.path in w_list:
            return None

        if 'username' not in request.session:
            if 'username' not in request.COOKIES:
                print('---login mw check return---')
                return HttpResponseRedirect('/user/login')
            else:
                # 赋值回 session
                request.session['username'] = request.COOKIES['username']
        print('MyMW process_request do---')

    def process_view(self,request,callback,callback_args,callback_kwargs):
        # None 正常返回
        # HttpResponse 则跳出django 直接返回
        print('MyMW process_view do---')

    def process_response(self,requset,response):
         # 必须返回 response
        print('MyMW process_response do---')
        return response

class VisitLimitMW(MiddlewareMixin):

    # redis? key - 生命周期 1分钟
    count_dict = {}
    def process_request(self,request):
        # 检查请求次数并进行拦截
        # 取出访问者ip地址
        ip_add = request.META['REMOTE_ADDR']
        # /user/test

        if request.path  != '/user/test':
            return None
        count = self.count_dict.get(ip_add,0)
        print(count)
        count += 1
        self.count_dict[ip_add] = count
        if count > 5:
            return HttpResponse('访问频率过快,已重复第 %s 次'%(count))


