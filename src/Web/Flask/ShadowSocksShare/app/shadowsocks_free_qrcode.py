#!/usr/bin/env python
"""
本代码使用了regex beautifulsoup4 qrcode这三个第三方库，只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
try:
    import regex as re
    from bs4 import BeautifulSoup
    import qrcode
except ImportError:
    print('Python缺少依赖库，请使用pip install -U regex beautifulsoup4 qrcode或者其他方式安装此依赖。\n本软件在Linux下写成，Python版本为3.5，如果遇到任何错误，请到GitHub上提交Issue。\n')
    exit(0)

import urllib
import sys
import requests
import base64
import json


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'
__url__ = 'https://github.com/the0demiurge/Python-Scripts/blob/master/src/MinorProjects/shadowsocks_free_qrcode.py'


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


def qrm2string(qrm):
    qrs = []
    for line in qrm:
        strline = ''.join(['██' if ele else '  ' for ele in line])
        qrs.append(strline)
    return qrs


def request_ss_list(url='https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    ss_list = list()

    for i in soup.find_all('p'):
        if re.match('\<p\>\s*服务器\d+[^:：]*[:：]', str(i)):
            ss_list.append(str(i))
    return ss_list


def get_servers(ss_list):
    servers = list()
    for i in ss_list:
        servers.append(dict())
        servers[-1]['string'] = i
        # name
        tmp = re.findall('服务器\d+[^:：]*(?=\s*[:：])', i)
        if tmp:
            servers[-1]['name'] = tmp[0]

        # server
        tmp = re.findall('(?<=服务器\s*\d+[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[\w\d\.]+', i)
        if tmp:
            servers[-1]['server'] = tmp[0]

        # server_port
        tmp = re.findall('(?<=端口\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)\d+', i)
        if tmp:
            servers[-1]['server_port'] = tmp[0]

        # password
        tmp = re.findall('(?<=密码\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['password'] = tmp[0]

        # method
        tmp = re.findall('(?<=加密方[式法]\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['method'] = tmp[0]

        # SSR协议
        tmp = re.findall('(?<=SSR协议\s*[^:：]*[:：]\s*[^a-zA-Z_0-9]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['ssr_protocol'] = tmp[0]

        # 混淆
        tmp = re.findall('(?<=混淆\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['obfs'] = tmp[0]

        try:
            try:
                # SSR信息是否完整
                decoded = ':'.join([
                                   servers[-1]['server'],
                                   servers[-1]['server_port'],
                                   servers[-1]['ssr_protocol'],
                                   servers[-1]['method'],
                                   servers[-1]['obfs'],
                                   base64.urlsafe_b64encode(bytes(servers[-1]['password'], 'utf-8')).decode('utf-8').replace('=', '')
                                   ])
                decoded += '/?remarks={remarks}'.format(
                    remarks=base64.urlsafe_b64encode(bytes(servers[-1]['name'], 'utf-8')).decode('utf-8').replace('=', '')
                )
                ss_uri = 'ssr://{endoced}'.format(
                                                  endoced=base64.urlsafe_b64encode(bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')
                )
            except (KeyError, EOFError):
                # 不完整则是SS
                decoded = '{method}:{password}@{hostname}:{port}'.format(
                    method=servers[-1]['method'],
                    password=servers[-1]['password'],
                    hostname=servers[-1]['server'],
                    port=servers[-1]['server_port'],
                )
                ss_uri = 'ss://{}#{}'.format(
                    str(base64.urlsafe_b64encode(bytes(decoded, encoding='utf8')), encoding='utf-8'),
                    urllib.parse.quote(servers[-1]['name']))

            qr = qrcode.QRCode(border=0)
            qr.add_data(ss_uri)
            servers[-1]['qrcode'] = qrm2string(qr.get_matrix())
            servers[-1]['qr'] = qr
            servers[-1]['uri'] = ss_uri
            servers[-1]['decoded_url'] = urllib.parse.unquote(ss_uri)

            obfs = servers[-1]['obfs'] if 'obfs' in servers[-1] else ''
            method = servers[-1]['method'] if 'method' in servers[-1] else ''
            ssr_protocol = servers[-1]['ssr_protocol'] if 'ssr_protocol' in servers[-1] else ''

            servers[-1]['json'] = json.dumps({
                "server": servers[-1]['server'],
                "server_ipv6": "::",
                "server_port": int(servers[-1]['server_port']),
                "local_address": "127.0.0.1",
                "local_port": 1080,
                "password": servers[-1]['password'],
                "timeout": 300,
                "udp_timeout": 60,
                "method": method,
                "protocol": ssr_protocol,
                "protocol_param": "",
                "obfs": obfs,
                "obfs_param": "",
                "fast_open": False,
                "workers": 1
            },
                ensure_ascii=False,
                indent=2)
        except (KeyError, EOFError):
            href = get_href(servers[-1]['string'], '.*查看连接信息.*')
            servers[-1]['href'] = href
    return servers


def main():
    ss_list = request_ss_list()
    servers = get_servers(ss_list)
    return servers


if __name__ == '__main__':
    print(main())
