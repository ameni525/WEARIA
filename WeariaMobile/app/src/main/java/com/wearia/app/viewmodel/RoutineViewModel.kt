package com.wearia.app.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.wearia.app.data.models.RoutineItem
import com.wearia.app.data.repositories.RoutineRepository
import kotlinx.coroutines.launch

class RoutineViewModel(private val repository: RoutineRepository) : ViewModel() {

    private val _routines = MutableLiveData<List<RoutineItem>>(emptyList())
    val routines: LiveData<List<RoutineItem>> = _routines

    private val _isLoading = MutableLiveData<Boolean>(false)
    val isLoading: LiveData<Boolean> = _isLoading

    fun loadRoutines() {
        _isLoading.value = true
        viewModelScope.launch {
            repository.getRoutines().onSuccess {
                _isLoading.value = false
                _routines.value = it
            }.onFailure {
                _isLoading.value = false
            }
        }
    }

    fun saveRoutine(jourSemaine: String, occasion: String) {
        viewModelScope.launch {
            repository.saveRoutine(jourSemaine, occasion).onSuccess {
                loadRoutines()
            }
        }
    }

    fun deleteRoutine(routineId: Int) {
        viewModelScope.launch {
            repository.deleteRoutine(routineId).onSuccess {
                loadRoutines()
            }
        }
    }
}
