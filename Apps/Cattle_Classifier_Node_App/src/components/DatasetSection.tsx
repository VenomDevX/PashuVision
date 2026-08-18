"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { breedData, splitData, totalImages, preprocessingSteps, datasetSources } from "@/lib/data";
import { BreedDistributionChart } from "./charts/BreedDistributionChart";
import { SplitChart } from "./charts/SplitChart";
import { Database, Filter, Scissors, CheckCircle, ExternalLink } from "lucide-react";

export function DatasetSection() {
  const sectionVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <section id="dataset" className="py-24 md:py-32 px-6 bg-white dark:bg-slate-900">
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
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-300 text-sm font-medium mb-4"
          >
            <Database className="w-4 h-4" />
            Curated Dataset
          </motion.span>
          <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            Multi-Breed Cattle Dataset
          </motion.h2>
          <motion.p variants={itemVariants} className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            A carefully curated and cleaned dataset of 5 prominent Indian cattle breeds with multi-view images, deduplicated and quality-filtered for robust model training.
          </motion.p>
        </motion.div>

        {/* Stats Overview */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16"
        >
          {[
            { label: "Total Images", value: totalImages.toLocaleString(), icon: Database, color: "blue" },
            { label: "Breeds", value: "5", icon: Filter, color: "green" },
            { label: "Train / Val / Test", value: "70 / 15 / 15", icon: Scissors, color: "purple" },
            { label: "Quality Check", value: "Passed", icon: CheckCircle, color: "amber" },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              variants={itemVariants}
              className="group relative p-6 rounded-2xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-800 transition-all"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />
              <div className="relative flex items-center gap-4">
                <div
                  className={`p-3 rounded-xl bg-${stat.color}-100 dark:bg-${stat.color}-900/30 text-${stat.color}-600 dark:text-${stat.color}-400`}
                >
                  <stat.icon className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{stat.label}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Charts Row */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="grid lg:grid-cols-2 gap-8 mb-16"
        >
          {/* Breed Distribution */}
          <motion.div variants={itemVariants} className="bg-white dark:bg-slate-800/50 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 md:p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Breed Distribution</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Class balance across 5 Indian cattle breeds</p>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                <ExternalLink className="w-4 h-4" />
                <span>Kaggle / Mendeley</span>
              </div>
            </div>
            <BreedDistributionChart />
          </motion.div>

          {/* Train/Val/Test Split */}
          <motion.div variants={itemVariants} className="bg-white dark:bg-slate-800/50 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 md:p-8 relative">
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Train / Validation / Test Split</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Stratified split maintaining class distribution</p>
            </div>
            <SplitChart />
          </motion.div>
        </motion.div>

        {/* Breed Cards */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          className="mb-16"
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
            Breed Details
          </motion.h3>
          <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {breedData.map((breed, index) => (
              <motion.div
                key={breed.breed}
                variants={itemVariants}
                className="group relative p-5 rounded-2xl bg-white dark:bg-slate-800 border border-gray-100 dark:border-gray-700 hover:border-gray-200 dark:hover:border-gray-600 transition-all hover:shadow-lg"
                style={{ borderLeft: `4px solid ${breed.color}` }}
              >
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-gray-900 dark:text-white">{breed.breed}</h4>
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: breed.color }}
                  />
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500 dark:text-gray-400">Images</span>
                    <span className="font-medium text-gray-900 dark:text-white">{breed.count.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500 dark:text-gray-400">Percentage</span>
                    <span className="font-medium text-gray-900 dark:text-white">{breed.percentage}%</span>
                  </div>
                  <div className="h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden mt-3">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${breed.percentage}%` }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5 + index * 0.1, duration: 1 }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: breed.color }}
                    />
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Preprocessing Steps */}
        <motion.div
          variants={sectionVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
            Data Preprocessing Pipeline
          </motion.h3>
          <motion.div variants={itemVariants} className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {preprocessingSteps.map((step, index) => (
              <motion.div
                key={step}
                variants={itemVariants}
                className="flex items-start gap-4 p-5 rounded-xl bg-gray-50 dark:bg-slate-800/50 border border-gray-100 dark:border-gray-700"
              >
                <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
                  <span className="text-xl font-bold">{index + 1}</span>
                </div>
                <p className="text-gray-700 dark:text-gray-300 mt-1">{step}</p>
              </motion.div>
            ))}
          </motion.div>

          {/* Data Sources */}
          <motion.div
            variants={sectionVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            className="mt-12"
          >
            <motion.h3 variants={itemVariants} className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
              Dataset Sources
            </motion.h3>
            <motion.div variants={itemVariants} className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto">
              {datasetSources.map((source, index) => (
                <motion.a
                  key={source}
                  href="#"
                  target="_blank"
                  rel="noopener noreferrer"
                  variants={itemVariants}
                  className="flex items-center gap-3 p-4 rounded-xl bg-white dark:bg-slate-800 border border-gray-100 dark:border-gray-700 hover:border-blue-200 dark:hover:border-blue-800 transition-all group"
                >
                  <ExternalLink className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors" />
                  <span className="text-gray-700 dark:text-gray-300">{source}</span>
                </motion.a>
              ))}
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}