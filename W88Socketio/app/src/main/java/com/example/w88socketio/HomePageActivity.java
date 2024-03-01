package com.example.w88socketio;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import io.socket.client.Socket;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Button;
import io.socket.client.IO;
import java.net.URISyntaxException;
import org.json.JSONObject;
import org.json.JSONException;

import android.os.Bundle;

public class HomePageActivity extends AppCompatActivity {
    private Socket mSocket;
    private TextView notificationTextView;
    private Button buttonAction1, buttonAction2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_page);

        notificationTextView = findViewById(R.id.notificationTextView);
        buttonAction1 = findViewById(R.id.buttonAction1);
        buttonAction2 = findViewById(R.id.buttonAction2);

        try {
            IO.Options opts = new IO.Options();
            opts.reconnection = true;
            opts.reconnectionAttempts = 10;
            opts.reconnectionDelay = 1000; // 1 second

            mSocket = IO.socket("http://10.0.2.2:5000", opts);
            mSocket.connect();

            mSocket.on(Socket.EVENT_CONNECT, args -> Log.d("SocketIO", "Connected"));
            mSocket.on(Socket.EVENT_DISCONNECT, args -> Log.d("SocketIO", "Disconnected"));
            mSocket.on(Socket.EVENT_CONNECT_ERROR, args -> Log.e("SocketIO", "Connect Error", (Throwable) args[0]));

        } catch (URISyntaxException e) {
            e.printStackTrace();
        }

        mSocket.on("message", args -> runOnUiThread(() -> {
            JSONObject data;
            try {
                if (args[0] instanceof String) {
                    // If args[0] is a String, parse it to JSONObject
                    data = new JSONObject((String) args[0]);
                } else {
                    // If args[0] is already a JSONObject, cast it directly
                    data = (JSONObject) args[0];
                }
                String type = data.getString("type");
                if ("notification".equals(type)) {
                    handleNotification(data.getJSONObject("data"));
                } else if ("drugschedule".equals(type)) {
                    handleDrugSchedule(data.getJSONObject("data"));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }));
    }
    private void handleNotification(JSONObject data) {
        // Extract data and update UI
        // ...

        buttonAction1.setText("I did it!");
        buttonAction1.setOnClickListener(v -> {
            // Send notification_callback with "took":"True"
            // ...
        });

        buttonAction2.setText("Remind me in 5 min");
        buttonAction2.setOnClickListener(v -> {
            // Send notification_callback with new time and "took":"false"
            // ...
        });
    }

    private void handleDrugSchedule(JSONObject data) {
        // Extract data and update UI
        // ...

        buttonAction1.setText("I took my drug!");
        buttonAction1.setOnClickListener(v -> {
            // Send drugschedule_callback with "took":"True"
            // ...
        });

        buttonAction2.setText("Remind me in 5 min");
        buttonAction2.setOnClickListener(v -> {
            // Send drugschedule_callback with new time and "took":"false"
            // ...
        });
    }
}