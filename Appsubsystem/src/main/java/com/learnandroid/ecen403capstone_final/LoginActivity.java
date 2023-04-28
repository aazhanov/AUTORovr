package com.learnandroid.ecen403capstone_final;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.learnandroid.ecen403capstone_final.DBHelper;
import com.learnandroid.ecen403capstone_final.R;

public class LoginActivity extends AppCompatActivity {
    EditText Username, Password;
    Button login;
    TextView text;
    DBHelper DB;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        //Create the login page

        Username = (EditText) findViewById(R.id.username1);
        Password = (EditText) findViewById(R.id.password1);
        login = (Button) findViewById(R.id.btnsignin1);
        text = (TextView) findViewById(R.id.textView2);

        //Set the username, password, and login button
        DB = new DBHelper(this);
        //Use the DBHelper to access the database
        login.setOnClickListener(new View.OnClickListener() {
            //Set a listener for the button
            @Override
            public void onClick(View view) {
                //When the button is clicked, get the username and password to string
                String user = Username.getText().toString();
                String pass = Password.getText().toString();
                text.setTextColor(Color.parseColor("#FFFF0000"));
                if(user.equals("")||pass.equals("")) {
                    text.setText("Please enter all the fields");
                    //If the username or password is blank, let the user know
                }
                else{
                    Boolean checkuserpass = DB.checkusrandpass(user, pass);
                    //If not, check the username and password and make sure it lines up with the one in the database
                    if(checkuserpass==true){
                        //if it does, tell the user
                        text.setTextColor(Color.parseColor("#009150"));
                        text.setText("Sign in successful");
                        //Create intent, and start the mapsactivity
                        Intent intent  = new Intent(LoginActivity.this, MapsActivity.class);
                        startActivity(intent);
                    }else{
                        //If it doesn't work, tell the user
                        text.setText("Invalid Credentials");
                    }
                }
            }
        });

    }
}