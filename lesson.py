import requests
import json
from bs4 import BeautifulSoup


class Lesson_plan():
    """获取课程信息"""
    def __init__(self, url_head, xh, xm):
        self.url_head = url_head
        self.xh = xh
        self.xm = xm

    def lesson_file(self):
        """判断课程计划文件是否存在，若存在则读取；不存在则重新爬取并保存"""

        try:
            filename = self.xh[0:6] + '.json'
            with open(filename, 'r', encoding='utf-8') as file_obj:
                lesson_list = json.load(file_obj)

        except FileNotFoundError:
            """获取课程信息"""
            url_N121607 = self.url_head + 'pyjh.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121607'
            # 获取教学计划界面_VIEWSTATE
            headers_0 = {
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding':
                'gzip, deflate',
                'Accept-Language':
                'zh-CN,zh;q=0.9',
                'Connection':
                'keep-alive',
                'DNT':
                '1',
                'Host':
                'jxw.sylu.edu.cn',
                'Referer':
                self.url_head + 'xs_main.aspx?xh=' + self.xh,
                'Upgrade-Insecure-Requests':
                '1',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
            resp_0 = requests.get(url_N121607, headers=headers_0)
            bs_0 = BeautifulSoup(resp_0.text, 'lxml')
            viewstate = bs_0.find(type="hidden")
            viewstate = viewstate.next_sibling.next_sibling.next_sibling.next_sibling
            viewstate = str(viewstate['value'])
            # print(viewstate)

            # 跳转教学计划请求头，不全可能会导致跳转失败
            headers_1 = {
                'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding':
                'gzip, deflate',
                'Accept-Language':
                'zh-CN,zh;q=0.9',
                'Cache-Control':
                'max-age=0',
                'Connection':
                'keep-alive',
                'Content-Length':
                '4264',
                'Content-Type':
                'application/x-www-form-urlencoded',
                'DNT':
                '1',
                'Host':
                'jxw.sylu.edu.cn',
                'Origin':
                'http://jxw.sylu.edu.cn',
                'Referer':
                self.url_head + 'xs_main.aspx?xh=' + self.xh,
                'Upgrade-Insecure-Requests':
                '1',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }

            lesson_list = {}
            page = [
                'DBGrid:_ctl24:_ctl0', 'DBGrid:_ctl24:_ctl1',
                'DBGrid:_ctl24:_ctl2', 'DBGrid:_ctl24:_ctl3',
                'DBGrid:_ctl24:_ctl4'
            ]
            for p in page:
                data_1 = {
                    '__EVENTTARGET': p,
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': viewstate,
                    'xq': '全部',
                    'kcxz': '全部'
                }

                resp_1 = requests.post(url_N121607,
                                       headers=headers_1,
                                       data=data_1)
                bs = BeautifulSoup(resp_1.text, 'lxml')
                # print(bs)
                result = bs.find(text='课程代码')
                # print(result)
                for tt in result.parent.parent.parent.next_siblings:
                    t_list = []
                    # 筛选包含成绩的Tag
                    if len(tt) < 7 or str(
                            type(tt)) != "<class 'bs4.element.Tag'>":
                        continue
                    else:
                        for t in tt.children:
                            t_list.append(t.string)

                    lesson_list[t_list[1]] = t_list[17]

            filename = self.xh[0:6] + '.json'
            with open(filename, 'w', encoding='utf-8') as file_obj:
                json.dump(lesson_list, file_obj, ensure_ascii=False, indent=4)

        return lesson_list
