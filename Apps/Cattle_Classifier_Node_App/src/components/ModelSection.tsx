"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { speciesModelMetrics, breedModelMetrics } from "@/lib/data";
import { ModelMetricsChart } from "./charts/ModelMetricsChart";
import { ConfusionMatrix } from "./charts/ConfusionMatrix";
import { Brain, Award, Target, BarChart2, GitBranch } from "lucide-react";

export function ModelSection() {
  const sectionVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  const modelCards = [
    {
      title: "Species Classifier",
      subtitle: "Cattle vs Buffalo Binary Classification",
      icon: Target,
      iconColor: "blue",
      metrics: [
        { label: "Test Accuracy", value: `${speciesModelMetrics.testAccuracy}%` },
        { label: "Macro F1-Score", value: `${speciesModelMetrics.macroF1}%` },
        { label: "Test Images", value: speciesModelMetrics.testImages.toLocaleString() },
        { label: "Correct / Wrong", value: `${speciesModelMetrics.correctPredictions} / ${speciesModelMetrics.wrongPredictions}` },
      ],
      badge: "98.15% Accuracy",
      badgeColor: "blue",
    },
    {
      title: "Breed Classifier",
      subtitle: "5-Class Indian Cattle Breed Classification",
      icon: Award,
      iconColor: "amber",
      metrics: [
        { label: "Test Accuracy", value: `${breedModelMetrics.testAccuracy}%` },
        { label: "Macro F1-Score", value: `${breedModelMetrics.macroF1}%` },
        { label: "Weighted F1", value: `${breedModelMetrics.weightedF1}%` },
        { label: "Test Images", value: breedModelMetrics.testImages.toLocaleString() },
      ],
      badge: "96.79% Accuracy",
      badgeColor: "amber",
    },
  ];

  return (
    <section id="models" className="py-24 md:py-32 px-6 bg-gray-50 dark:bg-slate-900/50">
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
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300 text-sm font-medium mb-4"
          >
            <Brain className="w-4 h-4" />
            Deep Learning Models
          </motion.span>
          <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Model Performance
          </motion.h2>
          <motion.p variants={itemVariants} className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Two specialized EfficientNet-B0 models trained via transfer learning: one for species detection, another for fine-grained breed classification.
          </motion.p>
        </motion.div>

        {/* Model Overview Cards */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid md:grid-cols-2 gap-6 mb-16"
        >
          {modelCards.map((model, index) => (
            <motion.div
              key={model.title}
              variants={itemVariants}
              className="relative group p-8 rounded-2xl bg-white dark:bg-slate-800 border border-gray-100 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-800 transition-all hover:shadow-xl"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />
              <div className="relative flex items-start gap-4 mb-6">
                <div className={`p-4 rounded-2xl bg-${model.iconColor}-100 dark:bg-${model.iconColor}-900/30 text-${model.iconColor}-600 dark:text-${model.iconColor}-400`}>
                  <model.icon className="w-8 h-8" />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white">{model.title}</h3>
                  <p className="text-gray-500 dark:text-gray-400 mt-1">{model.subtitle}</p>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-semibold bg-${model.badgeColor}-100 dark:bg-${model.badgeColor}-900/30 text-${model.badgeColor}-700 dark:text-${model.badgeColor}-300`}>
                  {model.badge}
                </div>
              </div>

              <div className="relative grid grid-cols-2 gap-4">
                {model.metrics.map((metric, i) => (
                  <motion.div
                    key={metric.label}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 + index * 0.2 + i * 0.05 }}
                    className="p-4 rounded-xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700"
                  >
                    <p className="text-sm text-gray-500 dark:text-gray-400">{metric.label}</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{metric.value}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Detailed Metrics Charts */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.div variants={itemVariants} className="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 md:p-8">
            <ModelMetricsChart />
          </motion.div>
        </motion.div>

        {/* Confusion Matrix */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.div variants={itemVariants} className="bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 md:p-8">
            <ConfusionMatrix />
          </motion.div>
        </motion.div>

        {/* Per-Class Breed Metrics Table */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
            Per-Breed Detailed Metrics
          </motion.h3>
          <motion.div variants={itemVariants} className="overflow-x-auto bg-white dark:bg-slate-800 rounded-2xl border border-gray-100 dark:border-gray-700">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="px-6 py-4 text-left font-semibold text-gray-900 dark:text-white">Breed</th>
                  <th className="px-6 py-4 text-center font-semibold text-gray-900 dark:text-white">Precision</th>
                  <th className="px-6 py-4 text-center font-semibold text-gray-900 dark:text-white">Recall</th>
                  <th className="px-6 py-4 text-center font-semibold text-gray-900 dark:text-white">F1-Score</th>
                  <th className="px-6 py-4 text-center font-semibold text-gray-900 dark:text-white">Support</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(breedModelMetrics.perClassMetrics).map(([breed, metrics], index) => (
                  <motion.tr
                    key={breed}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + index * 0.05 }}
                    className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-slate-800/50 transition-colors"
                  >
                    <td className="px-6 py-4 font-medium text-gray-900 dark:text-white flex items-center gap-3">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: breedData.find(b => b.breed === breed)?.color }}
                      />
                      {breed}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="font-semibold text-green-600 dark:text-green-400">{metrics.precision}%</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="font-semibold text-blue-600 dark:text-blue-400">{metrics.recall}%</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="font-bold text-amber-600 dark:text-amber-400">{metrics.f1}%</span>
                    </td>
                    <td className="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                      {metrics.support}
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}