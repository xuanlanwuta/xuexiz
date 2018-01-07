import time
import pymysql
import re
import urllib.parse


# 路由：根据不一样的请求，不一样的函数去服务器
# key是浏览器中可能输入的url
# value是url需要调用的函数的引用
# 通过这个字典，做到了只要添加一行 key-value就完成了 对应服务的设定
#url_func_dict = {
#    "/index.html": index,        
#    "/center.html": center,        
#    "/register.html": register,        
#    "/login.html": login,
#    "/unregister.html": unregister
#}
url_func_dict = dict()

def route(url):
    def set_func(func):
        url_func_dict[url] = func  # 向url_func_dict中添加一个key-value，key是url，value是对应的函数引用
        #def call_func(*args, **kwargs):
        #    return func(*args, **kwargs)
        #return call_func
    return set_func


@route(r"/index\.html")
def index(ret):
    print("------1-------")
    # 1. 打开对应的模板文件
    # open在没有指明用什么模式打开的时候 ，默认是r
    with open("./templates/index.html") as f:
        html_content = f.read()

    # 2. 查询mysql
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    sql = """select * from info;"""
    print("------2-------")
    cursor.execute(sql)
    data_from_mysql = cursor.fetchall()  # 存储查询出来的数据
    cursor.close()
    print("------21-------")
    conn.close()

    # 3. 将mysql查询出来的数据替换到模板中
    line_html = """
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>
                        <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
                    </td>
                </tr>
    """
    code_html = ""
    for temp in data_from_mysql:
        code_html += line_html % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[1])

    html_content = re.sub(r"\{%content%\}", code_html, html_content)

    print("------3-------")
    # 4. 返回数据
    return html_content


@route(r"/center\.html")
def center(ret):
    # 1. 打开对应的模板文件
    # open在没有指明用什么模式打开的时候 ，默认是r
    with open("./templates/center.html") as f:
        html_content = f.read()

    # 2. 从mysql中查询数据
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    sql = """select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id;"""
    cursor.execute(sql)
    data_from_mysql = cursor.fetchall()  # 存储查询出来的数据
    cursor.close()
    conn.close()

    # 这是一行的模板
    line_html = """<tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                        <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                        </td>
                        <td>
                        <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                        </td>
                    </tr>
                """

    code_html = ""
    for temp in data_from_mysql:
        code_html += line_html % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[0],temp[0])

    # 3. 替换数据
    html_content = re.sub(r"\{%content%\}", code_html, html_content)

    # 4. 返回模板数据
    return html_content


@route(r"/register\.html")
def register(ret):
    return "-----注册页面----current time is %s" % time.ctime()


@route(r"/login\.html")
def login(ret):
    return "-----登陆页面----current time is %s" % time.ctime()


@route(r"/unregister\.html")
def unregister(ret):
    return "-----注销页面----current time is %s" % time.ctime()


# 方案１：一个url定义一个函数,如果要是有多个ｕｒｌ的话，那么就意味着需要定义多个函数
#@route("/add/000007.html")
#def add_focus():
#    return "-----添加关注成功----"
#
#
#@route("/add/000036.html")
#def add_focus2():
#    return "-----添加关注成功----"

# 方案２：多个url可以对应同一个函数
#@route("/add/000007.html")
#@route("/add/000036.html")
#def add_focus2():
#    return "-----添加关注成功----"

