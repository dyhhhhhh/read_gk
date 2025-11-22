import random
import time
import requests
import json
from bs4 import BeautifulSoup


# 获取课程下面的所有学习活动
def courses_modules():
    headers["referer"] = "https://lms.ouchn.cn/course/{}/ng".format(course_id)
    url = "https://lms.ouchn.cn/api/courses/{}/modules".format(course_id)
    modules = requests.get(url, headers=headers).json()
    modules = modules["modules"]
    # 当前课程所有学习活动数组
    for module in modules:
        # 学习活动名称
        module_name = module["name"]
        # 学习活动id
        module_id = module["id"]
        print(module_name)
        # 获取当前学习活动的情况
        all_activities(module_id)


# 获取当前学习活动的情况
def all_activities(module_id):
    global common_payload
    module_ids = [module_id]
    headers["referer"] = "https://lms.ouchn.cn/course/{}/ng".format(course_id)
    url = "https://lms.ouchn.cn/api/course/{}/all-activities?module_ids={}&activity_types=learning_activities,exams,classrooms,live_records,rollcalls&no-loading-animation=true".format(
        course_id, module_ids)
    response = requests.request("GET", url, headers=headers).json()
    # 获取当前考试分数
    # get_score(response["exams"])
    # 去学习
    # 获取当前要学习的类型
    learning_activities = response["learning_activities"]
    # 获取考试内容
    exams = response["exams"]
    for learning_activity in learning_activities:
        learning_activity_id = learning_activity["id"]
        learning_activity_title = learning_activity["title"]
        learning_activity_type = learning_activity["type"]
        if learning_activity_id in completed_learning_activity:
            print("跳过当前课程:" + learning_activity_title)
            continue
        common_payload["activity_id"] = learning_activity_id
        print("《{}》-----类型:{}".format(learning_activity_title, learning_activity_type))
        # 普通页面
        if learning_activity_type == "page":
            # 发送学习中
            post_learning_activity(learning_activity_type)
            read_page(learning_activity_id)
        # 在线视频
        elif learning_activity_type == "online_video":
            # 获取视频信息
            details = get_details(learning_activity_id)
            uploads = details["uploads"]
            # 获取视频信息
            videos = uploads[0]["videos"]
            # 获取音频信息
            audits = uploads[0]["audio"]

            common_payload["sub_type"] = str(uploads[0]["name"]).split(".")[1]
            common_payload["sub_id"] = uploads[0]["id"]

            if len(list(videos)) == 0:
                duration = audits["duration"]
            else:
                duration = videos[0]["duration"]
            # 发送学习中
            post_learning_activity(learning_activity_type)

            read_video(learning_activity_id, 0, 61, duration, details)
            del common_payload["sub_type"]
            del common_payload["sub_id"]
        # 发表讨论及回复
        elif learning_activity_type == "forum":
            # 判断是否完成
            complete = is_full(learning_activity_id, {})["completeness"]
            if complete != "full":
                # 发送学习中
                post_learning_activity(learning_activity_type)
                publish_discussion(learning_activity_id)
            else:
                print("已学习")
        # 外部网站
        elif learning_activity_type == "web_link":
            # 发送学习中
            post_learning_activity(learning_activity_type)
            read_page(learning_activity_id)
        # 打开文件
        elif learning_activity_type == "material":
            complete = is_full(learning_activity_id, {})["completeness"]
            if complete != "full":
                view_material(learning_activity_id, learning_activity_type)
        # 暂时手动答题,这种可以跳过，我这里是循环到手动做完
        elif learning_activity_type == "exam":
            print("跳过")
            # while not check_pass_examination(learning_activity_id):
            #     print("请手动答题...《{}》---》《{}》".format(course_name, learning_activity_title))
            #     time.sleep(random.randint(30, 60))
    # # 考试,这种不能跳
    # if exams is not None:
    #     for exam in exams:
    #         # 考试id
    #         exam_id = exam["id"]
    #         # 考试名称
    #         exam_title = exam["title"]
    #         # 暂时手动答题
    #         while not check_pass_examination(exam_id):
    #             print("请手动答题...《{}》---》《{}》".format(course_name, exam_title))
    #             time.sleep(60)


