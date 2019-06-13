package com.example.myapplication;

import android.content.Context;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Message;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import android.os.Handler;

public class CartActivity extends AppCompatActivity {
    private Handler myHandler;
    private Thread myThread;  //서버 환경 설정
    private Socket socket;
    private BufferedReader socketIn;
    private PrintWriter socketOut;
    private BufferedReader networkReader;
    private BufferedWriter networkWriter;
    TextView list;
    private String ip = "xxx.xxx.xxx.xxx"; // IP
    private int port = 9999; // PORT번호

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cart);

        Button backbutton = (Button) findViewById(R.id.back);
        Button completebutton = (Button) findViewById(R.id.complete);

        list = (TextView) findViewById(R.id.cart);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            socket = new Socket(ip, port);
            socketIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            socketOut = new PrintWriter(socket.getOutputStream(), true);
        } catch (Exception e) {
            e.printStackTrace();
        }   //서버와 연결시작

        socketOut.println("C");//페이지 알림

        myHandler = new Handler();
        myThread = new Thread();   //서버로부터 데이터를 받는 스레드
        myThread.start();   //스레드 시작

        class MyThread extends Thread {
            public void run() {
                while (true) {
                    try {
                        String data = socketIn.readLine();
                        list.setText(data);
                        //Message msg = myHandler.obtainMessage();
                        //msg.obj = data;
                        //myHandler.sendMessage(msg);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }

                }
            }
        }


        completebutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MenuActivity.class);
                startActivity(intent);
            }
        });
        backbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MenuActivity.class);
                startActivity(intent);
            }
        });
    }
}
