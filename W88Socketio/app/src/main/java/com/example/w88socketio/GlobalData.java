package com.example.w88socketio;

public class GlobalData {
    private static String userId;

    public static String getUserId() {
        return userId;
    }

    public static void setUserId(String newUserId) {
        userId = newUserId;
    }
}

