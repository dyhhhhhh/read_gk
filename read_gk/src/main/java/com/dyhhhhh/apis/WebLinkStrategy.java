package com.dyhhhhh.apis;

import java.io.IOException;
import java.util.HashMap;

/**
 * 打开外部网站活动
 */
public class WebLinkStrategy implements Strategy{
    @Override
    public void execute(String activityId, HashMap<String, Object> activityDetails) throws IOException {
        //和浏览page页面一样的
        PageStrategy pageStrategy = new PageStrategy();
        pageStrategy.execute(activityId,activityDetails);
    }
}
