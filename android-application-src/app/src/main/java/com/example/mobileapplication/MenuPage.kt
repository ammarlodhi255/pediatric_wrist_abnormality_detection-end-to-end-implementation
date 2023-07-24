package com.example.mobileapplication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.view.Window
import android.view.WindowManager

class MenuPage : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestWindowFeature(Window.FEATURE_NO_TITLE)
        this.window.setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN)
        supportActionBar?.hide()
        setContentView(R.layout.activity_menu_page)
    }
    fun goToDICOM_Conversion(view : View){
        startActivity(Intent(this, DicomToPNG::class.java))
    }
    fun goToImageDetection(view : View){
        startActivity(Intent(this, ImageDetection::class.java))
    }
}