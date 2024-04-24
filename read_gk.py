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
        # 下面的子任务
        # module_syllabuses = list(module["syllabuses"])
        # for syllabus in module_syllabuses:
        #     # 子任务id
        #     syllabus_id = syllabus["id"]
        #     # 子任务名称
        #     syllabus_name = syllabus["summary"]


# 获取当前学习活动的情况
def all_activities(module_id):
    global learning_activity_payload
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
        learning_activity_payload["activity_id"] = learning_activity_id
        learning_activity_payload["activity_type"] = learning_activity_type
        print("《{}》-----类型:{}".format(learning_activity_title, learning_activity_type))
        # 普通页面
        if learning_activity_type == "page":
            # 发送学习中
            post_learning_activity(learning_activity_id, learning_activity_type)
            read_page(learning_activity_id)
        # 在线视频
        elif learning_activity_type == "online_video":
            # 获取视频信息
            details = get_details(learning_activity_id)
            uploads = details["uploads"]
            videos = uploads[0]["videos"]
            learning_activity_payload["sub_type"] = str(uploads[0]["name"]).split(".")[1]
            learning_activity_payload["sub_id"] = uploads[0]["id"]
            duration = videos[0]["duration"]
            # 发送学习中
            post_learning_activity(learning_activity_id, learning_activity_type)
            read_video(learning_activity_id, 0, 61, duration)
        # 发表讨论及回复
        elif learning_activity_type == "forum":
            # 发送学习中
            post_learning_activity(learning_activity_id, learning_activity_type)
            details = get_details(learning_activity_id)
            topic_category_id = details["topic_category_id"]
            publish_discussion(learning_activity_id, topic_category_id)
        # 外部网站
        elif learning_activity_type == "web_link":
            # 发送学习中
            post_learning_activity(learning_activity_id, learning_activity_type)
            read_page(learning_activity_id)
        # 打开文件
        elif learning_activity_type == "material":
            view_material(learning_activity_id, learning_activity_type)
        # 暂时手动答题
        elif learning_activity_type == "exam":
            while not check_pass_examination(learning_activity_id):
                print("请手动答题...《{}》---》《{}》".format(course_name, learning_activity_title))
                time.sleep(random.randint(6, 12))
    # 考试
    if exams is not None:
        for exam in exams:
            # 考试id
            exam_id = exam["id"]
            # 考试名称
            exam_title = exam["title"]
            # 暂时手动答题
            while not check_pass_examination(exam_id):
                print("请手动答题...《{}》---》《{}》".format(course_name, exam_title))
                time.sleep(random.randint(6, 12))


# 获取考试分数
def get_score(exams):
    # for exam in exams:
    #     # 考试标题
    #     title = exam["title"]
    #     # 最高考试分数
    #     score = exam["activity_final_score"]
    #     print("考试的名称:" + title)
    #     print("考试的分数:" + score)
    pass


# 获取我的课程
def get_myCourses():
    global course_id, course_code, course_name, learning_activity_payload
    url = "https://lms.ouchn.cn/api/my-courses?conditions=%7B%22status%22:%5B%22ongoing%22%5D,%22keyword%22:%22%22%7D&fields=id,name,course_code,department(id,name),grade(id,name),klass(id,name),course_type,cover,small_cover,start_date,end_date,is_started,is_closed,academic_year_id,semester_id,credit,compulsory,second_name,display_name,created_user(id,name),org(is_enterprise_or_organization),org_id,public_scope,course_attributes(teaching_class_name,copy_status,tip,data),audit_status,audit_remark,can_withdraw_course,imported_from,allow_clone,is_instructor,is_team_teaching,academic_year(id,name),semester(id,name),instructors(id,name,email,avatar_small_url),is_master,is_child,has_synchronized,master_course(name)&page=1&page_size=10"
    referer = "https://lms.ouchn.cn/user/courses"
    headers["referer"] = referer
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    # 课程json数组
    courses = response["courses"]
    for course in courses:
        course_name = course["display_name"]
        course_id = course["id"]
        # 赋值master_course_id
        learning_activity_payload["master_course_id"] = get_master_course_id()
        course_code = course["course_code"]
        print("当前任务:{}".format(course_name))
        courses_modules()


