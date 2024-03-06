package com.example.w88socketio;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebView;
import android.widget.Button;

import java.net.URISyntaxException;

import io.socket.client.IO;
import io.socket.client.Socket;


public class Activity3 extends AppCompatActivity {
    private WebView webView;
    private Button ackFromAct3;
    private Socket mSocket;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_3);

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

        ackFromAct3 = findViewById(R.id.backfromact3);

        webView = (WebView) findViewById(R.id.webview3);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("https://h5p.org/h5p/embed/615");


        ackFromAct3.setOnClickListener(v -> {
            startActivity(new Intent(Activity3.this, HomePageActivity.class));
        });
    }
}