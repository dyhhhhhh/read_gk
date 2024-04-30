package com.dyhhhhh.apis;

import com.alibaba.fastjson2.JSON;
import com.dyhhhhh.bean.MyCoursesBean;
import com.dyhhhhh.common.PersonalInformation;
import com.dyhhhhh.config.RequestHttpConfig;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 获取所有课程api
 */
public class MyCoursesApi{
    private Map<String,Object> MyCourses;
    //构造单例对象
    private static MyCoursesApi myCoursesApi;
    //私有化。 MyCourses 只需要获取一次就够了
    private MyCoursesApi() throws IOException {
        if (myCoursesApi == null){
            String url = "https://lms.ouchn.cn/api/my-courses";
            RequestHttpConfig requestHttpConfig = RequestHttpConfig.getInstance();
            String text = requestHttpConfig.startGet(url, new MyCoursesBean().toString());
            MyCourses = (HashMap<String, Object>) JSON.parse(text);
        }
    }
    //初始化MyCourses
    static {
        try {
            myCoursesApi = getMyCoursesApi();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    //唯一对外返回对象
    public static synchronized MyCoursesApi getMyCoursesApi() throws IOException {
        if (myCoursesApi == null){
            myCoursesApi = new MyCoursesApi();
        }
        return myCoursesApi;
    }

    public List<Map<String, Object>> getAllCourses() {
        return (List<Map<String, Object>>) MyCourses.get("courses");
    }

    //获取所有课程的进度
    public Map<String,Double> getAllCoursesSchedule(){
        HashMap<String, Double> stringIntegerHashMap = new HashMap<>();
        Object obj = MyCourses.get("courses");
        //检测是否可以强转
        if (obj instanceof List<?>){
            List<Map<String,Object>> courses = (List<Map<String, Object>>) obj;
            for (Map<String, Object> cour : courses) {
                stringIntegerHashMap.put(String.valueOf(cour.get("name")),Double.valueOf(cour.get("completeness").toString()));
            }
            return stringIntegerHashMap;
        }else {
            return null;
        }
    }

    //获取课程下面的所有模块
    public List<Map<String,Object>> getCoursesModules(String coursesId) throws IOException {
        List<Map<String, Object>> maps;
        String url = "https://lms.ouchn.cn/api/courses/"+coursesId+"/modules";
        RequestHttpConfig requestHttpConfig = RequestHttpConfig.getInstance();
        HashMap<String,List<Map<String,Object>>> text = (HashMap<String, List<Map<String, Object>>>) JSON.parse(requestHttpConfig.startGet(url, ""));
        maps = text.get("modules");
        return maps;
    }

}
