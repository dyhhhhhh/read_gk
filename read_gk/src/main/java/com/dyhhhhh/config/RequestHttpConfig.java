package com.dyhhhhh.config;

import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONWriter;
import com.dyhhhhh.apis.MyCoursesApi;
import com.dyhhhhh.common.PersonalInformation;
import lombok.AllArgsConstructor;
import lombok.Data;
import okhttp3.*;
import org.jetbrains.annotations.NotNull;

import java.io.IOException;
import java.sql.SQLOutput;
import java.util.Objects;

/**
 * 发送请求
 */
@Data
public class RequestHttpConfig {
    //头部信息
    private final static String USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0";
    private static final String cookie = PersonalInformation.getCookie();
    private static RequestHttpConfig requestHttpConfig;
    private RequestHttpConfig() {

    }
    public static synchronized RequestHttpConfig getInstance(){
        if (requestHttpConfig == null){
            requestHttpConfig = new RequestHttpConfig();
        }
        return requestHttpConfig;
    }
    //get请求
    public String startGet(String url,String str) throws IOException {
        OkHttpClient okHttpClient = new OkHttpClient();
        //返回request对象
        Request request = new Request.Builder().url(url + str)
                .addHeader("cookie",cookie)
                .addHeader("user-agent",USER_AGENT)
                .get()
                .build();
        Response response = okHttpClient.newCall(request).execute();
        System.out.println(request);
        return Objects.requireNonNull(response.body()).string();
    }
    //post请求
    public String startPost(String url,String str,Object body) throws IOException{
        OkHttpClient okHttpClient = new OkHttpClient();
        //创建请求体
        MediaType mediaType = MediaType.parse("application/json; charset=UTF-8");
        RequestBody requestBody = RequestBody.create(mediaType,JSON.toJSONString(body));
        //返回request对象
        Request request = new Request.Builder().url(url + str)
                .addHeader("cookie",cookie)
                .addHeader("accept", "application/json, text/javascript, */*; q=0.01")
                .addHeader("user-agent",USER_AGENT)
                .addHeader("content-type","application/json; charset=UTF-8")
                .post(requestBody)
                .build();
        Response response = okHttpClient.newCall(request).execute();
        return Objects.requireNonNull(response.body()).string();
    }
}
