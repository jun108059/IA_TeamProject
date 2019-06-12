package com.example.myapplication;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.content.Intent;
import android.text.InputType;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import android.os.Handler;

public class MainActivity extends AppCompatActivity {
    private Handler mHandler;

    private Socket socket;
    private BufferedReader socketIn;
    private PrintWriter socketOut;
    private BufferedReader networkReader;
    private BufferedWriter networkWriter;

    private String ip = "54.180.142.83"; // IP
    private int port = 9999; // PORT번호

    EditText editId, editPwd;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try{
            socket = new Socket(ip ,port);
            socketIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            socketOut = new PrintWriter(socket.getOutputStream(), true);
        }
        catch (Exception e){
            e.printStackTrace();
        }   //서버와 연결시작

        socketOut.println("yes");//페이지 알림

        Button loginbutton=(Button)findViewById(R.id.login);
        editId = (EditText) findViewById(R.id.id);
        editPwd = (EditText) findViewById(R.id.pwd);

        loginbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick (View view){
                String id_s = editId.getText().toString();
                String pwd_s = editPwd.getText().toString();
                if(id_s.equals("shopporter") && pwd_s.equals("1234")) {
                    Intent intent = new Intent(getApplicationContext(), MenuActivity.class);
                    startActivity(intent);
//                    socketOut.println(id_s); //서버로 메세지 보내기
                }
                else{
                    Toast.makeText(MainActivity.this, "아이디와 암호를 확인해주세요.", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}
