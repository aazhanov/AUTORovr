package com.learnandroid.ecen403capstone_final;
import static android.content.ContentValues.TAG;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.TextView;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    EditText username, password, akey;
    TextView update;
    Button signup, signin;
    int q = 0;
    Boolean unique = true;
    DBHelper DB;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Set up all the buttons, edittexts,and textview from the xml file
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        akey = (EditText) findViewById(R.id.actkey);
        signup = (Button) findViewById(R.id.btnsignup);
        signin = (Button) findViewById(R.id.btnsignin);
        DB = new DBHelper(this);
        update = (TextView) findViewById(R.id.textView);

        //Create a listener for the signup button
        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Create varibles that get the string in the
                String user = username.getText().toString();
                String pass = password.getText().toString();
                String actkey = akey.getText().toString();
                update.setTextColor(Color.parseColor("#FFFF0000"));
                if (user.equals("") || pass.equals("") || actkey.equals("")) {
                    update.setText("Please enter all the fields");
                    //If any of the fields are not filled, let the user know
                }
                else {
                    Boolean checkuser = DB.checkusr(user);
                    if (checkuser == false) {
                            // If the username is not in the database
                        for (int i = 0; i < DB.keys.length; i++){
                            //go through all the keys
                            if(actkey.equals(DB.keys[i])){
                                //If the actkey is equal to one of the actkeys in the helper class
                                unique = false;
                                //Make the unique = false
                                q = i;
                                //This is for the portnum
                                break;
                            }
                        }
                        if (!unique) { //If the actkey does equal one of the ones in the dbhelper
                            Boolean checkactkey = DB.activationkey(actkey);
                            //Check to see if it is already in use
                            if (checkactkey == false){
                                //If not, insert the data in the database
                                Boolean insert = DB.insertdata(user, pass, actkey, DB.portnum[q]);
                                if (insert == true) {
                                    //If it works, tell the user and start the mapsactivity
                                    update.setTextColor(Color.parseColor("#009150"));
                                    update.setText("Registered Successfully");
                                   // Intent intent = new Intent(getApplicationContext(), MapsActivity.class);
                                    Intent intent = new Intent(MainActivity.this, MapsActivity.class);
                                    startActivity(intent);
                                }} else {
                                //If the activation key is in the databse, let the user know
                                update.setText("Activation Key in Use");
                            }
                        } else {
                            //If the actkey doesn't match up with the ones in the db helper
                            update.setText("Activation Key is wrong");
                        }
                    }
                    else {
                        //If the username is already in the database
                        update.setText("User already exists! please sign in");
                    }
                }
            }
        });
        //Create a listener for the sigin page
        signin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //If clicked, start the signin page
               // Intent intent = new Intent(getApplicationContext(), LoginActivity.class);
                Intent intent = new Intent(MainActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });
    }
}