# 方案３：一个通用的url对应一个函数，那么就完成了　浏览器中多个url都能够访问这个函数
@route(r"^/add/(\d+)\.html$")
def add_focus(ret):

    # 最终的目的：向数据库中写入相应的数据,来表达已经关注了这支股票
    # 1. 获取你要关注的股票代码
    stock_code = ret.group(1)
    print("------>>>>>>>", stock_code)

    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    # 2. 判断是否有这支股票
    sql = """select * from info where code=%s;"""
    cursor.execute(sql, [stock_code])
    data_from_mysql = cursor.fetchall()
    if not data_from_mysql:
        # 如果要是没有这个股票，那么就退出
        cursor.close()
        conn.close()
        return "没有这支股票...."

    # 3. 判断是否之前关注过这支股票
    sql = """select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cursor.execute(sql, [stock_code])
    data_from_mysql = cursor.fetchall()
    if data_from_mysql:
        # 如果要是关注过这个股票，那么就退出
        cursor.close()
        conn.close()
        return "请误重复关注...."

    # 4. 写入数据
    sql = """insert into focus (info_id) select id from info where code=%s;""" 
    cursor.execute(sql, [stock_code])
    conn.commit()
    cursor.close()
    conn.close()

    return "-----添加关注成功----"


@route(r"^/del/(\d+)\.html$")
def del_focus(ret):

    # 最终的目的：向数据库中写入相应的数据,来表达已经关注了这支股票
    # 1. 获取你要关注的股票代码
    stock_code = ret.group(1)
    print("------>>>>>>>", stock_code)

    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    # 2. 判断是否有这支股票
    sql = """select * from info where code=%s;"""
    cursor.execute(sql, [stock_code])
    data_from_mysql = cursor.fetchall()
    if not data_from_mysql:
        # 如果要是没有这个股票，那么就退出
        cursor.close()
        conn.close()
        return "没有这支股票...."

    # 3. 判断是否之前关注过这支股票
    sql = """select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cursor.execute(sql, [stock_code])
    data_from_mysql = cursor.fetchall()
    if not data_from_mysql:
        # 如果之前没有关注过这个股票，那么就退出
        cursor.close()
        conn.close()
        return "请先关注，然后在取消关注...."

    # 4. 删除股票对应的关注信息
    sql = """delete from focus where info_id = (select id from info where code=%s);"""
    cursor.execute(sql, [stock_code])
    conn.commit()
    cursor.close()
    conn.close()

    return "-----取消关注成功----"


@route(r"/update/(\d+)\.html")
def show_edit_noteinfo_page(ret):
    
    # 0. 提取股票代码
    stock_code = ret.group(1)

    # 1. 打开模板
    with open("./templates/update.html") as f:
        html = f.read()

    # 2. 从数据库中查询数据
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    sql = """select note_info from focus where info_id=(select id from info where code=%s);"""
    cursor.execute(sql, [stock_code])
    # data_from_mysql = cursor.fetchall()  # ((备注信息,),)
    data_from_mysql = cursor.fetchone()  # (备注信息,)
    cursor.close()
    conn.close()

    # 3. 合并数据
    html = re.sub(r"\{%note_info%\}", data_from_mysql[0], html)
    html = re.sub(r"\{%code%\}", stock_code, html)

    # 4. 返回数据给http服务器
    return html


@route(r"/update/(\d+)/(.*)\.html")
def save_edit_noteinfo(ret):
    # 1. 提取股票代码以及备注信息
    stock_code = ret.group(1)  # 股票代码
    note_info = urllib.parse.unquote(ret.group(2))  # 备注

    # 2. 修改数据
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',database='stock_db',charset='utf8')
    cursor = conn.cursor()
    sql = """update focus as f inner join info as i on i.id=f.info_id set f.note_info=%s where i.code=%s;"""
    cursor.execute(sql, [note_info, stock_code])
    conn.commit()
    cursor.close()
    conn.close()

    return "修改备注成功..."


def application(env, set_header):
    # 1. 调用set_header指向的函数，将response_header传递过去
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html; charset=UTF-8')]
    set_header(status, response_headers)

    # 提取url
    path_info = env['PATH_INFO']  # /index.html
    try:
        """
        # 打印url_func_dict，验证是否已经通过装饰器将这个字典中需要的key-value都添加了
        print(url_func_dict)
        # url不一样，那么取出来的value，即函数的引用不一样
        func = url_func_dict[path_info]  # 如果path_info是/index.html那么也就意味着取 index函数的引用
        # 那么将来调用的时候，就调用了不一样的函数
        response_body = func()
        """
        # 此时字典的样子如下：
        # url_func_dict = {
        #   r"/add/\d+\.html$": add_focus,
        #   r"/index\.html": index
        #}
        for r_url, func in url_func_dict.items():
            # 当此次for循环的时候，r_url是原字符串 （正则表达式）,而func指向了这个正则表达式匹配的情况下
            # 需要调用的函数
            ret = re.match(r_url, path_info)    
            if ret:
                response_body = func(ret)
                break
        else:
            response_body = "次ｕｒｌ没有对应的函数......"

    except Exception as ret:
        response_body = "-----not found you page-----"

    # 2. 通过return 将body返回
    return response_body

