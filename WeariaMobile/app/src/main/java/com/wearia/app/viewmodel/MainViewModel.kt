package com.wearia.app.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.wearia.app.data.models.OutfitRecommendationResponse
import com.wearia.app.data.repositories.RecommendationRepository
import kotlinx.coroutines.launch

class MainViewModel(private val repository: RecommendationRepository) : ViewModel() {

    private val _outfit = MutableLiveData<OutfitRecommendationResponse?>()
    val outfit: LiveData<OutfitRecommendationResponse?> = _outfit

    private val _isLoading = MutableLiveData<Boolean>(false)
    val isLoading: LiveData<Boolean> = _isLoading

    private val _message = MutableLiveData<String?>()
    val message: LiveData<String?> = _message

    fun generateDailyOutfit(occasion: String? = null, temp: Float = 19.0f, rain: Boolean = false, desc: String = "Ensoleillé") {
        _isLoading.value = true
        viewModelScope.launch {
            repository.getDailyRecommendation(occasion, temp, rain, desc)
                .onSuccess {
                    _isLoading.value = false
                    _outfit.value = it
                }
                .onFailure {
                    _isLoading.value = false
                    _message.value = it.localizedMessage
                }
        }
    }

    fun submitFeedback(outfitId: Int, appreciation: String) {
        viewModelScope.launch {
            repository.sendFeedback(outfitId, appreciation)
                .onSuccess {
                    _message.value = "Merci pour votre retour !"
                }
        }
    }
}
