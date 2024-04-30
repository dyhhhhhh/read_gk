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
    public void jsoupTest() throws IOException {
        System.out.println(CommonApis.get_master_course_id("30000083529"));
    }
}
