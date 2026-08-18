"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { speciesModelMetrics } from "@/lib/data";

interface ConfusionMatrixProps {
  className?: string;
}

const CLASS_NAMES = ["Cattle", "Buffalo"];
const MATRIX = [
  [speciesModelMetrics.confusionMatrix.cattle.correct, speciesModelMetrics.confusionMatrix.cattle.wrong],
  [speciesModelMetrics.confusionMatrix.buffalo.wrong, speciesModelMetrics.confusionMatrix.buffalo.correct],
];

export function ConfusionMatrix({ className }: ConfusionMatrixProps) {
  const maxValue = Math.max(...MATRIX.flat());

  const getColor = (value: number) => {
    const intensity = value / maxValue;
    const r = Math.round(255 * (1 - intensity));
    const g = Math.round(200 * intensity + 55);
    const b = 55;
    return `rgb(${r}, ${g}, ${b})`;
  };

  const getTextColor = (value: number) => {
    return value / maxValue > 0.5 ? "#ffffff" : "#1f2937";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className={cn("w-full", className)}
    >
      <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-6 text-center">
        Species Classification Confusion Matrix
      </h4>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[400px] border-collapse">
          <thead>
            <tr>
              <th className="w-32"></th>
              {CLASS_NAMES.map((name) => (
                <th key={name} className="px-4 py-3 text-center font-semibold text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 border-b-2 border-gray-200 dark:border-gray-700">
                  Predicted: {name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {MATRIX.map((row, i) => (
              <motion.tr
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i }}
              >
                <th className="px-4 py-3 text-right font-semibold text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800 border-r-2 border-gray-200 dark:border-gray-700">
                  Actual: {CLASS_NAMES[i]}
                </th>
                {row.map((value, j) => (
                  <motion.td
                    key={j}
                    initial={{ scale: 0.8 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.1 * i + 0.05 * j, type: "spring", stiffness: 300 }}
                    className="px-4 py-4 text-center border border-gray-200 dark:border-gray-700"
                    style={{
                      backgroundColor: getColor(value),
                      color: getTextColor(value),
                    }}
                  >
                    <div className="text-3xl font-bold">{value}</div>
                    <div className="text-sm opacity-80">
                      {((value / (i === 0 ? 756 : 760)) * 100).toFixed(1)}%
                    </div>
                  </motion.td>
                ))}
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 text-center">
        {CLASS_NAMES.map((name, i) => (
          <motion.div
            key={name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + 0.1 * i }}
            className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4"
          >
            <p className="font-medium text-gray-900 dark:text-white mb-1">{name}</p>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {speciesModelMetrics.perClassMetrics[name.toLowerCase() as keyof typeof speciesModelMetrics.perClassMetrics].f1.toFixed(2)}%
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">F1-Score</p>
          </motion.div>
        ))}
      </div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="mt-4 text-center text-sm text-gray-500 dark:text-gray-400"
      >
        Total test images: {speciesModelMetrics.testImages} | Correct: {speciesModelMetrics.correctPredictions} | Wrong: {speciesModelMetrics.wrongPredictions}
      </motion.p>
    </motion.div>
  );
}