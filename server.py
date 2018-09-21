# -*- encoding: utf-8 -*
import importlib,sys
importlib.reload(sys)

from wsgiref.simple_server import make_server
from cgi import parse_qs


class Request(object):
    def __init__(self):
        self.method = ""
        self.params = {}

    def add(self, key, value):
        """添加一些客户端的请求信息"""
        if key not in self.params.keys():
            self.params[key] = value

    def __repr__(self):
        return self.method


class Application(object):
    def __init__(self, name):
        self.routes = {}
        self.name = name
        # self.request = Request()

    def route(self, path):
        def decorator(funcname):
            if path not in self.routes:
                self.routes[path] = funcname
            else:
                # 可以做额外的提示处理，这里不过多操作了
                pass
            return funcname
        return decorator

    def __call__(self, env, start_response):
        """
        根据WSGI标准，web应用程序需要包含两个参数：
        @param env : 一个包含了请求内容的字典
        @param start_response ： 开始处理来自客户端的请求
        """
        path = env["PATH_INFO"]
        if path in self.routes:
            status = '200 OK'
            headers = [('Content-Type', 'text/html;charset=UTF-8')]
            # 对来自客户端的请求做封装处理
            request_method = env.get("REQUEST_METHOD", "")
            print("***"*28, request_method)
            self.request = Request()
            if request_method == "POST":
                content_length = int(env.get('CONTENT_LENGTH', 0))
                form_data = parse_qs(env.get('wsgi.input', '').read(content_length).decode('utf-8'))
                # print("form_data{}".format(form_data))
                # print("str{}".format(str))
                str_ascii = form_data['code'][0].encode('utf-8')
                # print("str_ascii:{}".format(str_ascii))
                form_data = {b'code':[str_ascii]}
                # print("form_data:{}".format(form_data))
                self.request.add(key='method', value="POST")
                self.request.add(key='post_data', value=str_ascii)
            elif request_method == "GET":
                self.request.add(key='method', value=request_method)
                query_string = env.get('QUERY_STRING', '')
                self.request.add(key='query_string', value=query_string)
            start_response(status, headers)
            return self.routes[path](self.request)
        else:
            # 处理函数不包含在路由控制器内
            status = '404 Not Found'
            headers = [('Content-Type', 'text/html;charset=UTF-8')]
            start_response(status, headers)
            return ["No handler match for `{}`".format(path).encode('utf8')]

    def run(self, host='127.0.0.1', port=8080):
        """
        模拟Flask的run实现，让服务器直接跑起来即可。
        """
        print("Server is listening on {}:{} ... ...\nPress CTRL+C to Quit.".\
        format(host, port))
        try:
            server = make_server(host=host, port=port, app=self)
            server.serve_forever()
        except Exception as e:
            # 可以做下日志处理，这里简单的打印一下即可。
            print('服务器解析出错了，详细内容为：{}'.format(e))