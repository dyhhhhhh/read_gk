package com.dyhhhhh.apis;

import com.dyhhhhh.bean.MaterialBean;
import com.dyhhhhh.common.CommonApis;

import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 * 打开文件的具体执行
 */
public class MaterialStrategy implements Strategy{
    @Override
    public void execute(String activityId, HashMap<String, Object> activityDetails) throws Exception {
        MaterialBean materialBean = new MaterialBean();
        //找到里面的文件
        List<HashMap<String,Object>> uploads = (List<HashMap<String, Object>>) activityDetails.get("uploads");
        //循环阅读文件
        for (HashMap<String, Object> upload : uploads) {
            Thread.sleep(5 + new Random().nextInt(5));
            //获取每个文件后缀
            String suffix = String.valueOf(upload.get("name")).split("\\.")[1];
            //文件id
            String sub_id = String.valueOf(upload.get("id"));
            materialBean.setSub_type(suffix);
            materialBean.setSub_id(sub_id);
            //发送学习中
            CommonApis.post_learning_activity("material");
            System.out.println("阅读资料:"+upload.get("name"));
            //判断是否完成
            HashMap<String, String> stringStringHashMap = new HashMap<>();
            stringStringHashMap.put("upload_id", sub_id);
            HashMap<String, Object> stringObjectHashMap = CommonApis.check_full(activityId, stringStringHashMap);
            if (stringStringHashMap.get("completeness").equals("full")) {
                System.out.println("阅读完毕");
                break;
            }
        }
    }
}
