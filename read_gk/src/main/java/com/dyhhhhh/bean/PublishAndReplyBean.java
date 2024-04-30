package com.dyhhhhh.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PublishAndReplyBean {
    private String title;
    private String content;
    private String category_id;
    private List<Object> uploads = new ArrayList<>();
}
