package com.dyhhhhh.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;


@AllArgsConstructor
@NoArgsConstructor

/**
 * 查询所有课程的对象
 */
public class MyCoursesBean {
    //查询课程的参数
    //该参数代表查询所有
    private String conditions = "%7B%22status%22:%5B%22ongoing%22%5D,%22keyword%22:%22%22%7D";
    //要查询的字段
    private static final String fieIds = "id,name,course_code,department";
    //查询页码
    private int page = 1;
    //每页大小
    private int size = 10;

    @Override
    public String toString() {
        return "?conditions="+conditions+"&"
                +"fields="+fieIds+"&"
                +"page="+page+"&"
                +"page_size="+size;
    }

    public String getConditions() {
        return conditions;
    }

    public void setConditions(String conditions) {
        this.conditions = conditions;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }
}
