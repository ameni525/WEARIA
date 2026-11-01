package com.wearia.app.ui.dressing

import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import coil.load
import com.wearia.app.data.models.*
import com.wearia.app.databinding.ActivityAddClothingBinding
import com.wearia.app.utils.Constants
import com.wearia.app.viewmodel.ClothingViewModel
import com.wearia.app.viewmodel.ViewModelFactory
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

class AddClothingActivity : AppCompatActivity() {

    private lateinit var binding: ActivityAddClothingBinding
    private val viewModel: ClothingViewModel by viewModels { ViewModelFactory(this) }

    private var selectedImageUri: Uri? = null
    private var uploadedPhotoUrl: String = "/uploads/demo_chemise.jpg"

    private val pickImageLauncher = registerForActivityResult(
        ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedImageUri = uri
            binding.ivPreview.load(uri) {
                crossfade(true)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAddClothingBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupListeners()
        observeViewModel()

        viewModel.loadReferentials()
    }

    private fun setupListeners() {
        // Bouton de retour en arrière
        binding.btnBack.setOnClickListener {
            finish()
        }

        binding.btnPickImage.setOnClickListener {
            pickImageLauncher.launch("image/*")
        }

        binding.btnScanAi.setOnClickListener {
            if (selectedImageUri == null) {
                Toast.makeText(this, "Veuillez d'abord sélectionner une photo", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val file = copyUriToFile(selectedImageUri!!)
            val requestFile = file.asRequestBody("image/*".toMediaTypeOrNull())
            val body = MultipartBody.Part.createFormData("file", file.name, requestFile)

            viewModel.classifyImage(body)
        }

        binding.btnSaveClothing.setOnClickListener {
            val name = binding.etClothingName.text.toString().trim()
            if (name.isEmpty()) {
                binding.etClothingName.error = "Veuillez saisir un nom"
                return@setOnClickListener
            }

            val selectedCat = binding.spinnerCategory.selectedItem as? CategorieItem
            val selectedType = binding.spinnerType.selectedItem as? TypeVetementItem
            val selectedCol = binding.spinnerColor.selectedItem as? CouleurItem

            if (selectedCat == null || selectedType == null || selectedCol == null) {
                Toast.makeText(this, "Veuillez sélectionner la catégorie, le type et la couleur", Toast.LENGTH_LONG).show()
                return@setOnClickListener
            }

            val req = ClothingCreateRequest(
                nom = name,
                photo_url = uploadedPhotoUrl,
                type_vetement_id = selectedType.id,
                categorie_id = selectedCat.id,
                couleur_id = selectedCol.id,
                statut = "DISPONIBLE"
            )
            viewModel.addClothing(req)
        }
    }

    private fun observeViewModel() {
        viewModel.categories.observe(this) { list ->
            val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, list)
            binding.spinnerCategory.adapter = adapter
        }

        viewModel.types.observe(this) { list ->
            val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, list)
            binding.spinnerType.adapter = adapter
        }

        viewModel.colors.observe(this) { list ->
            val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, list)
            binding.spinnerColor.adapter = adapter
        }

        viewModel.isLoading.observe(this) { loading ->
            binding.pbAiScan.visibility = if (loading) View.VISIBLE else View.GONE
            binding.btnScanAi.isEnabled = !loading
            binding.btnSaveClothing.isEnabled = !loading
        }

        viewModel.classification.observe(this) { res ->
            if (res != null) {
                uploadedPhotoUrl = res.image_url
                binding.cardAiResult.visibility = View.VISIBLE
                val confidencePct = (res.confidence * 100).toInt()
                binding.tvAiDetails.text = "Type détecté : ${res.category} | Couleur : ${res.color} (Confiance : $confidencePct%)"

                // Pré-remplissage naturel
                binding.etClothingName.setText("${res.category} ${res.color}")

                selectSpinnerCategory(res.category)
                selectSpinnerColor(res.color)

                Toast.makeText(this, "Analyse terminée !", Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.addResult.observe(this) { result ->
            result?.onSuccess {
                Toast.makeText(this, "Vêtement '${it.nom}' ajouté à votre dressing !", Toast.LENGTH_SHORT).show()
                viewModel.resetAddResult()
                finish()
            }?.onFailure {
                Toast.makeText(this, it.localizedMessage ?: "Erreur d'ajout", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun selectSpinnerCategory(categoryName: String) {
        val cats = viewModel.categories.value.orEmpty()
        val index = cats.indexOfFirst { it.nom.equals(categoryName, ignoreCase = true) }
        if (index != -1) {
            binding.spinnerCategory.setSelection(index)
        }
    }

    private fun selectSpinnerColor(colorName: String) {
        val cols = viewModel.colors.value.orEmpty()
        val index = cols.indexOfFirst { it.nom.equals(colorName, ignoreCase = true) }
        if (index != -1) {
            binding.spinnerColor.setSelection(index)
        }
    }

    private fun copyUriToFile(uri: Uri): File {
        val inputStream = contentResolver.openInputStream(uri)
        val tempFile = File(cacheDir, "upload_temp_${System.currentTimeMillis()}.jpg")
        val outputStream = FileOutputStream(tempFile)
        inputStream?.copyTo(outputStream)
        inputStream?.close()
        outputStream.close()
        return tempFile
    }
}