# 判断当前活动是否完成
def is_full(activity_id, data):
    time.sleep(random.randint(3, 8))
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    url = "https://lms.ouchn.cn/api/course/activities-read/{}".format(activity_id)
    payload = data
    headers["referer"] = referer
    return requests.request("POST", url, headers=headers, data=payload).json()


# 学习普通页面
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
def read_video(video_activity_id, start: int, end: int, duration):
    print("开始观看视频...")
    payload = json.dumps({
        "start": start,
        "end": end
    })
    # 视频直接看到80%以上
    result = is_full(video_activity_id, payload)

    # 继续观看,从上次一次观看的最大时长开始往后观看
    data = result["data"]
    ranges = data["ranges"]
    for rang in ranges:
        for r in rang:
            end = max(r, end)
    print("视频时长->{}".format(duration))
    # 计算是否观看到80%
    if end < duration * 0.85:
        # 延迟
        time.sleep(random.randint(5, 8))
        print("继续观看")
        # 递归观看随机1分钟以上直到通过
        rand = random.randint(1, 5)
        start = end
        if duration - end + 60 + rand > 60:
            end = end + 60 + rand
        else:
            end = end + duration - end
        print("start:" + str(start))
        print("end:" + str(end))
        read_video(video_activity_id, start, end, duration)
    else:
        print("观看完毕")


# 发表讨论及回帖
def publish_discussion(learning_activity_id, topic_category_id):
    # 判断是否完成
    complete = is_full(learning_activity_id, {})["completeness"]
    if complete != "full":
        # 首先获取该讨论的已发表内容，然后进行复制回帖
        topic = getPublished(topic_category_id)
        title = topic["title"]
        post_id = topic["id"]
        content = topic["content"]
        if len(content) != 0:
            # 发表帖子
            response = publish_post(topic_category_id, title, content)
            if len(response) > 0:
                print("发表成功")
            else:
                print("发表失败")
            # 回复帖子
            response = replies_post(post_id, content)
            if len(response) > 0:
                print("回复成功")
            else:
                print("回复失败")
    else:
        print("已学习")


# 回复帖子
def replies_post(post_id, content):
    print("开始回复帖子...")
    time.sleep(random.randint(6, 12))
    url = "https://lms.ouchn.cn/api/topics/{}/replies".format(post_id)
    referer = "https://lms.ouchn.cn/course/{}/topic/{}".format(course_id, post_id)
    headers["referer"] = referer
    payload = json.dumps({
        "content": content,
        "uploads": []
    })
    return requests.request("POST", url, headers=headers, data=payload).json()


# 发表帖子
def publish_post(topic_category_id, title, content):
    print("开始发表帖子...")
    time.sleep(random.randint(6, 12))
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
    global learning_activity_payload
    complete = is_full(material_activity_id, {})["completeness"]
    if complete != "full":
        # 获取其中所有文件，然后去访问
        result = get_details(material_activity_id)
        # 找到里面的上传文件
        uploads = result["uploads"]
        # 循环阅读文件
        for upload in uploads:
            time.sleep(random.randint(6, 12))
            # 获取每个文件后缀
            suffix = str(upload["name"]).split(".")[1]

            learning_activity_payload["sub_type"] = suffix
            learning_activity_payload["sub_id"] = uploads[0]["id"]
            # 发送学习中
            post_learning_activity(material_activity_id, learning_activity_type)
            print("阅读资料:{}".format(upload["name"]))
            complete = is_full(material_activity_id, {"upload_id": upload["id"]})
            if complete == "full":
                break


# 在线形考
def view_online_examination(exam_activity_id):
    # 校验是否完成考试
    is_adopt = check_pass_examination(exam_activity_id)
    if bool(is_adopt) is not True:
        # 获取考试详情
        detail = get_detail_exam(exam_activity_id)
        print(detail)


# 获取考题
def get_exam_questions(exam_activity_id):
    referer = "https://lms.ouchn.cn/exam/{}/subjects".format(exam_activity_id)
    headers["referer"] = referer
    url = "https://lms.ouchn.cn/api/exams/{}/distribute".format(exam_activity_id)
    subjects = requests.get(url, headers).json()
    # 获取题型及做题
    subjects = subjects["subjects"]
    for subject in subjects:
        # 创建对象用来返回答案
        my_answer = {}
        # 单选
        if subject["type"] == "single_selection":
            do_single_selection(subject, my_answer)


