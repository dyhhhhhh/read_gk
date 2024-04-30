package com.dyhhhhh.common;

/**
 * 各个内容的类型
 */
public enum TypeEnum {
    PAGE("page"),
    VIDEO("online_video"),
    FORUM("forum"),
    WEB("web_link"),
    MATERIAL("material"),
    EXAM("exam");
    private String value;

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
    TypeEnum(String value){
        this.value = value;
    }
}