# 获取考试分数
def get_score():
    pass


# 获取我的课程
def get_myCourses():
    global course_id, course_code, course_name, learning_activity_payload, master_course_id, common_payload
    url = "https://lms.ouchn.cn/api/my-courses?conditions=%7B%22status%22:%5B%22ongoing%22%5D,%22keyword%22:%22%22%7D&fields=id,name,course_code,department(id,name),grade(id,name),klass(id,name),course_type,cover,small_cover,start_date,end_date,is_started,is_closed,academic_year_id,semester_id,credit,compulsory,second_name,display_name,created_user(id,name),org(is_enterprise_or_organization),org_id,public_scope,course_attributes(teaching_class_name,copy_status,tip,data),audit_status,audit_remark,can_withdraw_course,imported_from,allow_clone,is_instructor,is_team_teaching,academic_year(id,name),semester(id,name),instructors(id,name,email,avatar_small_url),is_master,is_child,has_synchronized,master_course(name)&page=1&page_size=10"
    referer = "https://lms.ouchn.cn/user/courses"
    headers["referer"] = referer
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    # 课程json数组
    courses = response["courses"]
    for course in courses:
        completeness = course["completeness"]
        if completeness is not None and completeness > 93:
            continue
        course_name = course["display_name"]
        course_code = course["course_code"]
        course_id = course["id"]
        # 赋值参数
        master_course_id = get_master_course_id()
        common_payload["course_id"] = course_id
        common_payload["course_code"] = course_code
        common_payload["course_name"] = course_name
        common_payload["master_course_id"] = master_course_id
        print("当前任务:{}".format(course_name))
        # 查询该课程已完成的任务
        my_completeness(course_id)
        courses_modules()


# 获取已完成的课程
def my_completeness(course_id):
    # 将课程id传过去，该接口会查询出学习完成的任务
    url = "https://lms.ouchn.cn/api/course/{}/my-completeness".format(course_id)
    referer = "https://lms.ouchn.cn/course/{}/ng".format(course_id)
    headers["referer"] = referer
    response = requests.request("GET", url, headers=headers).json()
    completed_result = response["completed_result"]
    completed = completed_result["completed"]
    completed_learning_activity.update(completed["learning_activity"])


def read_page(page_activity_id):
    print("开始阅读...")
    # 判断任务是否完成
    result = is_full(page_activity_id, {})
    complete = result["completeness"]
    if complete != "full":
        time.sleep(random.randint(8, 15))
        print("失败")
    else:
        print("阅读成功")


# 学习视频
def read_video(video_activity_id, start: int, end: int, duration, detail):
    print("开始观看视频...")
    payload = json.dumps({
        "start": start,
        "end": end
    })
    result = is_full(video_activity_id, payload)

    module_id = detail["module_id"]

    syllabus_id = detail["syllabus_id"]
    sub_id = common_payload["sub_id"]
    # 模拟点进去观看，这一次只记录观看次数+1
    do_online_video(video_activity_id, module_id, syllabus_id, sub_id, 0, 0, "view")
    # 继续观看,从上次一次观看的最大时长开始往后观看
    data = result["data"]
    if len(dict(data)) != 0:
        ranges = data["ranges"]
        for rang in ranges:
            for r in rang:
                end = max(r, end)
    print("视频时长->{}".format(duration))
    # 发送观看时长
    # # 发送观看中
    recursion_watch_video(duration, video_activity_id, end, module_id, syllabus_id, sub_id)


# 递归观看视频
def recursion_watch_video(duration, video_activity_id, end, module_id, syllabus_id, sub_id):
    # 计算是否观看到80%
    if end < duration * 0.80:
        # 延迟
        time.sleep(random.randint(5, 10))
        print("继续观看")
        # 递归观看随机1分钟以上直到通过
        rand = random.randint(1, 5)
        start = end
        if duration - end + 60 + rand > 60:
            end = end + 60 + rand
        else:
            end = end + duration - end
        payload = json.dumps({
            "start": start,
            "end": end
        })
        # 发送观看时长
        do_user_visits(end - start)
        # 发送观看中
        do_online_video(video_activity_id, module_id, syllabus_id, sub_id, start, end, "play")
        # 记录观看到哪里了
        print(payload)
        print(is_full(video_activity_id, payload))
        print("start:" + str(start))
        print("end:" + str(end))
        recursion_watch_video(duration, video_activity_id, end, module_id, syllabus_id, sub_id)
    else:
        print("观看完毕")


