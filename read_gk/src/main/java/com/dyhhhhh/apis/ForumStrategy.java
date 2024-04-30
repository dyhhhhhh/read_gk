package com.dyhhhhh.apis;

import com.alibaba.fastjson2.JSON;
import com.dyhhhhh.bean.PublishAndReplyBean;
import com.dyhhhhh.config.RequestHttpConfig;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 * 发表讨论及回复的具体执行
 */
public class ForumStrategy implements Strategy{
    @Override
    public void execute(String activityId, HashMap<String, Object> activityDetails) throws Exception {
        //获取帖子id
        String topic_category_id = String.valueOf(activityDetails.get("topic_category_id"));
        HashMap<String, Object> topic = getPublished(topic_category_id,1);
        if(topic!=null){
            //标题
            String title = String.valueOf(topic.get("title"));
            //评论id
            String post_id = String.valueOf(topic.get("id"));
            //内容
            String content = String.valueOf(topic.get("content"));
            if (content.length() != 0){
                //去发表和回复帖子
                if (publish_post(topic_category_id, title, content) && replies_post(post_id,content)){
                    System.out.println("全部成功");
                }else {
                    System.out.println("失败");
                }
            }
        }

    }

    /**
     * 发表帖子
     * @param topic_category_id:帖子id
     * @param title:标题
     * @param content:内容
     * @return
     */
    public boolean publish_post(String topic_category_id,String title,String content) throws Exception {
        System.out.println("开始发表帖子..");
        String url = "https://lms.ouchn.cn/api/topics";
        Thread.sleep(5 + new Random().nextInt(5));
        PublishAndReplyBean publishAndReplyBean = new PublishAndReplyBean();
        publishAndReplyBean.setTitle(title);
        publishAndReplyBean.setContent(content);
        publishAndReplyBean.setCategory_id(topic_category_id);
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        //去发表
        String response = instance.startPost(url, "", publishAndReplyBean);
        if (response.length() > 0){
            System.out.println("发表成功");
            return true;
        }else {
            System.out.println("发表失败");
            return false;
        }

    }

    /**
     * 回复帖子
     * @param post_id:要回复的帖子id
     * @param content
     * @return
     */
    public boolean replies_post(String post_id,String content) throws IOException {
        System.out.println("开始回复帖子..");
        String url = "https://lms.ouchn.cn/api/topics/"+post_id+"/replies";
        PublishAndReplyBean publishAndReplyBean = new PublishAndReplyBean();
        publishAndReplyBean.setContent(content);
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        String response = instance.startPost(url, "", publishAndReplyBean);
        if (response.length() > 0){
            System.out.println("回复成功");
            return true;
        }else {
            System.out.println("回复失败");
            return false;
        }
    }
    /**
     * 获取评论
     * @param activityId:帖子id
     * @param page:页数
     * @return
     * @throws IOException
     */
    private HashMap<String, Object> getPublished(String activityId,int page) throws IOException {
        String url = "https://lms.ouchn.cn/api/forum/categories/"+activityId+"?conditions=%7B%7D&fields=id,title,created_by(id,name,nickname,comment,avatar_big_url,user_no),group_id,created_at,updated_at,content,read_replies(reply_id),reply_count,unread_reply_count,like_count,current_user_read,current_user_liked,in_common_category,user_role,has_matched_replies,uploads,user_role&page=" + page;
        RequestHttpConfig instance = RequestHttpConfig.getInstance();
        String text = instance.startGet(url, "");
        HashMap<String,Object> response = (HashMap<String, Object>) JSON.parse(text);
        //获取评论结果
        HashMap<String,Object> result = (HashMap<String, Object>) response.get("result");
        List<HashMap<String,Object>> topics = (List<HashMap<String, Object>>) result.get("topics");
        for (HashMap<String, Object> topic : topics) {
            String content = String.valueOf(topic.get("content"));
            if(verify_personal_information(content)){
                return topic;
            }
        }
        //翻页递归是找合适的
        if(page > 5){
            return null;
        }
        page = page + 1;
       return getPublished(activityId,page);
    }

    public boolean verify_personal_information(String content){
        return !content.contains("姓名") || !content.contains("学号");
    }

}
