package com.dyhhhhh.apis;

import com.dyhhhhh.common.CommonApis;

import java.io.IOException;
import java.util.HashMap;

//上下文类，用于执行活动类型的方法
public class Context {
    private Strategy strategy;
    public Context(Strategy strategy){
        this.strategy = strategy;
    }
    public void setStrategy(Strategy strategy){
        this.strategy = strategy;
    }
    public void executeStrategy(String activityId) throws Exception {
        //获取该内容详情
        HashMap<String, Object> activityDetails = CommonApis.getActivityDetails(activityId);
        System.out.println(activityDetails);
        //在执行前发送学习中
        String type = String.valueOf(activityDetails.get("type"));
        System.out.println(type);
        CommonApis.post_learning_activity(type);
        //开始执行
        strategy.execute(activityId,activityDetails);
    }
}
