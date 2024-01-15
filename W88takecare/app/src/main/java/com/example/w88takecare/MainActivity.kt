package com.example.w88takecare

import android.R
import android.os.AsyncTask
import android.view.View
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import java.net.HttpURLConnection
import java.net.URL
import java.io.OutputStream


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val myButton = findViewById<Button>(R.id.Button)
        myButton.setOnClickListener { SendHttpRequestTask().execute() }
    }

    private class SendHttpRequestTask :
        AsyncTask<Void?, Void?, Void?>() {
        protected override fun doInBackground(vararg params: Void): Void? {
            try {
                val url = URL("http://192.116.98.97:5000")
                val conn = url.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json")
                conn.doOutput = true
                val jsonInputString = "{\"hello\": \"tomer\"}"
                conn.outputStream.use { os ->
                    val input =
                        jsonInputString.toByteArray(charset("utf-8"))
                    os.write(input, 0, input.size)
                }

                // Read response, handle it or log it
                // ...
                conn.disconnect()
            } catch (e: Exception) {
                e.printStackTrace()
            }
            return null
        }
    }
}

