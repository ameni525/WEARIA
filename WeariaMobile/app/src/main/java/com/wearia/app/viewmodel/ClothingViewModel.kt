package com.wearia.app.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.wearia.app.data.models.*
import com.wearia.app.data.repositories.ClothingRepository
import kotlinx.coroutines.launch
import okhttp3.MultipartBody

class ClothingViewModel(private val repository: ClothingRepository) : ViewModel() {

    private val _clothes = MutableLiveData<List<ClothingItem>>(emptyList())
    val clothes: LiveData<List<ClothingItem>> = _clothes

    private val _isLoading = MutableLiveData<Boolean>(false)
    val isLoading: LiveData<Boolean> = _isLoading

    private val _errorMessage = MutableLiveData<String?>()
    val errorMessage: LiveData<String?> = _errorMessage

    private val _classification = MutableLiveData<ClassificationResponse?>()
    val classification: LiveData<ClassificationResponse?> = _classification

    private val _addResult = MutableLiveData<Result<ClothingItem>?>()
    val addResult: LiveData<Result<ClothingItem>?> = _addResult

    // Référentiels pour les formulaires
    val categories = MutableLiveData<List<CategorieItem>>(emptyList())
    val types = MutableLiveData<List<TypeVetementItem>>(emptyList())
    val colors = MutableLiveData<List<CouleurItem>>(emptyList())
    val styles = MutableLiveData<List<StyleItem>>(emptyList())

    fun loadReferentials() {
        viewModelScope.launch {
            repository.getCategories().onSuccess { categories.value = it }
            repository.getTypes().onSuccess { types.value = it }
            repository.getColors().onSuccess { colors.value = it }
            repository.getStyles().onSuccess { styles.value = it }
        }
    }

    fun loadClothes(
        categorieId: Int? = null,
        couleurId: Int? = null,
        saison: String? = null,
        statut: String? = null,
        search: String? = null
    ) {
        _isLoading.value = true
        viewModelScope.launch {
            repository.getClothes(categorieId, couleurId, saison, statut, search)
                .onSuccess {
                    _isLoading.value = false
                    _clothes.value = it
                }
                .onFailure {
                    _isLoading.value = false
                    _errorMessage.value = it.localizedMessage
                }
        }
    }

    fun toggleClothingStatus(item: ClothingItem) {
        val newStatus = if (item.statut == "DISPONIBLE") "SALE" else "DISPONIBLE"
        viewModelScope.launch {
            repository.updateClothingStatus(item.id, newStatus).onSuccess { updated ->
                // Mise à jour locale dans la liste (Chapitre 4: manipulation des données)
                val currentList = _clothes.value.orEmpty().toMutableList()
                val index = currentList.indexOfFirst { it.id == item.id }
                if (index != -1) {
                    currentList[index] = updated
                    _clothes.value = currentList
                }
            }
        }
    }

    fun deleteClothing(item: ClothingItem) {
        viewModelScope.launch {
            repository.deleteClothing(item.id).onSuccess {
                val currentList = _clothes.value.orEmpty().toMutableList()
                currentList.removeAll { it.id == item.id }
                _clothes.value = currentList
            }
        }
    }

    fun classifyImage(filePart: MultipartBody.Part) {
        _isLoading.value = true
        viewModelScope.launch {
            repository.classifyImage(filePart)
                .onSuccess {
                    _isLoading.value = false
                    _classification.value = it
                }
                .onFailure {
                    _isLoading.value = false
                    _errorMessage.value = "Erreur IA : ${it.localizedMessage}"
                }
        }
    }

    fun addClothing(request: ClothingCreateRequest) {
        _isLoading.value = true
        viewModelScope.launch {
            val result = repository.addClothing(request)
            _isLoading.value = false
            _addResult.value = result
        }
    }

    fun resetAddResult() {
        _addResult.value = null
        _classification.value = null
    }
}
