# coding: utf-8
import importlib,sys
importlib.reload(sys)
from server import Application
import test_bot

app = Application(__name__)


agent = test_bot.Load_model()

# 下面开始对于前台的请求做路由控制
@app.route('/')
def index(request):
    print("handler：", request)
    with open('./templates/index.html', 'r', encoding="utf8") as f:
        html = f.read()
        f.close()
    yield html.encode('utf8')


@app.route('/api/user')
def user(request):
    print(request.params)
    if request.params.get('method', '') == "POST" or request.params.get('method', '')== "GET":
        data = request.params.get('post_data').decode('utf-8')
        data.replace("查","查一下").replace("明天","明天的").replace("后天","后天的")
        # print(data)
        result = test_bot.get_res(agent,data)
        res = ""
        for i in range(len(result)):
            res += str(result[i]['text']).replace("\n","<br>").replace("\t\t","&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
            # res +="{}<br>".format(str(result [i]['text']).replace(""""))
            # print(result [i]['text'])
        # print(result)
        # result = result.encode('utf-8')
        # print(res)
        yield res.encode('utf-8')
    else:
        yield "Nothing".encode('utf8')


if __name__ == "__main__":
    # import sys
    # print(sys.stdout.encoding)
    app.run(host='127.0.0.1', port=8001)