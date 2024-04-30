package com.dyhhhhh.apis;

import java.io.IOException;
import java.util.HashMap;

public interface Strategy {
    void execute(String activityId, HashMap<String, Object> activityDetails) throws Exception;
}
