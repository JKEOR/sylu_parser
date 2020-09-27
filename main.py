import requests
from login import Login
from lesson import Lesson_plan
from score import Score
from gpa import Gpa


def main():
    """爬取沈阳理工大学教学网"""

    xh = str(input("请输入学号："))
    pw = str(input("请输入密码："))

    # 获取登录地址
    r = requests.get('http://jxw.sylu.edu.cn/')
    url_head = str(r.url)[0:50]

    # 登录并获取姓名
    login = Login(xh, pw, url_head)
    xm = login.login_website()

    # 获取课程计划学位课
    lesson = Lesson_plan(url_head, xh, xm)
    lesson_list = lesson.lesson_file()

    # 获取成绩
    score = Score(url_head, xh, xm, lesson_list, '')
    score.get_page()
    grades = score.get_data()

    # 计算绩点
    year = '2019-2020'
    get_gpa = Gpa(grades, year)
    gpa = get_gpa.count_gpa()

    # 输出信息
    print('\n', xm)
    print(year + "学年绩点1(除去公共选修课)：" + gpa[0])
    print(year + "学年绩点2(除去所有选修课)：" + gpa[1])
    print("学位课绩点：" + gpa[2])


if __name__ == "__main__":
    msg = """此程序可以爬取沈阳理工大学教学网，实现自动计算绩点，查询成绩等功能。
初次使用需要爬取教学计划，大概需要2-3分钟的时间，请耐心等待。
初次运行会生成.json格式文件，该文件为学位课信息，请不要删除。
——————by JKOR\n"""
    print(msg)
    main()
    input()
