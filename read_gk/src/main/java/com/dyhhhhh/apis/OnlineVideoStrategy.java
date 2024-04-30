package com.dyhhhhh.apis;

import com.dyhhhhh.bean.OnlineVideoBean;
import com.dyhhhhh.bean.ReadVideoBean;
import com.dyhhhhh.bean.UserVisitsBean;
import com.dyhhhhh.common.CommonApis;
import com.dyhhhhh.config.RequestHttpConfig;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 * 在线观看视频的具体执行
 */
public class OnlineVideoStrategy implements Strategy{
    @Override
    public void execute(String activityId, HashMap<String, Object> activityDetails) throws Exception {
        //获取视频时长
        List<HashMap<String,Object>> uploads = (List<HashMap<String, Object>>) activityDetails.get("uploads");
        List<HashMap<String,Object>> videos = (List<HashMap<String, Object>>) uploads.get(0).get("videos");
        int duration = Integer.valueOf(String.valueOf(videos.get(0).get("duration")));
        System.out.println("开始观看视频");
        ReadVideoBean readVideoBean = new ReadVideoBean();
        readVideoBean.setStart(0);
        readVideoBean.setEnd(61);
        HashMap<String, Object> response = CommonApis.check_full(activityId, readVideoBean);
        //获取module_id
        Long module_id = Long.valueOf(String.valueOf(activityDetails.get("module_id")));
        Long syllabus_id = Long.valueOf(String.valueOf(activityDetails.get("syllabus_id")));
        //模拟点进去观看，这一次只记录观看次数+1
        do_online_video(Long.valueOf(activityId),module_id,syllabus_id,0,0,"view");
        //继续观看，从上次一次观看的最大时长开始往后观看
        HashMap<String,Object> data = (HashMap<String, Object>) response.get("data");
        List<List<Integer>> ranges = (List<List<Integer>>) data.get("ranges");
        for (List<Integer> range : ranges) {
            for (Integer r : range) {
                readVideoBean.setEnd(Math.max(readVideoBean.getEnd(),r));
            }
        }
        recursion_watch_video(duration,activityId,readVideoBean.getEnd(),module_id,syllabus_id);
    }

    /**
     * 递归观看直到80%
     * @param duration
     * @param video_activity_id
     * @param end
     * @param module_id
     * @param syllabus_id
     */
    public void recursion_watch_video(int duration,String video_activity_id,
                                      int end,Long module_id,Long syllabus_id) throws Exception {
        //判断是否观看到80%
        if(end < duration * 0.8){
            Thread.sleep(5 + new Random().nextInt(5));
            System.out.println("继续观看");
            int rand = 1 + new Random().nextInt(5);
            int start = end;
            if(duration - end + 60 + rand > 60){
                end = end + 60 + rand;
            }else {
                end = end + duration - end;
            }
            ReadVideoBean readVideoBean = new ReadVideoBean();
            readVideoBean.setStart(start);
            readVideoBean.setEnd(end);
            //发送观看时长
            do_user_visits(end);
            //记录
            CommonApis.check_full(video_activity_id,readVideoBean);
            //递归观看
            recursion_watch_video(duration,video_activity_id,end,module_id,syllabus_id);
        }else {
            System.out.println("观看完毕");
        }
    }
    /**
     * 发送观看次数及记录
     * @param activity_id
     * @param module_id
     * @param syllabus_id
     * @param start
     * @param end
     * @param action_type
     * @throws Exception
     */
    public void do_online_video(Long activity_id, Long module_id,
                                Long syllabus_id, int start, int end,
                                String action_type) throws Exception {
        Thread.sleep(3);
        OnlineVideoBean onlineVideoBean = new OnlineVideoBean();
        String url = "https://lms.ouchn.cn/statistics/api/online-videos";
        onlineVideoBean.setModule_id(module_id);
        onlineVideoBean.setSyllabus_id(syllabus_id);
        onlineVideoBean.setActivity_id(activity_id);
        onlineVideoBean.setAction_type(action_type);
        onlineVideoBean.setStart_at(start);
        onlineVideoBean.setEnd_at(end);
        //发送请求
        RequestHttpConfig.getInstance().startPost(url,"",onlineVideoBean);
    }
    /**
     * 发送观看时长
     */
    public void do_user_visits(int end) throws Exception {
        Thread.sleep(3);
        String url = "https://lms.ouchn.cn/statistics/api/user-visits";
        UserVisitsBean userVisitsBean = new UserVisitsBean();
        userVisitsBean.setVisit_duration(end);
        RequestHttpConfig.getInstance().startPost(url,"",userVisitsBean);
    }
}
