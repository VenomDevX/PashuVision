"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { architectureInfo, techStack } from "@/lib/data";
import { Cpu, Database, Zap, GitBranch, Layers, Settings, ArrowRight, CheckCircle } from "lucide-react";

export function ArchitectureSection() {
  const sectionVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { staggerChildren: 0.1 } },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const pipelineSteps = [
    { title: "Input Image", desc: "224×224 RGB cattle image", icon: Database },
    { title: "Preprocessing", desc: "Normalize, augment, batch", icon: Settings },
    { title: "EfficientNet-B0", desc: "Frozen feature extractor (80%)", icon: Cpu },
    { title: "Fine-tuning", desc: "Trainable layers (20%) + Classifier head", icon: Layers },
    { title: "Classification", desc: "Softmax → 5 breed probabilities", icon: Zap },
  ];

  const trainingDetails = [
    { label: "Optimizer", value: architectureInfo.trainingConfig.optimizer },
    { label: "Learning Rate", value: `${architectureInfo.trainingConfig.learningRate} (cosine annealing)` },
    { label: "Batch Size", value: architectureInfo.trainingConfig.batchSize },
    { label: "Epochs", value: architectureInfo.trainingConfig.epochs },
    { label: "Early Stopping", value: `Patience ${architectureInfo.trainingConfig.earlyStopping}` },
    { label: "Loss Function", value: architectureInfo.trainingConfig.loss },
    { label: "Augmentation", value: architectureInfo.trainingConfig.augmentation },
    { label: "Hardware", value: architectureInfo.hardware },
    { label: "Framework", value: architectureInfo.framework },
  ];

  return (
    <section id="architecture" className="py-24 md:py-32 px-6 bg-white dark:bg-slate-900">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="text-center mb-16"
        >
          <motion.span
            variants={itemVariants}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-50 dark:bg-purple-900/30 border border-purple-200 dark:border-purple-800 text-purple-700 dark:text-purple-300 text-sm font-medium mb-4"
          >
            <GitBranch className="w-4 h-4" />
            Model Architecture
          </motion.span>
          <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Technical Architecture
          </motion.h2>
          <motion.p variants={itemVariants} className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Transfer learning with EfficientNet-B0: leveraging ImageNet pre-trained features and fine-tuning for domain-specific cattle breed recognition.
          </motion.p>
        </motion.div>

        {/* Model Specs */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-16"
        >
          {[
            { label: "Base Model", value: architectureInfo.baseModel, icon: Cpu, color: "blue" },
            { label: "Pre-trained On", value: architectureInfo.preTrainedOn, icon: Database, color: "green" },
            { label: "Input Resolution", value: architectureInfo.inputResolution, icon: Layers, color: "purple" },
            { label: "Parameters", value: architectureInfo.parameters, icon: Zap, color: "amber" },
          ].map((spec, index) => (
            <motion.div
              key={spec.label}
              variants={itemVariants}
              className="p-6 rounded-2xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className={`p-2 rounded-xl bg-${spec.color}-100 dark:bg-${spec.color}-900/30 text-${spec.color}-600 dark:text-${spec.color}-400`}>
                  <spec.icon className="w-5 h-5" />
                </div>
                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{spec.label}</span>
              </div>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">{spec.value}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Pipeline Visualization */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-8 text-center">
            Inference Pipeline
          </motion.h3>
          <motion.div variants={itemVariants} className="relative">
            {/* Connecting line */}
            <div className="absolute top-10 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-gray-300 to-transparent dark:via-gray-600" />

            <div className="flex flex-wrap justify-center gap-4 md:gap-8 relative z-10">
              {pipelineSteps.map((step, index) => (
                <motion.div
                  key={step.title}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + index * 0.15 }}
                  className="flex flex-col items-center relative"
                >
                  <div className="relative z-10 w-20 h-20 rounded-2xl bg-white dark:bg-slate-800 border-2 border-gray-200 dark:border-gray-700 flex items-center justify-center shadow-lg">
                    <step.icon className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>

                  {index < pipelineSteps.length - 1 && (
                    <div className="absolute top-10 left-1/2 w-full h-0.5 bg-gradient-to-r from-blue-500 to-transparent -translate-x-1/2" />
                  )}

                  <div className="mt-4 w-40 text-center">
                    <p className="font-semibold text-gray-900 dark:text-white text-sm">{step.title}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{step.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </motion.div>

        {/* Transfer Learning Strategy */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-8 text-center">
            Transfer Learning Strategy
          </motion.h3>
          <motion.div variants={itemVariants} className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <motion.div
              className="p-6 rounded-2xl bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-xl bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400">
                  <CheckCircle className="w-5 h-5" />
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Frozen Feature Extractor</h4>
              </div>
              <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                <li className="flex items-center gap-2">• Initial 80% of EfficientNet-B0 layers frozen</li>
                <li className="flex items-center gap-2">• Pre-trained on ImageNet (1000 classes)</li>
                <li className="flex items-center gap-2">• Extracts generic visual features (edges, textures, shapes)</li>
                <li className="flex items-center gap-2">• Reduces training time & prevents overfitting</li>
              </ul>
            </motion.div>

            <motion.div
              className="p-6 rounded-2xl bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800"
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 rounded-xl bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400">
                  <Layers className="w-5 h-5" />
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white">Fine-tuned Classifier Head</h4>
              </div>
              <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                <li className="flex items-center gap-2">• Final 20% layers unfrozen for domain adaptation</li>
                <li className="flex items-center gap-2">• Custom head: GlobalAvgPool → Dropout(0.3) → Dense(512) → Dropout(0.2) → Dense(5)</li>
                <li className="flex items-center gap-2">• Label smoothing (0.1) for better calibration</li>
                <li className="flex items-center gap-2">• Cosine annealing LR scheduler with warm restarts</li>
              </ul>
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Training Configuration */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-8 text-center">
            Training Configuration
          </motion.h3>
          <motion.div variants={itemVariants} className="grid md:grid-cols-3 gap-4 max-w-5xl mx-auto">
            {trainingDetails.map((detail, index) => (
              <motion.div
                key={detail.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.03 }}
                className="p-5 rounded-xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700"
              >
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{detail.label}</p>
                <p className="text-gray-900 dark:text-white">{detail.value}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-8 text-center">
            Technology Stack
          </motion.h3>
          <motion.div variants={itemVariants} className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
            {techStack.map((category, index) => (
              <motion.div
                key={category.category}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className="p-6 rounded-2xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-800 transition-all"
              >
                <h4 className="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <GitBranch className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                  {category.category}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {category.items.map((item) => (
                    <span
                      key={item}
                      className="px-3 py-1 text-sm rounded-full bg-white dark:bg-slate-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}