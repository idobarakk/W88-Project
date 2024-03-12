package com.example.w88socketio;


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



public class MainActivity extends AppCompatActivity {
    private Socket mSocket;
    private EditText usernameInput; // New username field
    private EditText passwordInput; // New password field
    private TextView responseView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        usernameInput = findViewById(R.id.usernameInput);
        passwordInput = findViewById(R.id.passwordInput);
        Button sendButton = findViewById(R.id.sendButton);
        responseView = findViewById(R.id.responseView);

        try {
            IO.Options opts = new IO.Options();
            opts.reconnection = true;
            opts.reconnectionAttempts = 10;
            opts.reconnectionDelay = 1000;
            //10.0.2.2
            mSocket = IO.socket("http://192.116.98.97:5000", opts);
            mSocket.connect();

            mSocket.on(Socket.EVENT_CONNECT, args -> Log.d("SocketIO", "Connected"));
            mSocket.on(Socket.EVENT_DISCONNECT, args -> Log.d("SocketIO", "Disconnected"));
            mSocket.on(Socket.EVENT_CONNECT_ERROR, args -> Log.e("SocketIO", "Connect Error", (Throwable) args[0]));

        } catch (URISyntaxException e) {
            e.printStackTrace();
            Log.e("SocketIO", "Connection error", e);
        }

        sendButton.setOnClickListener(v -> {
            JSONObject loginData = new JSONObject();
            try {
                loginData.put("type", "login");
                JSONObject data = new JSONObject();
                data.put("username", usernameInput.getText().toString());
                data.put("password", passwordInput.getText().toString());
                loginData.put("data", data);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            mSocket.emit("message", loginData.toString());
        });

        mSocket.on("message", args -> runOnUiThread(() -> {
            try {
                JSONObject data;
                if (args[0] instanceof String) {
                    // If args[0] is a String, parse it to JSONObject
                    data = new JSONObject((String) args[0]);
                } else {
                    // If args[0] is already a JSONObject, cast it directly
                    data = (JSONObject) args[0];
                }
                if(data.getString("type").equals("login_callback")) {
                    JSONObject loginData = data.getJSONObject("data");
                    String userId = loginData.optString("user_id");
                    boolean validPass = loginData.getBoolean("validpass");
                    boolean validUser = loginData.getBoolean("validuser");

                    if (!userId.equals("") && !userId.equals("null") && validUser && validPass) {
                        // Save userId globally and navigate to HomePage
                        GlobalData.setUserId(userId); // Assuming GlobalData is a class you create for global variables
                        startActivity(new Intent(MainActivity.this, HomePageActivity.class));
                    } else if (!validPass) {
                        responseView.setText("Wrong password");
                    } else if (!validUser) {
                        responseView.setText("User not found");
                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("SocketIO", "Error", e);
            }
        }));

    }
}
