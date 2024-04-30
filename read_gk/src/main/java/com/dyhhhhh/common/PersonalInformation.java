package com.dyhhhhh.common;

import com.sun.org.apache.bcel.internal.generic.PUSH;
import sun.security.mscapi.PRNG;

public class PersonalInformation {
    //个人信息
    private static final String COOKIE = "";
    private static final String USER_ID = "";
    private static final Long ORG_ID = 0L;
    private static final boolean IS_TEACHER = false;
    private static final boolean IS_STUDENT = true;
    private static final String ORG_NAME = "";
    private static final String ORG_CODE = "";
    private static final String USER_NAME = "";
    private static final String USER_NO = "";
    private static final String DEP_CODE = "";
    private static final String DEP_ID = "";
    private static final String DEP_NAME = "";
    private static final String USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0";

    //
    public static String getCookie() {
        return COOKIE;
    }
    public static String USER_ID(){
        return USER_ID;
    }
    public static Long ORG_ID(){
        return ORG_ID;
    }
    public static boolean IS_TEACHER(){
        return IS_TEACHER;
    }
    public static boolean IS_STUDENT(){
        return IS_STUDENT;
    }
    public static String ORG_NAME(){
        return ORG_NAME;
    }
    public static String ORG_CODE(){
        return ORG_CODE;
    }
    public static String USER_NAME(){
        return USER_NAME;
    }
    public static String USER_NO(){
        return USER_NO;
    }
    public static String DEP_CODE(){
        return DEP_CODE;
    }
    public static String DEP_ID(){
        return DEP_ID;
    }
    public static String DEP_NAME(){
        return DEP_NAME;
    }
    public static String USER_AGENT(){
        return USER_AGENT;
    }
}
