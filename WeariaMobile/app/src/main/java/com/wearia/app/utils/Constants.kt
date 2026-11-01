package com.wearia.app.utils

object Constants {
    // Adresse IP de votre PC sur votre réseau Wi-Fi local pour téléphone réel (INFINIX) :
    const val BASE_URL = "http://192.168.1.113:8000/"

    // Si vous utilisez un émulateur Android (AVD), utilisez : "http://10.0.2.2:8000/"
    // Si vous utilisez adb reverse (USB) : "http://localhost:8000/"

    const val PREFS_NAME = "wearia_prefs"
    const val KEY_TOKEN = "jwt_token"
    const val KEY_USER_ID = "user_id"
    const val KEY_USER_NAME = "user_name"
    const val KEY_USER_EMAIL = "user_email"

    fun getFullImageUrl(relativePath: String): String {
        return if (relativePath.startsWith("http")) {
            relativePath
        } else {
            val cleanPath = relativePath.removePrefix("/")
            "$BASE_URL$cleanPath"
        }
    }
}
