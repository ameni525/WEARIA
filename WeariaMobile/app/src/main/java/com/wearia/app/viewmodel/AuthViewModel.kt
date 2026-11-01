package com.wearia.app.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.wearia.app.data.models.TokenResponse
import com.wearia.app.data.repositories.AuthRepository
import kotlinx.coroutines.launch

class AuthViewModel(private val authRepository: AuthRepository) : ViewModel() {

    private val _authState = MutableLiveData<Result<TokenResponse>?>()
    val authState: LiveData<Result<TokenResponse>?> = _authState

    private val _isLoading = MutableLiveData<Boolean>(false)
    val isLoading: LiveData<Boolean> = _isLoading

    fun login(email: String, motDePasse: String) {
        _isLoading.value = true
        viewModelScope.launch {
            val result = authRepository.login(email, motDePasse)
            _isLoading.value = false
            _authState.value = result
        }
    }

    fun register(nom: String, email: String, motDePasse: String, genre: String?, ville: String?) {
        _isLoading.value = true
        viewModelScope.launch {
            val result = authRepository.register(nom, email, motDePasse, genre, ville)
            _isLoading.value = false
            _authState.value = result
        }
    }

    fun isLoggedIn(): Boolean = authRepository.isLoggedIn()

    fun getUserName(): String = authRepository.getUserName()

    fun logout() = authRepository.logout()
}
