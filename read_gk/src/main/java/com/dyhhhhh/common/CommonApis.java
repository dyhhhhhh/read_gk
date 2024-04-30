package com.dyhhhhh.common;

import com.alibaba.fastjson2.JSON;
import com.dyhhhhh.bean.LearningActivityBean;
import com.dyhhhhh.bean.ModuleActivitiesBean;
import com.dyhhhhh.config.RequestHttpConfig;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;

/**
 * 公共的api
 */
public class CommonApis {
    /**
     * 获取该活动的详细信息
     * @param activityId:活动id
     */
    public static HashMap<String,Object> getActivityDetails(String activityId) throws IOException {
        String url = "https://lms.ouchn.cn/api/activities/"+activityId+"";
        RequestHttpConfig requestHttpConfig = RequestHttpConfig.getInstance();
        return (HashMap<String, Object>) JSON.parse(requestHttpConfig.startGet(url,""));
    }

    /**
     * 检测当前活动的状态
     * @param activityId
     * @param data
     * @return
     */
    public static HashMap<String,Object> check_full(String activityId,Object data) throws IOException {
        String url = "https://lms.ouchn.cn/api/course/activities-read/"+activityId+"";
        RequestHttpConfig requestHttpConfig = RequestHttpConfig.getInstance();
        return (HashMap<String, Object>) JSON.parse(requestHttpConfig.startPost(url, "", data));
    }

    /**
     * 发送正在学习中
     * @param activityType
     */
    public static void post_learning_activity(String activityType) throws IOException {
        System.out.println("发送学习中...");
        LearningActivityBean learningActivityBean = new LearningActivityBean();
        learningActivityBean.setActivity_type(activityType);
        learningActivityBean.setEnrollment_role("student");
        learningActivityBean.setActivity_name(null);
        learningActivityBean.setModule(null);
        learningActivityBean.setAction("open");
        learningActivityBean.setMode("normal");
        learningActivityBean.setChannel("web");

        learningActivityBean.setTarget_info(new HashMap<>());
        String url = "https://lms.ouchn.cn/statistics/api/learning-activity";
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        System.out.println(instance.startPost(url, "", learningActivityBean));
    }
    /**
     * 获取模块下面所有的活动
     */
    public static List<HashMap<String,Object>> getModuleActivities(ModuleActivitiesBean moduleActivitiesBean) throws IOException {
        String url = "https://lms.ouchn.cn/api/course/30000083529/all-activities";
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        HashMap<String,List<HashMap<String,Object>>> hashMap = (HashMap<String, List<HashMap<String, Object>>>) JSON.parse(instance.startGet(url, moduleActivitiesBean.toString()));
        return hashMap.get("learning_activities");
    }
    /**
     * 解析html获取master_course_id
     */
    public static String get_master_course_id(String courseId) throws IOException {
        String url = "https://lms.ouchn.cn/course/"+courseId+"/learning-activity/full-screen";
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        String text = instance.startGet(url, "");
        Document document = Jsoup.parse(text);
        Element masterCourseId = document.select("#masterCourseId").first();
        return masterCourseId.val();
    }
}
