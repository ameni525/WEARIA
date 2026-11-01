package com.wearia.app.ui.dressing

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.wearia.app.data.models.ClothingItem
import com.wearia.app.databinding.ActivityWardrobeBinding
import com.wearia.app.ui.adapters.ClothingAdapter
import com.wearia.app.viewmodel.ClothingViewModel
import com.wearia.app.viewmodel.ViewModelFactory

class WardrobeActivity : AppCompatActivity() {

    private lateinit var binding: ActivityWardrobeBinding
    private val viewModel: ClothingViewModel by viewModels { ViewModelFactory(this) }
    private lateinit var adapter: ClothingAdapter

    private var selectedCategoryName: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWardrobeBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupRecyclerView()
        setupListeners()
        observeViewModel()

        viewModel.loadClothes()
    }

    private fun setupRecyclerView() {
        adapter = ClothingAdapter(
            onItemClicked = { item ->
                Toast.makeText(this, "${item.nom} (${item.statut.lowercase()})", Toast.LENGTH_SHORT).show()
            },
            onItemLongClicked = { item ->
                showActionDialog(item)
                true
            }
        )

        binding.rvClothing.apply {
            layoutManager = LinearLayoutManager(this@WardrobeActivity)
            setHasFixedSize(true)
            adapter = this@WardrobeActivity.adapter
        }
    }

    private fun setupListeners() {
        // Bouton de retour en arrière
        binding.btnBack.setOnClickListener {
            finish()
        }

        binding.fabAddClothing.setOnClickListener {
            startActivity(Intent(this, AddClothingActivity::class.java))
        }

        binding.btnRefresh.setOnClickListener {
            viewModel.loadClothes()
        }

        binding.chipGroupCategory.setOnCheckedChangeListener { _, checkedId ->
            when (checkedId) {
                binding.chipAll.id -> {
                    selectedCategoryName = null
                    viewModel.loadClothes()
                }
                binding.chipHauts.id -> {
                    selectedCategoryName = "Haut"
                    filterByLocalCategory("Haut")
                }
                binding.chipBas.id -> {
                    selectedCategoryName = "Bas"
                    filterByLocalCategory("Bas")
                }
                binding.chipChaussures.id -> {
                    selectedCategoryName = "Chaussures"
                    filterByLocalCategory("Chaussures")
                }
                binding.chipVestes.id -> {
                    selectedCategoryName = "Veste"
                    filterByLocalCategory("Veste")
                }
            }
        }
    }

    private fun filterByLocalCategory(catName: String) {
        val all = viewModel.clothes.value.orEmpty()
        val filtered = all.filter { it.categorie?.nom.equals(catName, ignoreCase = true) }
        adapter.updateList(filtered)
        binding.tvEmptyWardrobe.visibility = if (filtered.isEmpty()) View.VISIBLE else View.GONE
    }

    private fun showActionDialog(item: ClothingItem) {
        val currentStatus = item.statut
        val actionToggle = if (currentStatus == "DISPONIBLE") "Marquer comme sale (à laver)" else "Marquer comme propre (disponible)"

        val options = arrayOf(actionToggle, "Supprimer le vêtement")

        AlertDialog.Builder(this)
            .setTitle(item.nom)
            .setItems(options) { _, which ->
                when (which) {
                    0 -> {
                        viewModel.toggleClothingStatus(item)
                        Toast.makeText(this, "Statut mis à jour", Toast.LENGTH_SHORT).show()
                    }
                    1 -> {
                        confirmDelete(item)
                    }
                }
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun confirmDelete(item: ClothingItem) {
        AlertDialog.Builder(this)
            .setTitle("Suppression")
            .setMessage("Voulez-vous supprimer '${item.nom}' de votre dressing ?")
            .setIcon(android.R.drawable.ic_menu_delete)
            .setPositiveButton("Supprimer") { _, _ ->
                viewModel.deleteClothing(item)
                Toast.makeText(this, "Vêtement supprimé", Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton("Annuler", null)
            .show()
    }

    private fun observeViewModel() {
        viewModel.isLoading.observe(this) { loading ->
            binding.progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        }

        viewModel.clothes.observe(this) { list ->
            if (selectedCategoryName != null) {
                filterByLocalCategory(selectedCategoryName!!)
            } else {
                adapter.updateList(list)
                binding.tvEmptyWardrobe.visibility = if (list.isEmpty()) View.VISIBLE else View.GONE
            }
        }

        viewModel.errorMessage.observe(this) { err ->
            if (!err.isNullOrEmpty()) {
                Toast.makeText(this, err, Toast.LENGTH_LONG).show()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        viewModel.loadClothes()
    }
}
