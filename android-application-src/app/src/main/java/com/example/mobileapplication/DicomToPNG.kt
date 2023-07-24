package com.example.mobileapplication

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.view.Window
import android.view.WindowManager
import android.webkit.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat


class DicomToPNG : AppCompatActivity() {
    private lateinit var webView: WebView
    private var fileUploadCallback: ValueCallback<Array<Uri>>? = null
    private var fileUploadPermissionsCode = 1
    private var selectedFileUri: Uri? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestWindowFeature(Window.FEATURE_NO_TITLE)
        this.window.setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        )
        supportActionBar?.hide()
        setContentView(R.layout.activity_dicomtopng)
        webView = findViewById<View>(R.id.webView) as WebView
        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true
        webSettings.allowFileAccess = true
        webSettings.allowFileAccessFromFileURLs = true
        webSettings.allowUniversalAccessFromFileURLs = true
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = object : WebChromeClient() {
            override fun onShowFileChooser(
                webView: WebView?,
                filePathCallback: ValueCallback<Array<Uri>>?,
                fileChooserParams: FileChooserParams?
            ): Boolean {
                fileUploadCallback = filePathCallback
                if (ContextCompat.checkSelfPermission(
                        this@DicomToPNG,
                        Manifest.permission.READ_EXTERNAL_STORAGE
                    ) != PackageManager.PERMISSION_GRANTED
                ) {
                    ActivityCompat.requestPermissions(
                        this@DicomToPNG,
                        arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE),
                        fileUploadPermissionsCode
                    )
                } else {
                    openFileChooser()
                }
                return true
            }
        }
        val webpageUrl = resources.getString(R.string.server_url) + "/dicom_to_png_api_index"
        webView.loadUrl(webpageUrl)
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == fileUploadPermissionsCode) {
            if (resultCode == RESULT_OK) {
                selectedFileUri = data?.data
                fileUploadCallback?.onReceiveValue(arrayOf(selectedFileUri!!))
                fileUploadCallback = null
            } else {
                fileUploadCallback?.onReceiveValue(null)
                fileUploadCallback = null
            }
        }
    }

    private fun openFileChooser() {
        val intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.type = "application/dicom"
        intent.putExtra(Intent.EXTRA_MIME_TYPES, arrayOf("application/dicom", "application/octet-stream"))
        startActivityForResult(
            Intent.createChooser(intent, "Choose File"),
            fileUploadPermissionsCode
        )
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == fileUploadPermissionsCode) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                openFileChooser()
            } else {
                fileUploadCallback?.onReceiveValue(null)
                fileUploadCallback = null
            }
        }
    }
}