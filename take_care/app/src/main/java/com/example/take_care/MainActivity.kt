package com.example.take_care

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val getButton: Button = findViewById(R.id.getButton)
        val resultText: TextView = findViewById(R.id.resultText)

        getButton.setOnClickListener {
            // Handle the "Get" button click
            resultText.text = "ziv"
        }
    }
}