# 发送online_video
def do_online_video(activity_id, module_id, syllabus_id, upload_id, start, end, action_type):
    time.sleep(5)
    global common_payload
    url = "https://lms.ouchn.cn/statistics/api/online-videos"
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    local_payload = common_payload
    local_payload["module_id"] = module_id
    local_payload["syllabus_id"] = syllabus_id
    local_payload["activity_id"] = activity_id
    local_payload["upload_id"] = upload_id
    local_payload["reply_id"] = None
    local_payload["comment_id"] = None
    local_payload["forum_type"] = ""
    local_payload["action_type"] = action_type
    local_payload["ts"] = int(time.time() * 1000)
    local_payload["meeting_type"] = "online_video"
    local_payload["start_at"] = start
    local_payload["end_at"] = end
    local_payload["duration"] = end - start
    print(requests.request("POST", url, headers=headers, data=json.dumps(local_payload)))


# 发送user-visits
def do_user_visits(end):
    time.sleep(5)
    global common_payload
    url = "https://lms.ouchn.cn/statistics/api/user-visits"
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    local_payload = common_payload
    local_payload["visit_duration"] = end
    local_payload["browser"] = "edge"
    local_payload["activity_type"] = "online_video"
    local_payload["auto_interval"] = True
    print(requests.request("POST", url, headers=headers, data=json.dumps(local_payload)))


# 发表讨论及回帖
def publish_discussion(learning_activity_id):
    # 获取帖子id
    details = get_details(learning_activity_id)
    topic_category_id = details["topic_category_id"]
    # 首先获取该讨论的已发表内容，然后进行复制回帖
    try:
        topic = getPublished(topic_category_id)
        title = topic["title"]
        post_id = topic["id"]
        content = topic["content"]
    except Exception as e:
        print(e)
        return
    if len(content) != 0:
        # 发表帖子
        response = publish_post(topic_category_id, title, content)
        if len(response) > 0:
            print("发表成功")
        else:
            print("发表失败")
        # 回复帖子
        response = replies_post(post_id, content + "。")  # 加个句号防止重复
        if len(response) > 0:
            print("回复成功")
        else:
            print("回复失败")


# 发表帖子
def publish_post(topic_category_id, title, content):
    print("开始发表帖子...")
    time.sleep(random.randint(8, 15))
    payload = json.dumps({
        "title": title,
        "content": content,
        "category_id": topic_category_id,
        "uploads": []
    })
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    url = "https://lms.ouchn.cn/api/topics"
    headers["referer"] = referer
    return requests.request("POST", url, headers=headers, data=payload).json()


# 回复帖子
def replies_post(post_id, content):
    print("开始回复帖子...")
    time.sleep(random.randint(8, 15))
    url = "https://lms.ouchn.cn/api/topics/{}/replies".format(post_id)
    referer = "https://lms.ouchn.cn/course/{}/topic/{}".format(course_id, post_id)
    headers["referer"] = referer
    payload = json.dumps({
        "content": content,
        "uploads": []
    })
    return requests.request("POST", url, headers=headers, data=payload).json()


# 获取评论
def getPublished(topic_category_id, page=1):
    url = "https://lms.ouchn.cn/api/forum/categories/{}?conditions=%7B%7D&fields=id,title,created_by(id,name,nickname,comment,avatar_big_url,user_no),group_id,created_at,updated_at,content,read_replies(reply_id),reply_count,unread_reply_count,like_count,current_user_read,current_user_liked,in_common_category,user_role,has_matched_replies,uploads,user_role&page={}".format(
        topic_category_id, page)
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    response = requests.request("GET", url, headers=headers, data={}).json()
    # 获取评论结果
    result = response["result"]
    topics = result["topics"]
    for topic in topics:
        if verify_personal_information(topic["content"]):
            return topic
    # 连翻五页都没找到合适的直接返回
    if page > 5:
        return
    page = page + 1
    getPublished(topic_category_id, page)


