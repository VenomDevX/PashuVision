"use client";

import { motion } from "framer-motion";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { cn } from "@/lib/utils";
import { splitData } from "@/lib/data";

interface SplitChartProps {
  className?: string;
}

const COLORS = ["#3b82f6", "#8b5cf6", "#06b6d4"];

export function SplitChart({ className }: SplitChartProps) {
  const data = splitData.map((split, index) => ({
    ...split,
    fill: COLORS[index],
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const item = payload[0].payload;
      return (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-3 min-w-[180px]"
        >
          <div className="flex items-center gap-2 mb-1">
            <div
              className="w-3 h-3 rounded"
              style={{ backgroundColor: item.fill }}
            />
            <span className="font-semibold text-gray-900 dark:text-white">
              {item.name}
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-300 space-y-1">
            <div>Images: <span className="font-medium">{item.count.toLocaleString()}</span></div>
            <div>Percentage: <span className="font-medium">{item.percentage}%</span></div>
          </div>
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
      transition={{ duration: 0.6, delay: 0.2 }}
      className={cn("w-full h-[350px] flex flex-col items-center", className)}
    >
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={70}
            outerRadius={110}
            paddingAngle={3}
            dataKey="count"
            nameKey="name"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
            labelLine={false}
            fontSize={12}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
          <Tooltip content={CustomTooltip} />
          <Legend
            layout="vertical"
            align="right"
            verticalAlign="middle"
            iconType="circle"
            iconSize={10}
            wrapperStyle={{ marginLeft: 20 }}
          />
        </PieChart>
      </ResponsiveContainer>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.8 }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none"
      >
        <div className="text-3xl font-bold text-gray-900 dark:text-white">
          6,614
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          Total Images
        </div>
      </motion.div>
    </motion.div>
  );
}