package com.wearia.app.data.local

import android.content.Context
import android.content.SharedPreferences
import com.wearia.app.utils.Constants

class SessionManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences(Constants.PREFS_NAME, Context.MODE_PRIVATE)

    fun saveSession(token: String, userId: Int, userName: String, email: String) {
        prefs.edit().apply {
            putString(Constants.KEY_TOKEN, token)
            putInt(Constants.KEY_USER_ID, userId)
            putString(Constants.KEY_USER_NAME, userName)
            putString(Constants.KEY_USER_EMAIL, email)
            apply()
        }
    }

    fun getToken(): String? = prefs.getString(Constants.KEY_TOKEN, null)

    fun getUserId(): Int = prefs.getInt(Constants.KEY_USER_ID, -1)

    fun getUserName(): String = prefs.getString(Constants.KEY_USER_NAME, "Utilisateur") ?: "Utilisateur"

    fun getUserEmail(): String? = prefs.getString(Constants.KEY_USER_EMAIL, null)

    fun isLoggedIn(): Boolean = !getToken().isNullOrEmpty()

    fun clearSession() {
        prefs.edit().clear().apply()
    }
}