# 查看文件活动
def view_material(material_activity_id, learning_activity_type):
    global common_payload
    local_payload = common_payload
    # 获取其中所有文件，然后去访问
    result = get_details(material_activity_id)
    # 找到里面的上传文件
    uploads = result["uploads"]
    # 循环阅读文件
    for upload in uploads:
        time.sleep(random.randint(8, 15))
        # 获取每个文件后缀
        suffix = str(upload["name"]).split(".")[1]
        sub_id = upload["id"]
        local_payload["sub_type"] = suffix
        local_payload["sub_id"] = sub_id
        # 发送学习中
        post_learning_activity(learning_activity_type)
        print("阅读资料:{}".format(upload["name"]))
        complete = is_full(material_activity_id, json.dumps({"upload_id": sub_id}))
        if complete == "full":
            print("阅读完毕,退出")
            break
    # 阅读文件后删除key
    del local_payload["sub_type"]
    del local_payload["sub_id"]


# 判断当前活动是否完成
def is_full(activity_id, data):
    time.sleep(random.randint(5, 8))
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    url = "https://lms.ouchn.cn/api/course/activities-read/{}".format(activity_id)
    payload = data
    headers["referer"] = referer
    return requests.request("POST", url, headers=headers, data=payload).json()


# 检测考试是否通过
def check_pass_examination(exam_activity_id):
    url = "https://lms.ouchn.cn/api/exams/{}/submissions".format(exam_activity_id)
    raw = requests.get(url=url, headers=headers)
    result = raw.json()
    code = raw.status_code
    if int(code) != 200:
        print("还未考试")
        return False
    exam_score = result["exam_score"]
    try:
        exam_score_int = int(exam_score)
        if exam_score_int < 0:
            return False
    except ValueError:
        print(ValueError)
        return False
    return True


# 获取考试详情
def get_detail_exam(exam_activity_id):
    # 获取该考试详情
    url = "https://lms.ouchn.cn/api/exams/{}".format(exam_activity_id)
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    return requests.request("GET", url, headers=headers).json()


# 简单校验。
def verify_personal_information(content: str):
    if "姓名" in content or "学号" in content:
        return False
    else:
        return True


# 获取活动详情
def get_details(video_activity_id):
    time.sleep(3)
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    url = "https://lms.ouchn.cn/api/activities/{}".format(video_activity_id)
    response = requests.request("GET", url, headers=headers).json()
    return response


# 发送学习zhong
def post_learning_activity(activity_type):
    global common_payload
    # 赋值一遍，去操作local_payload。不会修改全局公共变量
    local_payload = common_payload
    time.sleep(random.randint(2, 5))
    # 更新值
    local_payload["ts"] = int(time.time() * 1000)
    local_payload["activity_type"] = activity_type
    local_payload["enrollment_role"] = "student"
    local_payload["activity_name"] = "None"
    local_payload["module"] = "None"
    local_payload["action"] = "open"
    local_payload["mode"] = "normal"
    local_payload["channel"] = "web"
    local_payload["target_info"] = {}

    print("发送学习中...")
    url = "https://lms.ouchn.cn/statistics/api/learning-activity"
    print(requests.request("POST", url, headers=headers, data=json.dumps(local_payload)))
    print("发送完毕")


# 获取master_course_id,该值是直接写死到html文件里面的，所以解析html取值。
def get_master_course_id():
    if course_id == 0:
        return
    url = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    response = requests.request("GET", url, headers=headers).content
    soup = BeautifulSoup(response, 'html.parser')
    masterCourseId = soup.find('input', attrs={'id': 'masterCourseId'})['value']
    return masterCourseId


# 需要复制自己的cookie,打开f12随便抓个包就行
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # cookie信息
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

course_code = ""
course_name = ""
master_course_id = 0
# 个人信息  learning-activity 的接口 参数
common_payload = {
    "user_id": "",
    "org_id": ,
    "is_teacher": False,
    "is_student": True,
    "org_name": "",
    "org_code": "",
    "user_no": "",
    "user_name": "",
    "dep_id": "",
    "dep_name": "",
    "dep_code": "",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
}
# 该容器保存总完成任务数和列表
completed_learning_activity = set()

if __name__ == '__main__':
    # 入口
    get_myCourses()
