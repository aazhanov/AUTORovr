package com.learnandroid.AUTORover;
import static android.media.CamcorderProfile.get;

import androidx.annotation.NonNull;
import androidx.fragment.app.FragmentActivity;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.location.Address;
import android.location.Geocoder;
import android.os.Bundle;
import android.os.Handler;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.Type;
import java.net.Socket;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.List;
import java.util.Locale;

import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

//import com.google.maps.model.PlaceResult;
import com.google.android.gms.maps.model.PolylineOptions;
import com.learnandroid.AUTORover.databinding.ActivityMapsBinding;


public class MapsActivity extends FragmentActivity implements OnMapReadyCallback, GoogleMap.OnMapClickListener {

    private static GoogleMap mMap;

    private ActivityMapsBinding binding;
    boolean clickable = false;
    public static boolean send = false;

    SearchView searchView;

    public boolean kill = false;

    TextView text, text2;
    public String ipaddress = "null";

    boolean moving = false;

    public Marker dest = null;

    public String portnum = "q";

    public boolean go = false;

    public static Handler handler;

    public Polyline polyline = null;

    private LatLng begin = new LatLng(30.62133, -96.33927);

    public Marker loc = null;
    public static Double destinationlat = 0.0;
    public static Double destinationlong = 0.0;
    public static AlertDialog dialog; // Reference to the AlertDialog
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //Creating the map
        binding = ActivityMapsBinding.inflate(getLayoutInflater());

