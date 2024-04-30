package com.dyhhhhh.bean;

import com.dyhhhhh.common.PersonalInformation;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 公共参数
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class CommonPayloadBean {
    public String user_id = PersonalInformation.USER_ID();
    public Long org_id = PersonalInformation.ORG_ID();
    public String user_agent = PersonalInformation.USER_AGENT();
    public boolean is_teacher = PersonalInformation.IS_TEACHER();
    public boolean is_student = PersonalInformation.IS_STUDENT();
    public String org_name = PersonalInformation.ORG_NAME();
    public String org_code = PersonalInformation.ORG_CODE();
    public String user_name = PersonalInformation.USER_NAME();
    public String user_no = PersonalInformation.USER_NO();
    public String dep_code = PersonalInformation.DEP_CODE();
    public String dep_id = PersonalInformation.DEP_ID();
    public String dep_name = PersonalInformation.DEP_NAME();

}
