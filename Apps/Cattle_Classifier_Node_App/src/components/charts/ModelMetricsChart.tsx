"use client";

import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { cn } from "@/lib/utils";
import { breedModelMetrics, speciesModelMetrics } from "@/lib/data";

interface ModelMetricsChartProps {
  className?: string;
}

const METRICS_DATA = [
  { metric: "Test Accuracy", species: speciesModelMetrics.testAccuracy, breed: breedModelMetrics.testAccuracy, color: "#3b82f6" },
  { metric: "Macro F1", species: speciesModelMetrics.macroF1, breed: breedModelMetrics.macroF1, color: "#8b5cf6" },
  { metric: "Weighted F1", species: speciesModelMetrics.weightedF1, breed: breedModelMetrics.weightedF1, color: "#06b6d4" },
];

const PER_CLASS_DATA = breedModelMetrics.perClassMetrics;

export function ModelMetricsChart({ className }: ModelMetricsChartProps) {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-3 min-w-[200px]"
        >
          <p className="font-medium text-gray-900 dark:text-white mb-2">{label}</p>
          {payload.map((entry: any, i: number) => (
            <div key={i} className="flex justify-between text-sm mb-1">
              <span className="text-gray-600 dark:text-gray-300 flex items-center gap-1">
                <span
                  className="w-2 h-2 rounded"
                  style={{ backgroundColor: entry.color }}
                />
                {entry.name}
              </span>
              <span className="font-semibold text-gray-900 dark:text-white">
                {entry.value.toFixed(2)}%
              </span>
            </div>
          ))}
        </motion.div>
      );
    }
    return null;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className={cn("w-full", className)}
    >
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Overall Model Comparison
        </h4>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={METRICS_DATA}
              layout="vertical"
              margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis
                type="number"
                domain={[90, 100]}
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 12, fill: "#6b7280" }}
              />
              <YAxis
                type="category"
                dataKey="metric"
                width={100}
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 13, fontWeight: 500, fill: "#374151" }}
              />
              <Tooltip content={CustomTooltip} />
              <Legend
                layout="horizontal"
                align="center"
                verticalAlign="bottom"
                iconType="circle"
                iconSize={8}
                wrapperStyle={{ paddingTop: 10 }}
              />
              <Bar dataKey="species" radius={[0, 4, 4, 0]} maxBarSize={25} name="Species (Cattle vs Buffalo)">
                <Cell fill="#3b82f6" />
              </Bar>
              <Bar dataKey="breed" radius={[0, 4, 4, 0]} maxBarSize={25} name="Breed (5 Classes)">
                <Cell fill="#8b5cf6" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.3 }}
      >
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Per-Breed Performance (Breed Classifier)
        </h4>
        <div className="h-[350px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={Object.entries(PER_CLASS_DATA).map(([breed, metrics]) => ({
                breed,
                precision: metrics.precision,
                recall: metrics.recall,
                f1: metrics.f1,
              }))}
              layout="vertical"
              margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis
                type="number"
                domain={[80, 100]}
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 12, fill: "#6b7280" }}
              />
              <YAxis
                type="category"
                dataKey="breed"
                width={80}
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 13, fontWeight: 500, fill: "#374151" }}
              />
              <Tooltip content={CustomTooltip} />
              <Legend
                layout="horizontal"
                align="center"
                verticalAlign="bottom"
                iconType="circle"
                iconSize={8}
                wrapperStyle={{ paddingTop: 10 }}
              />
              <Bar dataKey="precision" radius={[0, 4, 4, 0]} maxBarSize={20} name="Precision">
                <Cell fill="#22c55e" />
              </Bar>
              <Bar dataKey="recall" radius={[0, 4, 4, 0]} maxBarSize={20} name="Recall">
                <Cell fill="#3b82f6" />
              </Bar>
              <Bar dataKey="f1" radius={[0, 4, 4, 0]} maxBarSize={20} name="F1-Score">
                <Cell fill="#f59e0b" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </motion.div>
  );
}