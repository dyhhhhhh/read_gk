import com.dyhhhhh.apis.Context;
import com.dyhhhhh.apis.PageStrategy;
import com.dyhhhhh.apis.Strategy;
import com.dyhhhhh.bean.ModuleActivitiesBean;
import com.dyhhhhh.common.CommonApis;
import com.dyhhhhh.common.TypeEnum;
import okhttp3.*;
import org.junit.Test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public class test {
    @Test
    public void getAllCourses() throws Exception {
//        MyCoursesApi myCoursesApi = MyCoursesApi.getMyCoursesApi();
//        //获取所有课程进度
//        System.out.println(myCoursesApi.getAllCoursesSchedule());
//        //获取所有课程
//        System.out.println(myCoursesApi.getAllCourses());
//        //获取指定课程下面所有的模块
//        List<Map<String, Object>> coursesModules = myCoursesApi.getCoursesModules("30000083529");
//        System.out.println(coursesModules);
        //获取所有模块id
        ModuleActivitiesBean moduleActivitiesBean = new ModuleActivitiesBean();
//        ArrayList<String> strings = new ArrayList<>();
//        for (Map<String, Object> coursesModule : coursesModules) {
//            strings.add(String.valueOf(coursesModule.get("id")));
//
//        }
        moduleActivitiesBean.setModule_ids(new ArrayList<String>() {
            {add("30000474355");
            }
        });
        //获取当前模块下所有活动
        List<HashMap<String, Object>> moduleActivities1 = CommonApis.getModuleActivities(moduleActivitiesBean);

        for (HashMap<String, Object> stringObjectHashMap : moduleActivities1) {
            //判断类型
            String type = String.valueOf(stringObjectHashMap.get("type"));
            //获取id
            String activityId = String.valueOf(stringObjectHashMap.get("id"));
            Strategy pageStrategy = null;
            if (TypeEnum.PAGE.getValue().equals(type)){
                pageStrategy = new PageStrategy();
            }
            Context context = new Context(pageStrategy);
            context.executeStrategy(activityId);
            System.out.println(stringObjectHashMap);
        }



        //context.executeStrategy();
    }
    @Test
    public void test() throws IOException {
        OkHttpClient client = new OkHttpClient().newBuilder()
                .build();
        MediaType mediaType = MediaType.parse("application/json; charset=UTF-8");
        RequestBody body = RequestBody.create(mediaType, "{\"org_id\":30000000001,\"user_id\":\"30001011626\",\"course_id\":\"30000083529\",\"enrollment_role\":\"student\",\"is_teacher\":false,\"activity_id\":30004402194,\"activity_type\":\"page\",\"activity_name\":null,\"module\":null,\"action\":\"open\",\"ts\":1714437432508,\"user_agent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0\",\"mode\":\"normal\",\"channel\":\"web\",\"target_info\":{},\"master_course_id\":135717,\"org_name\":\"河北开放大学\",\"org_code\":\"130\",\"user_no\":\"2413001200455\",\"user_name\":\"段雨寒\",\"course_code\":\"202403-02970130\",\"course_name\":\"国家开放大学学习指南\",\"dep_id\":\"30000000002\",\"dep_name\":\"开放教育学院\",\"dep_code\":\"1300000\"}");
        Request request = new Request.Builder()
                .url("https://lms.ouchn.cn/statistics/api/learning-activity")
                .method("POST", body)
                .addHeader("accept", "application/json, text/javascript, */*; q=0.01")
                .addHeader("accept-language", "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6")
                .addHeader("cache-control", "no-cache")
                .addHeader("content-type", "application/json; charset=UTF-8")
                .addHeader("cookie", "HWWAFSESID=6f3532fb8d6a4689d20; HWWAFSESTIME=1714432120831; session=V2-30000000001-c4a1aa77-9c26-46cd-a627-26035b44e783.MzAwMDEwMTE2MjY.1714523832459.GwISF19ngmstfzvMkrZ0d6FIcZQ")
                .addHeader("origin", "https://lms.ouchn.cn")
                .addHeader("pragma", "no-cache")
                .addHeader("priority", "u=1, i")
                .addHeader("referer", "https://lms.ouchn.cn/course/30000083529/learning-activity/full-screen")
                .addHeader("sec-ch-ua", "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"")
                .addHeader("sec-ch-ua-mobile", "?0")
                .addHeader("sec-ch-ua-platform", "\"Windows\"")
                .addHeader("sec-fetch-dest", "empty")
                .addHeader("sec-fetch-mode", "cors")
                .addHeader("sec-fetch-site", "same-origin")
                .addHeader("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")
                .addHeader("x-requested-with", "XMLHttpRequest")
                .build();
        Response response = client.newCall(request).execute();
        System.out.println(response);
    }
    @Test
    public void jsoupTest() throws IOException {
        System.out.println(CommonApis.get_master_course_id("30000083529"));
    }
}
