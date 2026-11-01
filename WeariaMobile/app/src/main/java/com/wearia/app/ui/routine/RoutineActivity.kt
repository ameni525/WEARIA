package com.wearia.app.ui.routine

import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.wearia.app.databinding.ActivityRoutineBinding
import com.wearia.app.ui.adapters.RoutineAdapter
import com.wearia.app.viewmodel.RoutineViewModel
import com.wearia.app.viewmodel.ViewModelFactory

class RoutineActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRoutineBinding
    private val viewModel: RoutineViewModel by viewModels { ViewModelFactory(this) }
    private lateinit var adapter: RoutineAdapter

    private val jours = listOf("LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE")
    private val occasions = listOf("UNIVERSITE", "TRAVAIL", "SORTIE", "SPORT", "QUOTIDIEN")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRoutineBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupSpinners()
        setupRecyclerView()
        setupListeners()
        observeViewModel()

        viewModel.loadRoutines()
    }

    private fun setupSpinners() {
        val adapterJours = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, jours)
        binding.spinnerJour.adapter = adapterJours

        val adapterOccasions = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, occasions)
        binding.spinnerOccasion.adapter = adapterOccasions
    }

    private fun setupRecyclerView() {
        adapter = RoutineAdapter(
            onDeleteClicked = { routine ->
                viewModel.deleteRoutine(routine.id)
                Toast.makeText(this, "Journée supprimée", Toast.LENGTH_SHORT).show()
            }
        )

        binding.rvRoutines.apply {
            layoutManager = LinearLayoutManager(this@RoutineActivity)
            adapter = this@RoutineActivity.adapter
        }
    }

    private fun setupListeners() {
        // Bouton de retour en arrière
        binding.btnBack.setOnClickListener {
            finish()
        }

        binding.btnSaveRoutine.setOnClickListener {
            val jour = binding.spinnerJour.selectedItem.toString()
            val occasion = binding.spinnerOccasion.selectedItem.toString()

            viewModel.saveRoutine(jour, occasion)
            Toast.makeText(this, "$jour configuré pour : $occasion", Toast.LENGTH_SHORT).show()
        }
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { loading ->
            binding.pbRoutine.visibility = if (loading) View.VISIBLE else View.GONE
        }

        viewModel.routines.observe(this) { list ->
            adapter.updateList(list)
        }
    }
}