        setContentView(binding.getRoot());

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
        Intent intent = getIntent();
        // Retrieve data from the Intent
        ipaddress = intent.getStringExtra("com.learnandroid.ecen403capstone_final.ip");
        portnum = intent.getStringExtra("com.learnandroid.ecen403capstone_final.port");
        searchView = findViewById(R.id.search_bar);
        final Button button = (Button) findViewById(R.id.button1);
        //Creating the "Plot Route" button
        text = findViewById(R.id.distanceview);
        text2 = findViewById(R.id.send);
        text.setTypeface(text.getTypeface(), Typeface.BOLD);
        text2.setTypeface(text2.getTypeface(), Typeface.BOLD);
        //Creating the textview that shows distance
        final Button button2 = (Button) findViewById(R.id.button2);
        //Creating second button
        final Button button3 = (Button) findViewById(R.id.button3);
        handler = new Handler();
        final Button button4 = (Button) findViewById(R.id.go);
        final Button helpbutton = (Button) findViewById(R.id.help);
        //showPopup();
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                if (dest != null) {
                    send = true;
                }
                else{
                    text2.setText("No destination");
                    text2.setTextColor(Color.parseColor("#F01E2C"));
                }
            }

        });
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (moving) {
                    kill = true;
                }
                else{
                    text2.setText("Rover is not moving");
                    text2.setTextColor(Color.parseColor("#F01E2C"));
                }
            }});
        button3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (dest != null) {
                    dest.remove();
                    dest = null;
                }
                if (polyline != null) {
                    polyline.remove();
                    polyline = null;
                }
                text2.setText("");

            }
        });
        button4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (polyline == null){
                    text2.setText("No Route created");
                    text2.setTextColor(Color.parseColor("#F01E2C"));
                }
                else{
                    go = true;
                }
            }
        });
        helpbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showPopup();
            }
        });
        searchView.clearFocus();
        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                String location = searchView.getQuery().toString();
                List<Address> addressList = null;
                if(location == null){
                    Toast.makeText(MapsActivity.this, "Location Not Found", Toast.LENGTH_SHORT).show();
                }
                else {
                    Geocoder geocoder = new Geocoder(MapsActivity.this, Locale.getDefault());

                    try {
                        addressList = geocoder.getFromLocationName(location,1);
                        Address address = addressList.get(0);
                        LatLng latLng = new LatLng (address.getLatitude(),address.getLongitude());
                        if (dest == null) {
                            dest = mMap.addMarker(new MarkerOptions().position(latLng).title("Destination"));
                        }
                        else{
                            dest.setPosition(latLng);
                        }
                        //dest = mMap.addMarker(new MarkerOptions().position(latLng).title("Destination"));
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(latLng, 16f));
                        dest.showInfoWindow();
                        destinationlat = dest.getPosition().latitude;
                        destinationlong = dest.getPosition().longitude;

                    } catch(Exception e) {
                        System.out.println("Search Error");
                        text2.setTextColor(Color.parseColor("#F01E2C"));
                        text2.setText("Invalid Place");

                    }
                }

                return false;
            }

            @Override
            public boolean onQueryTextChange(String newText) {
                return false;
            }
        });
        mapFragment.getMapAsync(this);
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                new ClientThread().start();
                text.setText("Connecting to Rover");
                text.setTextColor(Color.parseColor("#F01E2C"));
            }
        }, 5000);
    }

    public void showPopup() {
        // Create a dialog builder
        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        // Inflate the custom layout for the dialog
        LayoutInflater inflater = getLayoutInflater();
        View dialogView = inflater.inflate(R.layout.popup_layout, null);

        // Customize the dialog view (e.g., set text or handle button clicks)
        TextView textView = dialogView.findViewById(R.id.textView);

        // Set the custom view for the dialog
        builder.setView(dialogView);

        // Create and show the AlertDialog
        dialog = builder.create();
        dialog.show();

    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        //Create a varible for the map
        // marker = mMap.addMarker(new MarkerOptions().position(begin).title("Rover"));
        //marker.showInfoWindow();
        //add marker for the starting position
        float zoomLevel = 16.0f;
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(begin, zoomLevel));
        //move camera to starting position
        googleMap.getUiSettings().setZoomControlsEnabled(true);
        googleMap.getUiSettings().setZoomGesturesEnabled(true);
        //Set all teh UI settings for the user
        mMap.setOnMapClickListener(this);
        //Create a clicklistener for the map so that when clicked, it will know and we will be able to tell it what to do when clicked

    }


    @Override
    public void onMapClick(@NonNull LatLng latLng) {
        //When the map is clicked
        //if (dest != null) {
            //If there is a destination, remove it and reset the string
        //    dest.remove();
            //line = "";
       // }
        if (dest == null){
            dest = mMap.addMarker(new MarkerOptions()
                    //Create a new marker at where the user clicked
                    .title("Destination")
                    .position(latLng));
        }
        else{
            dest.setPosition(latLng);
        }
        if (polyline != null) {
            //Remove the polyline
            polyline.remove();
        }
        dest.showInfoWindow();
       // dest = mMap.addMarker(new MarkerOptions()
                //Create a new marker at where the user clicked
       //         .title("Destination")
        //        .position(latLng));
        text2.setText("");
        //set the variable clickable to true so that when plotting, it won't plot the lat and lng points
        clickable = true;
        destinationlat = dest.getPosition().latitude;
        destinationlong = dest.getPosition().longitude;
    }

    public static void dismissPopup() {
        // Dismiss the AlertDialog if it is showing
        if (dialog != null && dialog.isShowing()) {
            dialog.dismiss();
        }
    }


    private class ClientThread extends Thread {

        private Socket socket;
        public PrintWriter out;
        public BufferedReader in;

        @Override
        public void run() {
            boolean connected = false;
            while (!connected) {
                try (Socket socket1 = new Socket(ipaddress, Integer.parseInt(portnum))) {
                    System.out.println("Connected");
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            text.setText("Connected!");
                            text.setTextColor(Color.parseColor("#234F1E"));
                        }
                    });
                    out = new PrintWriter(socket1.getOutputStream(), true);
                    in = new BufferedReader(new InputStreamReader(socket1.getInputStream()));
                    String str = null;
                        while (true) {
                            if (kill) {
                                out.println("kill");
                                kill = false;
                            }
                            if (go){
                                out.println("go");
                                go = false;
                                runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        text2.setText("Going!");
                                        text2.setTextColor(Color.parseColor("#234F1E"));
                                    }
                                });
                                moving = true;
                            }
                            str = in.readLine();
                            System.out.println("Server Says: " + str);
                            if (str != null) {
                               /* if (str.equals("sent")) {
                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                        text2.setText("Sent Successfully!");
                                    }
                                    });
                                }*/
                                if (str.length() > 50){
                                    showroute(str);
                                }
                                else {

                                    String[] numberStrings = str.split("\\s+");
                                    double GPSLat = Double.parseDouble(numberStrings[0]);
                                    double GPSLong = Double.parseDouble(numberStrings[1]);
                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            //Add a marker on the map
                                            if (mMap != null) {
                                                LatLng markerLocation = new LatLng(GPSLat, GPSLong);
                                                if (loc == null) {
                                                    loc = mMap.addMarker(new MarkerOptions().position(markerLocation).title("Rover").icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_MAGENTA)));
                                                } else {
                                                    loc.setPosition(markerLocation);
                                                }
                                                mMap.animateCamera(CameraUpdateFactory.newLatLng(markerLocation));
                                                //loc.showInfoWindow();

                                            }
                                        }
                                    });
                                }
                            }
                            if (MapsActivity.send == true) {
                                // LatLng qwert = dest.getPosition();
                                if (str != null || !(str.equals("sent"))) {
                                    out.println(str + " " + MapsActivity.destinationlat.toString() + " " + MapsActivity.destinationlong.toString());
                                    System.out.println(str + " " + MapsActivity.destinationlat.toString() + " " + MapsActivity.destinationlong.toString());
                                    MapsActivity.send = false;
                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            text2.setText("Creating Route");
                                            text2.setTextColor(Color.parseColor("#234F1E"));
                                        }
                                    });
                                }
                            }
                        }
                    } catch(IOException e){
                        System.out.println("ERROR");
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                            text.setText("ERROR: Reconnecting Now");
                            text.setTextColor(Color.parseColor("#F01E2C"));
                        }
                        });
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException ex) {
                        ex.printStackTrace();
                    }
                }

            }
        }
        private void showroute(String route){
            String[] parts = route.split(" ");

            PolylineOptions polylineOptions = new PolylineOptions();
            for (int i = 0; i < parts.length; i += 2) {
                double longitude = Double.parseDouble(parts[i]);
                double latitude = Double.parseDouble(parts[i + 1]);
                LatLng latLng = new LatLng(latitude, longitude);

                polylineOptions.add(latLng);
            }

            // Add polyline to the map
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    polyline = mMap.addPolyline(polylineOptions);
                    text2.setText("Route Created!");
                    text2.setTextColor(Color.parseColor("#234F1E"));
                }
            });
        }
    }

}