# 单选
def do_single_selection(subject, my_answer):
    # 获取题目纯文本
    exam_title = subject["description"]
    exam_title = BeautifulSoup(exam_title, 'html.parser').text

    answer = get_answer(exam_title)
    # 获取选项
    options = subject["options"]
    # 遍历选项找到合适的答案
    for option in options:
        print(subject)


# 在外部找到答案
def get_answer(topic):
    pass


# 提交最终答案
def Submit_final_answer(exam_activity_id):
    url = "https://lms.ouchn.cn/api/exams/{}/submissions".format(exam_activity_id)
    payload = {
        "exam_paper_instance_id": 30073059087,
        "exam_submission_id": 30074824586,
        "subjects": [
            {
                "subject_id": 30018602518,
                "subject_updated_at": "2024-04-07T01:53:58Z",
                "answer_option_ids": [30049816884]
            },
            {
                "subject_id": 30018602524,
                "subject_updated_at": "2024-04-07T01:53:58Z",
                "answer_option_ids": [30049816891]
            },
            {
                "subject_id": 30018602532,
                "subject_updated_at": "2024-04-07T01:53:58Z",
                "answer_option_ids": [30049816907]
            },
            {
                "subject_id": 30018602535,
                "subject_updated_at": "2024-04-07T01:53:58Z",
                "answer_option_ids": [30049816910]
            }
        ],
        "progress": {"answered_num": 4, "total_subjects": 6}, "reason": "user"}


# 检测考试是否通过
def check_pass_examination(exam_activity_id):
    url = "https://lms.ouchn.cn/api/exams/{}/submissions".format(exam_activity_id)
    raw = requests.get(url=url, headers=headers)
    result = raw.json()
    code = raw.status_code
    if int(code) == 404:
        print("还未考试")
        return False
    exam_score = result["exam_score"]
    if int(exam_score) < 60:
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
    referer = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    headers["referer"] = referer
    url = "https://lms.ouchn.cn/api/activities/{}".format(video_activity_id)
    response = requests.request("GET", url, headers=headers).json()
    return response


# 发送学习zhong
def post_learning_activity(activity_id, activity_type):
    print("发送学习中...")
    global learning_activity_payload
    url = "https://lms.ouchn.cn/statistics/api/learning-activity"
    learning_activity_payload["activity_id"] = activity_id
    learning_activity_payload["activity_type"] = activity_type
    requests.request("POST", url, headers=headers, data=learning_activity_payload)
    print("发送完毕")


# 获取master_course_id,该值是直接写死到html文件里面的，所以解析html取值。
def get_master_course_id():
    if course_id == 0:
        return
    url = "https://lms.ouchn.cn/course/{}/learning-activity/full-screen".format(course_id)
    # url = "https://lms.ouchn.cn/course/30000083529/learning-activity/full-screen"
    response = requests.request("GET", url, headers=headers).content
    soup = BeautifulSoup(response, 'html.parser')
    masterCourseId = soup.find('input', attrs={'id': 'masterCourseId'})['value']
    return masterCourseId


headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'HWWAFSESTIME=1713762330009; HWWAFSESID=2d3152aa45b1d79351f; session=V2-30000000001-91581878-a3c8-40bd-94a9-33163da7c43f.MzAwMDEwMTE2MjY.1713851707529.sxoBuv-pclrnUmCB6BbjeOfjdxQ',
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
course_id = 0
course_code = ""
course_name = ""
learning_activity_payload = {
    "org_id": 30000000001,
    "user_id": "30001011626",
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
    "org_name": "河北开放大学",
    "org_code": "130",
    "user_no": "2413001200455",
    "user_name": "段雨寒",
    "course_code": course_code,
    "course_name": course_name,
    "dep_id": "30000000002",
    "dep_name": "开放教育学院",
    "dep_code": "1300000"
}
if __name__ == '__main__':
    # 入口
    get_myCourses()
    # view_online_examination(30000417418)
