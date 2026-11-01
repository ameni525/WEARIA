package com.wearia.app.viewmodel

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.wearia.app.data.local.SessionManager
import com.wearia.app.data.remote.RetrofitClient
import com.wearia.app.data.repositories.AuthRepository
import com.wearia.app.data.repositories.ClothingRepository
import com.wearia.app.data.repositories.RecommendationRepository
import com.wearia.app.data.repositories.RoutineRepository

class ViewModelFactory(private val context: Context) : ViewModelProvider.Factory {

    private val apiService by lazy { RetrofitClient.getInstance(context) }
    private val sessionManager by lazy { SessionManager(context) }

    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return when {
            modelClass.isAssignableFrom(AuthViewModel::class.java) -> {
                AuthViewModel(AuthRepository(apiService, sessionManager)) as T
            }
            modelClass.isAssignableFrom(ClothingViewModel::class.java) -> {
                ClothingViewModel(ClothingRepository(apiService)) as T
            }
            modelClass.isAssignableFrom(RoutineViewModel::class.java) -> {
                RoutineViewModel(RoutineRepository(apiService)) as T
            }
            modelClass.isAssignableFrom(MainViewModel::class.java) -> {
                MainViewModel(RecommendationRepository(apiService)) as T
            }
            else -> throw IllegalArgumentException("ViewModel inconnu: ${modelClass.name}")
        }
    }
}
