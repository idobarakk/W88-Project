package com.example.w88socketio;

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
import java.io.*;






// Example in MainActivity.java
public class MainActivity extends AppCompatActivity {
    private Socket mSocket;
    private EditText inputText;
    private TextView responseView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        inputText = findViewById(R.id.inputText);
        Button sendButton = findViewById(R.id.sendButton);
        responseView = findViewById(R.id.responseView);

        try {
            mSocket = IO.socket("http://10.0.2.2:5000");
            mSocket.connect();
        } catch (URISyntaxException e) {
            e.printStackTrace();
            Log.e("SocketIO", "Error", e);
        }

        sendButton.setOnClickListener(v -> {
            Log.d("socketio","clicked");
            String message = inputText.getText().toString();
            Log.d("socketio",message);
            mSocket.emit("message", message);
        });

        mSocket.on("message", args -> runOnUiThread(() -> {
            JSONObject data = (JSONObject) args[0];
            try {
                String response = data.getString("message");
                responseView.setText(response);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("SocketIO", "Error", e);
            }
        }));
    }
}
