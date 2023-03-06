# 服务器运行版本（最简化）

import requests
import random
import re
import time

# print("作者：ybq")
url_login = "http://smse.fun-master.cn/report/login/dologin"
url = "http://smse.fun-master.cn/report/index/doreporthd"
ua = {
	'user-agent': "Mozilla/5.0 (Linux; Android 12; M2012K10C Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220604 Mobile Safari/537.36 MMWEBID/9863 MicroMessenger/8.0.24.2180(0x28001887) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
}
# 获取打卡时的时间
def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def login_clock_log(stu_no, password, current_province, current_city, current_area, current_address, at_school):
    # 登陆
    session = requests.session()
    login_result = session.post(url_login,
                                data={'stu_no': stu_no, 'password': password, 'rememberme': 0}, headers=ua)
    # print(login_result.text)
    if re.search(r'用户密码错误', login_result.text) or re.search(r"学号不存在", login_result.text):
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{get_time()[11:]}----{stu_no}----密码错误----' + '\n')
    elif re.search(r'登录成功', login_result.text):
        # 开始打卡并记录日志
        data_info = dict(at_school=f'{at_school}', practise=2, current_province=f'{current_province}',
                         current_city=f'{current_city}', current_area=f'{current_area}',
                         current_address=f'{current_address}', mor_check=f'36 度 {random.randint(3, 8)}',
                         non_check=f'36 度 {random.randint(3, 8)}', night_check=f'36 度 {random.randint(3, 8)}',
                         under_check=2, new_contact=2, new_contact_desc='', new_contact1=2, new_contact1_desc='',
                         mor_c=2, code=1, non_c=2, night_c=2,
                         mor_desc='', non_desc='', night_desc='', less_check=2, less_check_desc='')

        resp = session.post(url, data=data_info, headers=ua)
        # print(resp.text)
        with open('log.txt', 'a', encoding='utf-8') as f:
            if re.search('还未到填报时间', resp.text) or re.search('连接人数', resp.text):
                f.write(f'{get_time()[11:]}----{stu_no}----打卡失败' + '\n')
            if re.search('已经提交', resp.text) or re.search('成功', resp.text):
                f.write(f"{get_time()[11:]}----{stu_no}----{at_school}----{current_province}{current_city}{current_area}{current_address}----打卡成功" + '\n')
            session.close()
    # print("over!")

with open('log.txt', 'a', encoding='utf-8') as f:
    # 每天执行程序开始先输出当天日期
    # 注意这里是写到日志文件不要写错了
    # f.write('-' * 90 + '\n' + '-' * 40 + get_time()[:10] + '-' * 40 + '\n' + '-' * 90 + '\n')
    f.write('-' * 40 + get_time()[:10] + '-' * 40 + '\n')
with open("userdata.csv", 'r', encoding="utf-8") as f:  
    for line in f:
        line = line.strip()
        # print(line)
        user_data_list = line.split(',')
        stu_no = user_data_list[0]
        password = user_data_list[1]
        # print(user_data_list[5])
        # print(user_data_list[5] == 2)
        # print(user_data_list[5] == '2')
        if user_data_list[5] == '2':		# 2表示不在校
            at_school = '2'
            current_province = user_data_list[2]
            current_city = user_data_list[3]
            current_area = user_data_list[4]
            current_address = ''
        else:
            at_school = '1'
            current_province = '辽宁省'
            current_city = '大连市'
            current_area = '沙河口区'
            current_address = '杨树南街'
        # print(stu_no, password, current_province, current_city, current_area, current_address, at_school)
        login_clock_log(stu_no, password, current_province, current_city, current_area, current_address, at_school)
        # 每一个人打完随机间隔3~5s
        # time.sleep(random.randint(3, 5))
print("clock done!")
time.sleep(60)
