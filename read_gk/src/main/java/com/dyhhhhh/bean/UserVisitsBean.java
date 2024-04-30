package com.dyhhhhh.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserVisitsBean extends CommonPayloadBean{
    private int visit_duration;
    private static String browser = "edge";
    private static String activity_type = "online_video";
    private static Boolean auto_interval = true;
}
