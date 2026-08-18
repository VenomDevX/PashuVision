"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { projectInfo } from "@/lib/data";
import { Github, Twitter, Linkedin, Mail, Award, Brain, Database } from "lucide-react";

export function Footer() {
  const navLinks = [
    { href: "#hero", label: "Overview" },
    { href: "#dataset", label: "Dataset" },
    { href: "#models", label: "Models" },
    { href: "#architecture", label: "Architecture" },
  ];

  const socialLinks = [
    { icon: Github, href: "#", label: "GitHub" },
    { icon: Twitter, href: "#", label: "Twitter" },
    { icon: Linkedin, href: "#", label: "LinkedIn" },
    { icon: Mail, href: "#", label: "Contact" },
  ];

  return (
    <footer className="bg-slate-900 text-white relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-t from-blue-500/10 via-transparent to-amber-500/10" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-r from-blue-500/10 to-amber-500/10 blur-3xl" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-16 md:py-24">
        <div className="grid md:grid-cols-4 gap-12 mb-16">
          {/* Brand */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="md:col-span-1"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 rounded-2xl bg-gradient-to-br from-blue-500 to-amber-500">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">{projectInfo.name.split(" - ")[0]}</span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">
              {projectInfo.tagline}
            </p>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Award className="w-4 h-4" />
              <span>{projectInfo.hackathon} {projectInfo.year}</span>
            </div>
          </motion.div>

          {/* Navigation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h4 className="font-semibold text-white mb-4">Navigation</h4>
            <nav className="space-y-3">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-2"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                  {link.label}
                </a>
              ))}
            </nav>
          </motion.div>

          {/* Key Metrics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h4 className="font-semibold text-white mb-4">Key Metrics</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span className="text-slate-400 text-sm">Species Accuracy</span>
                <span className="font-bold text-blue-400">98.15%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span className="text-slate-400 text-sm">Breed Accuracy</span>
                <span className="font-bold text-amber-400">96.79%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span className="text-slate-400 text-sm">Macro F1 (Breed)</span>
                <span className="font-bold text-green-400">93.84%</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                <span className="text-slate-400 text-sm">Dataset Size</span>
                <span className="font-bold text-purple-400">6,614+</span>
              </div>
            </div>
          </motion.div>

          {/* Social */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h4 className="font-semibold text-white mb-4">Connect</h4>
            <div className="flex flex-wrap gap-3 mb-6">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 hover:text-white hover:border-blue-500 hover:bg-blue-500/10 transition-all"
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
            <p className="text-slate-500 text-sm">
              Built for Smart India Hackathon 2026
            </p>
          </motion.div>
        </div>

        {/* Bottom Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="pt-8 border-t border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4"
        >
          <p className="text-slate-500 text-sm">
            © {new Date().getFullYear()} {projectInfo.name}. Open source project for agricultural AI.
          </p>
          <div className="flex items-center gap-6 text-xs text-slate-500">
            <span>Model: EfficientNet-B0</span>
            <span>Framework: PyTorch</span>
            <span>Deployment: ONNX + FastAPI</span>
          </div>
        </motion.div>
      </div>
    </footer>
  );
}