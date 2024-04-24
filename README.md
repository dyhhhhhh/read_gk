# read_gk
实现了国家开放学习平台全自动化学习刷课时。
# 快速开始
电脑有python环境和浏览器就可以，然后我代码大部分都写了注释，按照注释简单抓个包就可以跑起来了。
# 功能
目前实现了刷页面、视频、看文件、跳网页、讨论发帖及回复。视频我统一调到了观看总时长的百分之85，因为有的考试需要上一个视频看到百分之80及以上才可以。暂时没有写考试功能，因为找不到合适免费的题库，目前遇到有的考试有的必须做完才可以继续，有的可以配置跳过考试。
# 注意
延迟不要关,否则连接太多容易挂掉。里面还有一些代码未完善，不影响运行。
# 重要配置
##### 这个信息在网站上打开f12后然后随便点进一个学习，找到末尾是这个 learning-activity 的接口然后复制你的信息就可以了
```
learning_activity_payload = {
    "org_id": 0,
    "user_id": "",
    "course_id": course_id,
    "enrollment_role": "student",
    "is_teacher": "false",
    # 动态添加该参数
    # "activity_id": activity_id,
    # "activity_type": activity_type,
    "activity_name": None,
    "module": None,
    "action": "open",
    "ts": int(time.time() * 1000),
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "mode": "normal",
    "channel": "web",
    "target_info": {},
    # "master_course_id": get_master_course_id(),
    # 动态添加该参数
    # "sub_type": "pdf",
    # "sub_id": 17191463,
    "org_name": "",
    "org_code": "",
    "user_no": "",
    "user_name": "",
    "course_code": course_code,
    "course_name": course_name,
    "dep_id": "",
    "dep_name": "",
    "dep_code": ""
}
```
##### 需要复制自己的cookie,打开f12随便抓个包就行
```
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 需要复制自己的cookie,打开f12随便抓个包就行
    'cookie': '',
    'origin': 'https://lms.ouchn.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'x-requested-with': 'XMLHttpRequest'
}
```
# qq:1613203335
