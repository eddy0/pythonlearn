import socket
import ssl


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gual&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


def header_from_dict(headers):
    l = []
    for k, v in headers.items():
        line = r"{}: {}\r\n".format(k, v)
        l.append(line)
    log(''.join(l))
    return ''.join(l)


# https://movie.douban.com/top250


def parsed_url(url):
    protocol = 'http'
    if url[0:7] == 'http://':
        u = url.split('://')[1]
    elif url[0:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    i = u.find('/')
    if i == -1:
        path = '/'
        host = u
    else:
        path = u[i:]
        host = u[:i]

    port_dict = {
        'http': 80,
        'https': 443,
    }

    h = host.find(':')
    if h == -1:
        port = port_dict[protocol]
    else:
        host = host.split(':')[0]
        port = host.split(':')[1]

    return protocol, host, port, path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
        return s
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
        return s


def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response


def parsed_response(r):
    # HTTP/1.1 301 ....\r\n
    # headers\r\n\r\n
    # body
    body = r.split('\r\n\r\n', 1)[1]

    h = r.split('\r\n\r\n')[0]
    i = h.find('\r\n')
    headers = h[i:]
    status_code = h[:i].split()[1]
    return status_code, headers, body


def get_body(url):
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection:close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    request = http_request.encode(encoding)

    log('send request', request)
    s.sendall(request)

    # recv data, get response data: status_code, headers, body
    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)

    if int(status_code) == 301:
        url = headers['Location']
        get(url)
    log('received data..')

    return body


def detail_one_page(url):
    body = get_body(url)
    body = body.split('<ol class="grid_view">')[1]
    items = body.split('<div class="item">')[1:]

    for i in items:
        rank = i.split("<em class=\"\">")[1].split("</em>")[0]
        name = i.split('<span class=\"title\">')[1].split('</span>')[0]
        score = i.split("<span class=\"rating_num\" property=\"v:average\">")[1].split('</span>')[0]
        commit = i.split("<span>")[1].split('</span>')[0]
        quote = i.split("<span class=\"inq\">")[1].split('</span>')[0]

        print('排名:{}\r\n电影名:{}, 评分:{}, 人数:{}\r\nquote:{}'.format(rank, name, score, commit, quote))


def path_with_query(path, query):
    l = []
    for k, v in query.items():
        l.append('{}={}'.format(k, v))
    u = '&'.join(l)
    p = path + '?' + u
    return p


def parsed_url1(url, query):
    protocol = 'http'
    if url[0:7] == 'http://':
        u = url.split('://')[1]
    elif url[0:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    i = u.find('/')
    if i == -1:
        path = '/'
        host = u
    else:
        host = u[:i]
        path = path_with_query(u[i:], query)

    port_dict = {
        'http': 80,
        'https': 443,
    }

    h = host.find(':')
    if h == -1:
        port = port_dict[protocol]
    else:
        host = host.split(':')[0]
        port = host.split(':')[1]

    return protocol, host, port, path


def socket_by_protocol1(protocol):
    if protocol == 'http':
        s = socket.socket()
        return s
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
        return s


def response_by_socket1(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response


def parsed_response1(r):
    # HTTP/1.1 301 ....\r\n
    # headers\r\n\r\n
    # body
    body = r.split('\r\n\r\n', 1)[1]

    h = r.split('\r\n\r\n')[0]
    i = h.find('\r\n')
    headers = h[i:]
    status_code = h[:i].split()[1]
    return status_code, headers, body


def get_body1(url, query):
    protocol, host, port, path = parsed_url1(url, query)
    s = socket_by_protocol1(protocol)
    s.connect((host, port))

    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection:close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    request = http_request.encode(encoding)

    log('send request', request)
    s.sendall(request)

    # recv data, get response data: status_code, headers, body
    response = response_by_socket1(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response1(r)

    if int(status_code) == 301:
        url = headers['Location']
        get_body1(url, query)
    log('received data..')

    return body


def detail_one_page1(url, query):
    body = get_body1(url, query)
    body = body.split('<ol class="grid_view">')[1]
    # log(body)
    items = body.split('<div class="item">')[1:]
    # log(items)

    for i in items:
        rank = i.split("<em class=\"\">")[1].split("</em>")[0]
        name = i.split('<span class=\"title\">')[1].split('</span>')[0]
        score = i.split("<span class=\"rating_num\" property=\"v:average\">")[1].split('</span>')[0]
        commit = i.split("<span>")[1].split('</span>')[0]
        try:
            quote = i.split("<span class=\"inq\">")[1].split('</span>')[0]
        except:
            quote = 'N/A'

        print('排名:{}\r\n电影名:{}, 评分:{}, 人数:{}\r\nquote:{}'.format(rank, name, score, commit, quote))


query = {
    'start': 0
}

url = 'https://movie.douban.com/top250'

if __name__ == '__main__':
    for i in range(10):
        print('第{}页'.format(i + 1))
        detail_one_page1(url, query)
        query['start'] += 25
