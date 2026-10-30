# AI Livestock Breed Identification System

An AI-powered system designed to classify images of livestock (Cattle and Buffalo) into their exact breeds. Built for Smart India Hackathon (SIH) 2026.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.10+ installed. This project uses PyTorch for its machine learning models.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VenomDevX/PashuVision.git
   cd PashuVision
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📂 Project Structure

- **`Apps/Livestock_Flask_App/`**: Contains the Python Flask web application backend and frontend UI for the livestock predictor.
- **`Apps/Cattle_Classifier_Node_App/`**: Contains a supplementary Node.js web application.
- **`Datasets/`**: Contains the raw and processed image datasets for both Cattle and Buffalo.
- **`Models/`**: Contains the `.pth` weights for the trained neural networks.
- **`Scripts/`**: Contains advanced machine learning processing scripts.

## 💻 Running the Web App

To start the main prediction web interface locally:

```bash
cd Apps/Livestock_Flask_App
python app.py
```
Then navigate to `http://127.0.0.1:5000` in your browser.

## 🧠 Training & Model Pipeline

If you wish to contribute to the Machine Learning model's accuracy, we have a 4-step pipeline located in the `Scripts/` directory. **It is highly recommended to run these scripts on a GPU (e.g., Google Colab or AWS).**

1. **`augment_dataset.py`**: Balances the dataset by generating augmented images for minority breeds until every breed reaches exactly 350 images.
2. **`crop_backgrounds_yolo.py`**: Utilizes YOLOv8 to tightly crop the animal out of the image, removing background bias (grass, fences, humans).
3. **`create_species_dataset.py`**: Consolidates the data to train the binary Species Router model (Cattle vs Buffalo).
4. **`train_advanced_model.py`**: A PyTorch training loop that trains an `EfficientNet-B4` architecture using Mixed Precision and Cosine Annealing.

## 🤝 Contributing

1. Request access to the `.pth` model weights if you wish to run the local server, as massive models are not pushed to Git by default.
2. If you are adding more data, place raw images into `Datasets/Raw/Cattle_Data/<breed>` or `Datasets/Raw/Buffalo_Data/<breed>`.
3. Run the ML pipeline scripts in `Scripts/` to process the new data and retrain the models
