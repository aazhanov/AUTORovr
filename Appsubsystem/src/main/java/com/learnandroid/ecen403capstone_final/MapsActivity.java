package com.learnandroid.ecen403capstone_final;


import static android.content.ContentValues.TAG;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.FragmentActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.maps.GeoApiContext;
import com.google.maps.PendingResult;
import com.google.maps.DirectionsApiRequest;
import com.google.maps.internal.PolylineEncoding;
import com.google.maps.model.DirectionsResult;
import com.google.maps.model.DirectionsRoute;
import com.google.maps.model.TravelMode;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.maps.PlacesApi;

import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.PopupWindow;
import android.widget.RelativeLayout;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.maps.model.PlaceDetails;
//import com.google.maps.model.PlaceResult;
import com.google.maps.model.PlacesSearchResponse;
import com.google.maps.model.RankBy;
import com.learnandroid.ecen403capstone_final.databinding.ActivityMapsBinding;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback, GoogleMap.OnMapClickListener{

    private GoogleMap mMap;

    private ActivityMapsBinding binding;
    private EditText lat = null;
    double latitude = 0;
    boolean clickable = false;
    boolean start = true;
    private String distance = "";
    double longitude = 0;
    private EditText lng = null;

    boolean nochange = false;
    private Marker marker;

    TextView text, text2;
    String l = null;
    String q = null;

    private Marker dest = null;
    boolean invalid = false;

    Polyline polyline = null;

    private Boolean caldirections = true;

    private LatLng begin = new LatLng(30.62133, -96.33927);

    private String line = "";

    private LatLng latlng;

    private GeoApiContext mGeoApiContext = new GeoApiContext.Builder()
            .apiKey("AIzaSyCYnKDDS82O-oP8ZdNHyAAEY41x3zn0Cwc")
            .build();
    //creating mGeoApiContext so that I can use the directions function
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //Creating the map
        binding = ActivityMapsBinding.inflate(getLayoutInflater());

        setContentView(binding.getRoot());

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        final Button button = (Button) findViewById(R.id.button1);
        //Creating the "Plot Route" button
        text = findViewById(R.id.distanceview);
        text2 = findViewById(R.id.send);
        //Creating the textview that shows distance

        final Button button2 = (Button) findViewById(R.id.button2);
        //Creating second button

        final Button button3 = (Button) findViewById(R.id.button3);

        // Set an OnClickListener on the button to show the popup when it is pressed
        button.setOnClickListener(new View.OnClickListener() {
            //When clicked, this is what will happen
            public void onClick(View v) {
                invalid = false;
                text2.setText("");
                //this is if the lattitude and longitude is given a false input
                lat = findViewById(R.id.editTextTextPersonName);
                lng = findViewById(R.id.editTextTextPersonName2);
                   if (start == true){
                       l = lat.getText().toString();
                       q = lng.getText().toString();
                       System.out.println("Working");
                   }

                   if ((l.equals(lat.getText().toString()) && q.equals(lng.getText().toString())) && clickable == false && start == false) {
                       nochange = true;
                       System.out.println("Here");
                   }
                    if (dest != null && clickable == false && !nochange ) {
                        dest.remove();
                        line = "";
                        // This is if a route is already plotted, it will remove the destination marker
                    }
                    if (polyline != null && !nochange) {
                        polyline.remove();
                        //This is for the actual polyline getting removed
                    }

                //Getting the latitude and longitude
                if ((!(lat.getText().toString().isEmpty() || lng.getText().toString().isEmpty())) && clickable == false && !nochange) {
                    //Checking if the latitude and longitude is empty and if the marker wasn't created by tapping on the screen
                    try {
                        //Created a try catch so that if an invalid character is put as the lat or lng it will say "Invalid Input" on the app
                        latitude = Double.parseDouble(lat.getText().toString());
                        longitude = Double.parseDouble(lng.getText().toString());
                        //Getting the values for lat and lng
                        if (latitude > 90 || latitude < -90 || longitude > 180 || longitude < -180){
                            //This if statement is if the values are not in the range of lat and lng
                            text.setTextColor(Color.parseColor("#FFFF0000"));
                            //Change color to red
                            text.setText("Invalid input");
                            //Set text to Invalid input
                            invalid = true;
                            //set invalid to true
                        }
                    } catch (Exception e) {
                        //If not an acceptable character
                        text.setTextColor(Color.parseColor("#FFFF0000"));
                        //set color to red
                        text.setText("Invalid input");
                        //set text to invalid input
                        invalid = true;
                        //set invalid to true
                    }


                    if (invalid == false) {
                        //If the lat and lng point is valid
                        latlng = new LatLng(latitude, longitude);
                        //create a new latlng
                        dest = mMap.addMarker(new MarkerOptions().position(latlng).title("Destination"));
                        //addmarker as the destination
                        float zoomLevel = 16.0f;
                        //zoom in
                        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(latlng, zoomLevel));
                        //move the camera so that it goes to where the destination is
                        function(marker, dest);
                        //call to the function that creates and plots the route
                    }

                } else if (dest != null && clickable == true ) {
                    //if the marker was clicked on the map instead of the input
                    function(marker, dest);
                    //call the function
                }
                dest.showInfoWindow();
                l = lat.getText().toString();
                q = lng.getText().toString();
                //reset the clickable so that it doesn't mess up the route removal/creation
                start = false;
                nochange = false;
                Handler handler = new Handler();
                //Create a handler so that we can show the distance of the route
                handler.postDelayed(new Runnable() {
                    //Delay is so that the route can be calculated and the distance can be shown.
                    @Override
                    public void run() {
                        if (invalid == false ) {
                            //If the route is valid
                            if (caldirections == false) {
                                //If the direction is not calculated
                                text.setTextColor(Color.parseColor("#FFFF0000"));
                                //Change color to red
                                text.setText("Failed to get directions");
                                //change the text
                                caldirections = true;
                                //reset the caldirections bool
                            } else {
                                String newstr = distance.replaceAll("[^A-Za-z]+", "");
                                //Go through the distance (which will be in the format # mi or # ft) and remove the numbers
                                //This is to see if the distance is in ft or miles
                                Pattern regex = Pattern.compile("(-?\\d+(?:\\.\\d+)?)");
                                //Get all the numbers
                                Matcher matcher = regex.matcher(distance);
                                //Create a matcher that matches all the patterns in a string
                                //create the matcher
                                double compare = 0;
                                //create a double to convert everything to miles
                                while (matcher.find()) {
                                    compare = Double.parseDouble(matcher.group(1));
                                    //when the matcher finds the pattern in a string, make it the compare varible
                                }
                                if (newstr.equals("ft")) {
                                    compare = compare / 5280;
                                    //if the distance is in ft, convert to miles
                                }
                                if (compare > 2.0) {
                                    //if the distance is greater than 2 miles, make the color red to show that it might be too far
                                    text.setTextColor(Color.parseColor("#FFFF0000"));
                                } else {
                                    //make color black
                                    text.setTextColor(Color.parseColor("#FF000000"));
                                }
                                if (!distance.equals("")) {
                                    //If there is a distance, show it to user
                                    text.setText("Distance is " + distance);
                                }
                            }
                        }
                    }
                }, 1500);// delay of 1 sec so that the app is able to calculate the route
                clickable = false; //make the varible clickable flase so that the maponclicklistener resets
            }


        });

        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if (line == "") {
                    //If the string is empty, it means the route was not plotted
                    text2.setText("Please Plot Valid Route");
                    //make color red
                    text2.setTextColor(Color.parseColor("#FFFF0000"));
                }
                    else if (invalid == false) {
                    //This will be for sending nodes to rover
                    System.out.println(line);
                    //Make color black, and tell the user that it worked
                    text2.setTextColor(Color.parseColor("#FF000000"));
                    text2.setText("Sent Successfully!");
                }

            }

        });

        button3.setOnClickListener(new View.OnClickListener() { //Reset button
            @Override
            public void onClick(View v) {
                if (polyline != null) {
                    //If there is a polyline, remove it
                    polyline.remove();
                }
                if (dest != null) {
                    //If there is a destination marker, remove it
                    dest.remove();
                }
                float zoomLevel = 16.0f;
                //make the zoom 16.0f
                mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(begin, zoomLevel));
                //Reset the camera
                text.setText("");
                //Set all the text back to default
                text2.setText("");
                distance = "";

                if (start == false) {
                    //If not false
                    lat.setText("");
                    lng.setText("");
                }
                start = true;
                line = "";
                //Make the start var = true
            }
        });

    }

    private void function(Marker start, Marker end) {
        DirectionsApiRequest directions = new DirectionsApiRequest(mGeoApiContext);
        //Use this functions call to use the google maps directions api

        com.google.maps.model.LatLng beginning = new com.google.maps.model.LatLng(
                //make the latlng equal the starting LatLng
                start.getPosition().latitude,
                start.getPosition().longitude
        );

        com.google.maps.model.LatLng destination = new com.google.maps.model.LatLng(
                //Make the destination the destination the user plots
                end.getPosition().latitude,
                end.getPosition().longitude
        );

        double enddesinationslat = end.getPosition().latitude;
        double enddestinationlong = end.getPosition().longitude;
        double startdestinationlat = start.getPosition().latitude;
        double startdestinationlong = start.getPosition().longitude;
        directions.alternatives(false);
        //No alternative routes, since it's a rover we want the best route
        directions.origin(beginning);
        //make the origin the beginning latlng
        directions.mode(TravelMode.WALKING);
        //Make the travelmode walking so that the rover wouldn't go in the streets
        directions.destination(destination).setCallback(new PendingResult.Callback<DirectionsResult>() {
        //Call the directions API to calculate
            @Override
            public void onResult(DirectionsResult result) {
                //Once the result is completed
                String s = Arrays.toString(result.routes[0].legs[0].steps);
                //Get the steps needed to go about the route
                distance = result.routes[0].legs[0].distance.toString();
                // Get the distance from the route
                Pattern regex = Pattern.compile("(-?\\d+(?:\\.\\d+)?)");
                // Create a pattern that finds numbers
                Matcher matcher = regex.matcher(s);
                //Create a matcher that looks for that pattern
                String S = "";
                //A variable to store the numbers
                while (matcher.find()) {
                    S += matcher.group(1) + "\n";
                    //Get all the numbers
                }
                // Parsing the data to get the correct inputs and outputs
                Scanner scanner = new Scanner(S);
                //
                line = startdestinationlat + " " + startdestinationlong + " ";
                //Put the starting latlng, because the
                int i = 1;
                while (scanner.hasNextLine()) {
                    if (i == 5 || i == 6 || i == 7 || i == 8 || i == 11 || i == 12) {
                        scanner.nextLine();
                    } else {
                        line += scanner.nextLine() + " ";
                    }
                    // process the line
                    if (i == 12) {
                        i = 6;
                    }
                    i++;
                }
                line += enddesinationslat + " " + enddestinationlong;
                scanner.close();
                System.out.println(s);
                //Close the scanner
                addPolylinesToMap(result);
                //add the route to the app
            }

            @Override
            public void onFailure(Throwable e) {
                caldirections = false;
                //If not able to make directions
            }
        });

    }

    private void addPolylinesToMap(final DirectionsResult result) {
        //Create a handler that runs if successful result
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override
            public void run() {
                for (DirectionsRoute route : result.routes) {
                    //Creating a loop that goes through all the routes
                    List<com.google.maps.model.LatLng> decodedPath = PolylineEncoding.decode(route.overviewPolyline.getEncodedPath());
                    //Creating a list of the decoded path that the route creates
                    List<LatLng> newDecodedPath = new ArrayList<>();
                    //Creating a new list of latlngs in a route that will be added to the app


                    for (com.google.maps.model.LatLng latLng : decodedPath) {
                        //Creating another loop to go through the list of decoded paths
                        newDecodedPath.add(new LatLng(
                                //Create a path that get added to the app
                                latLng.lat,
                                latLng.lng
                        ));
                    }
                    polyline = mMap.addPolyline(new PolylineOptions().addAll(newDecodedPath));
                    //Add the path to the map
                }
            }
        });
    }
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        //Create a varible for the map
        marker = mMap.addMarker(new MarkerOptions().position(begin).title("Rover"));
        marker.showInfoWindow();
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
    public void onMapClick(@NonNull LatLng latLng)
    {
        //When the map is clicked
        if (dest != null){
            //If there is a destination, remove it and reset the string
            dest.remove();
            line = "";
        }
        if (polyline != null){
            //Remove the polyline
            polyline.remove();
        }
        dest = mMap.addMarker(new MarkerOptions()
                //Create a new marker at where the user clicked
                .title("Destination")
                .position(latLng));
        dest.showInfoWindow();
        //set the variable clickable to true so that when plotting, it won't plot the lat and lng points
        clickable = true;
    }
}