package com.dyhhhhh.bean;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 观看视频传递参数
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ReadVideoBean {
    private int start;
    private int end;
}
