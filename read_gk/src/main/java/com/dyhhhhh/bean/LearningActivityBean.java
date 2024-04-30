package com.dyhhhhh.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.Map;


/**
 * 构造发送 learning-activity 接口参数的对象
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class LearningActivityBean extends CommonPayloadBean implements Serializable {
    private String action;
    private String activity_name;
    private String activity_type;
    private String channel;
    private String course_code;
    private String course_id;
    private String course_name;
    private String enrollment_role;
    private Long master_course_id;
    private String mode;
    private String module;
    private Map<String,String> target_info;
    private Long ts = System.currentTimeMillis();


}
