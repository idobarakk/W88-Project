import android.os.AsyncTask
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.take_care.R
import java.sql.Connection
import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.Statement




class MainActivity : AppCompatActivity() {

    private lateinit var resultText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        resultText = findViewById(R.id.resultText)
        val getButton: Button = findViewById(R.id.getButton)

        getButton.setOnClickListener {
            GetDataTask().execute()
        }
    }

    private inner class GetDataTask : AsyncTask<Void, Void, String>() {

        override fun doInBackground(vararg voids: Void): String {
            return try {
                // Load the JDBC driver
                Class.forName("com.mysql.cj.jdbc.Driver")

                // Replace with your actual database connection details
                val url = "jdbc:mysql://192.168.1.100:3306/take_care"
                val user = "root"
                val password = "123456"

                val connection: Connection = DriverManager.getConnection(url, user, password)
                val statement: Statement = connection.createStatement()

                // Execute a SELECT query
                val resultSet: ResultSet = statement.executeQuery("SELECT word FROM notifications LIMIT 1")

                if (resultSet.next()) {
                    resultSet.getString("word")
                } else {
                    "No data found"
                }
            } catch (e: Exception) {
                e.printStackTrace()
                "Error: " + e.message
            }
        }

        override fun onPostExecute(result: String) {
            resultText.text = result
        }
    }
}
