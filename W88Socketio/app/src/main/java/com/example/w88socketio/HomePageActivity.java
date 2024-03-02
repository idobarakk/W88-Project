package com.example.w88socketio;

import static com.example.w88socketio.GlobalData.userId;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import io.socket.client.Socket;
import android.util.Log;
import android.view.View;
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
    private Button notificationButton;
    private TextView drugsTextView;
    private Button drugsButton;
    private Button activityButton1, activityButton2, activityButton3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_page);

        // Initialize UI components
        initializeUI();

        // Setup Socket.IO
        setupSocket();

        // Setup listeners for Socket.IO messages
        setupSocketListeners();

        // Setup button click listeners
        //setupButtonClickListeners();
    }

    private void initializeUI() {
        notificationTextView = findViewById(R.id.notificationTextView);
        notificationButton =findViewById(R.id.notificationButton);


        drugsTextView = findViewById(R.id.drugsTextView);
        drugsButton =findViewById(R.id.drugsButton);


        activityButton1 = findViewById(R.id.activityButton1);
        activityButton2 = findViewById(R.id.activityButton2);
        activityButton3 = findViewById(R.id.activityButton3);
    }

    private void setupSocket() {

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
    }

    private void setupSocketListeners() {
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
                }
                else if ("drugschedule".equals(type)) {
                    handleDrugSchedule(data.getJSONObject("data"));
                }
                else if ("activitiy".equals(type)) {
                    handleActivitiy(data.getJSONObject("data"));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }));
    }


    public void ringtone(){
        try {
            Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
            Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
            r.play();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void handleNotification(JSONObject data) {
        notificationTextView.setText("here notification id "+userId);
        notificationButton.setEnabled(true);
        notificationTextView.setVisibility(View.VISIBLE);
        notificationButton.setVisibility(View.VISIBLE);
        ringtone();
    }

    private void handleDrugSchedule(JSONObject data) {
        drugsTextView.setText("here drug id "+userId);
        drugsButton.setEnabled(true);
        drugsTextView.setVisibility(View.VISIBLE);
        drugsButton.setVisibility(View.VISIBLE);
        ringtone();

    }

    private void handleActivitiy(JSONObject data) {
        activityButton1.setEnabled(true);
        activityButton2.setEnabled(true);
        activityButton3.setEnabled(false);
    }

    // Additional methods for updating UI, handling navigation, etc.
}
