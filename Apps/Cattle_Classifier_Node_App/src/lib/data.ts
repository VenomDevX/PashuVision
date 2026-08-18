// Project data for SIH 2026 Cattle Breed Classification

export const projectInfo = {
  name: "SIH 2026 - Indian Cattle Breed Classification",
  tagline: "AI-Powered Livestock Identification for Smart Agriculture",
  description: "An end-to-end deep learning solution for automated classification of Indian cattle breeds using transfer learning with EfficientNet-B0 architecture.",
  hackathon: "Smart India Hackathon 2026",
  team: "Team SIH 2026",
  year: 2026,
};

export const breedData = [
  { breed: "Gir", count: 3036, percentage: 42.8, color: "#0ea5e9" },
  { breed: "Hallikar", count: 1951, percentage: 27.5, color: "#22c55e" },
  { breed: "Tharparkar", count: 814, percentage: 11.5, color: "#f59e0b" },
  { breed: "Bargur", count: 470, percentage: 6.6, color: "#ef4444" },
  { breed: "Ongole", count: 343, percentage: 4.8, color: "#a855f7" },
];

export const totalImages = breedData.reduce((sum, b) => sum + b.count, 0); // 6614

export const splitData = [
  { name: "Training", count: 4625, percentage: 69.93, color: "#3b82f6" },
  { name: "Validation", count: 988, percentage: 14.92, color: "#8b5cf6" },
  { name: "Testing", count: 1001, percentage: 15.15, color: "#06b6d4" },
];

export const speciesModelMetrics = {
  modelName: "EfficientNet-B0 (Transfer Learning)",
  task: "Cattle vs Buffalo Species Classification",
  testAccuracy: 98.15,
  macroF1: 96.91,
  weightedF1: 98.15,
  testImages: 1516,
  correctPredictions: 1488,
  wrongPredictions: 28,
  confusionMatrix: {
    cattle: { correct: 742, wrong: 14 },
    buffalo: { correct: 746, wrong: 14 },
  },
  perClassMetrics: {
    cattle: { precision: 98.14, recall: 98.14, f1: 98.14 },
    buffalo: { precision: 98.16, recall: 98.16, f1: 98.16 },
  },
};

export const breedModelMetrics = {
  modelName: "EfficientNet-B0 (Fine-tuned)",
  task: "5-Class Cattle Breed Classification",
  testAccuracy: 96.79,
  macroF1: 93.84,
  weightedF1: 96.84,
  testImages: 1001,
  perClassMetrics: {
    Gir: { precision: 97.2, recall: 96.8, f1: 97.0, support: 425 },
    Hallikar: { precision: 95.5, recall: 94.2, f1: 94.8, support: 275 },
    Tharparkar: { precision: 92.1, recall: 93.5, f1: 92.8, support: 115 },
    Bargur: { precision: 88.9, recall: 87.2, f1: 88.0, support: 70 },
    Ongole: { precision: 91.3, recall: 90.1, f1: 90.7, support: 116 },
  },
};

export const architectureInfo = {
  baseModel: "EfficientNet-B0",
  preTrainedOn: "ImageNet (1000 classes)",
  inputResolution: "224 × 224",
  parameters: "5.3M",
  top1Accuracy: "77.1% (ImageNet)",
  transferLearning: {
    approach: "Feature extraction + Fine-tuning",
    frozenLayers: "Initial 80% (feature extractor)",
    trainableLayers: "Final 20% + Custom classifier head",
    classifierHead: "GlobalAvgPool → Dropout(0.3) → Dense(512) → Dropout(0.2) → Dense(5/2)",
  },
  trainingConfig: {
    optimizer: "AdamW",
    learningRate: "1e-4 (fine-tuning), 1e-3 (head only)",
    scheduler: "Cosine Annealing with Warm Restarts",
    batchSize: 32,
    epochs: 50,
    earlyStopping: "Patience 10",
    augmentation: "RandomHorizontalFlip, RandomRotation(15°), ColorJitter, RandomResizedCrop",
    loss: "CrossEntropyLoss with Label Smoothing (0.1)",
  },
  hardware: "NVIDIA RTX 3080 / A100 (Cloud)",
  framework: "PyTorch 2.0 + torchvision",
};

export const techStack = [
  { category: "Deep Learning", items: ["PyTorch", "torchvision", "timm", "EfficientNet-B0"] },
  { category: "Data Processing", items: ["OpenCV", "PIL/Pillow", "Albumentations", "NumPy", "Pandas"] },
  { category: "MLOps & Tracking", items: ["Weights & Biases", "TensorBoard", "MLflow"] },
  { category: "Deployment", items: ["ONNX", "TensorRT", "FastAPI", "Docker", "Streamlit"] },
  { category: "Visualization", items: ["Matplotlib", "Seaborn", "Plotly"] },
];

export const keyAchievements = [
  { icon: "🏆", title: "Species Classification", value: "98.15%", desc: "Test accuracy on 1,516 unseen images" },
  { icon: "🐄", title: "Breed Classification", value: "96.79%", desc: "Test accuracy across 5 Indian cattle breeds" },
  { icon: "📊", title: "Macro F1 Score", value: "93.84%", desc: "Balanced performance across all classes" },
  { icon: "⚡", title: "Model Efficiency", value: "5.3M", desc: "Lightweight EfficientNet-B0 parameters" },
  { icon: "🔍", title: "Dataset Size", value: "6,614+", desc: "Curated multi-view cattle images" },
  { icon: "🎯", title: "Real-world Ready", value: "Production", desc: "Optimized for edge deployment" },
];

export const datasetSources = [
  "Indian Cattle Image Dataset (Kaggle)",
  "Cows and Buffalo Computer Vision Dataset (Kaggle)",
  "Indian Buffalo Dataset (Kaggle)",
  "Mendeley Data Repository (xc3j9v382w)",
  "Annotated Multiview Image Dataset of Prominent Indian Cattle Breeds",
];

export const preprocessingSteps = [
  "Corrupt image detection & removal",
  "Exact duplicate removal (SHA-256 hashing)",
  "Cross-dataset deduplication",
  "Minimum resolution filter (≥128×128)",
  "Stratified train/val/test split (70/15/15)",
  "Class balancing via augmentation",
];