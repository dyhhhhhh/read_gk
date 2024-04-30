package com.dyhhhhh.apis;

import com.dyhhhhh.common.CommonApis;

import java.io.IOException;
import java.util.HashMap;
import java.util.Random;

/**
 * 浏览页面的具体执行
 */
public class PageStrategy implements Strategy{

    @Override
    public void execute(String activityId,HashMap<String, Object> activityDetails) throws IOException {
        //获取详情信息
        String title = (String) activityDetails.get("title");
        //检查是否观看完毕
        System.out.println("开始阅读---" + title);
        HashMap<String, Object> stringObjectHashMap = CommonApis.check_full(activityId, "{}");
        //随机睡眠5-10
        int sleepTime = 5 + new Random().nextInt(5);
        try {
            Thread.sleep(sleepTime * 1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        System.out.println(stringObjectHashMap);
        if (!String.valueOf(stringObjectHashMap.get("completeness")).equals("full")){
            System.out.println("阅读失败--->" + title);
        }else {
            System.out.println("阅读成功");
        }
    }
}
