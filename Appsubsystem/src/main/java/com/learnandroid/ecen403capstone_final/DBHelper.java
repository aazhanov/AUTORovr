package com.learnandroid.ecen403capstone_final;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import androidx.annotation.Nullable;

//Creating a db helper class so that we can use the database
public class DBHelper extends SQLiteOpenHelper {
    public static final String DBNAME = "Login.db";
    //Create the name
    public String[] keys = {"q123w21", "qei3uUs3-r", "a1s2f3gte4"};
    public int[] portnum = {1111, 1112, 1113};

    //Create the keys and portnumbers for the activation keys
    public DBHelper(Context context) {
        super(context, "Login.db", null, 1);
    }
    //make the DB helper

    @Override
    public void onCreate(SQLiteDatabase MyDB) {
        MyDB.execSQL("create Table userspasskey(username TEXT primary key, password TEXT, actkey TEXT, port INT)");
        //Create a database that has 4 rows for username, password, activationkey, and portnumber
        ContentValues contentValues= new ContentValues();
        //Creating a blank initial set of values
    }
    @Override
    public void onUpgrade(SQLiteDatabase MyDB, int i, int i1) {

        MyDB.execSQL("drop Table if exists userspasskey");
        //If used, remove the table if it exists
    }

    public Boolean insertdata(String username, String password, String actkey, int portnum){
        //Created function to insert data into the database
        SQLiteDatabase MyDB = this.getWritableDatabase();
        //Create a writable database
        ContentValues contentValues= new ContentValues();
        //Creating a blank initial set of values
        contentValues.put("username", username);
        contentValues.put("password", password);
        contentValues.put("actkey", actkey);
        contentValues.put("port", portnum);
        //Insert all the varibles
        long result = MyDB.insert("userspasskey", null, contentValues);
        //Create varible to see if fails
        if(result==-1) {
            //If fails, return false
            return false;
        }
        else{
            //If successful, return true
            return true;
        }
    }

    public Boolean checkusr(String username) {
        //This is to check if the username exists
        SQLiteDatabase MyDB = this.getWritableDatabase();
        //Get the database
        Cursor cursor = MyDB.rawQuery("Select * from userspasskey where username = ? ", new String[]{username});
        //Create a cursor that looks and sees if the database has the username already in the database
        if (cursor.getCount() > 0)
            //If the username is in the database, return true
            return true;
        else
            //If not, return false
            return false;
    }

    public Boolean checkusrandpass(String username, String password) {
        //Check to see if the username matches with the password in the database
        SQLiteDatabase MyDB = this.getWritableDatabase();
        //Get the database
        Cursor cursor = MyDB.rawQuery("Select * from userspasskey where username = ? and password = ?", new String[]{username, password});
        //Create a cursor that looks and sees if the database has the username and password that match in the database
        if (cursor.getCount() > 0)
        {
            //If it does exist
            return true;
    }
        else {
            //If not
            return false;
        }
    }
    public Boolean activationkey(String activationkey){
        //Check to see if the activation key exists in the database
        SQLiteDatabase MyDB = this.getWritableDatabase();
        //Get the database
        Cursor cursor = MyDB.rawQuery("Select * from userspasskey where actkey = ?", new String[]{activationkey});
        //Create a cursor that looks and sees if the database has the actkey already in the database
        if(cursor.getCount()>0){
            //If it does exist, return true
            return true;
        }//If not,return false
        return false;
    }
}