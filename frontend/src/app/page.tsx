"use client";

import React, { useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import {
  BarChart3,
  FileText,
  Upload,
  Download,
  CheckCircle2,
  Clock,
  Zap,
  Lightbulb,
  AlertTriangle,
  Search,
  CheckCircle,
  Trophy,
  Target,
  Layout,
  Bell,
  User,
  ChevronRight,
  MessageSquareQuote,
  HelpCircle,
  FileUp,
  Braces,
} from "lucide-react";

interface AnalysisData {
  overall_score: number;
  recruiter_summary: string;
  red_flags: string[];
  metrics: {
    skills: number;
    keywords: number;
    formatting: number;
    experience: number;
    projects: number;
    awards: number;
  };
  detailed_analysis: string;
  checklist: { label: string; status: boolean }[];
  tips: { title: string; text: string }[];
  mock_interview: { question: string; purpose: string }[];
}

export default function V4Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [data, setData] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showInput, setShowInput] = useState(true);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setLogs(["Đang khởi tạo Agent...", "Đang đọc file PDF..."]);

    const formData = new FormData();
    formData.append("file", file);
    if (jdText) formData.append("jd", jdText);

    try {
      const response = await fetch("http://localhost:8000/analyze-stream", {
        method: "POST",
        body: formData,
      });

      if (!response.body) throw new Error("Không thể kết nối stream.");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonStr = line.replace("data: ", "").trim();
            try {
              const payload = JSON.parse(jsonStr);
              if (payload.type === "log") {
                setLogs((prev) => [...prev, payload.content].slice(-10));
              } else if (payload.type === "result") {
                setData(payload.data);
                setShowInput(false);
              } else if (payload.type === "error") {
                setError(payload.content);
              }
            } catch (e) {
              console.error("Parse error:", e);
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message || "Kết nối thất bại.");
    } finally {
      setLoading(false);
    }
  };

  // Tính toán điểm cho Radar Chart lục giác (6 chỉ số)
  const getRadarPoints = (metrics: any) => {
    if (!metrics) return "100,100 100,100 100,100 100,100 100,100 100,100";
    const center = 100;
    const factor = 0.8; // Scale để không bị tràn ra mép (max 100 điểm * 0.8 = 80px từ tâm)

    const angleStep = (Math.PI * 2) / 6;
    const points = [
      metrics.skills || 0,
      metrics.keywords || 0,
      metrics.formatting || 0,
      metrics.experience || 0,
      metrics.projects || 0,
      metrics.awards || 0,
    ].map((val, i) => {
      const radius = val * factor;
      const angle = i * angleStep - Math.PI / 2; // Bắt đầu từ đỉnh 12h
      return {
        x: center + radius * Math.cos(angle),
        y: center + radius * Math.sin(angle),
      };
    });

    return points.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");
  };

  const RadarGrid = ({ levels = 4 }) => {
    const center = 100;
    const factor = 0.8;
    const angleStep = (Math.PI * 2) / 6;

    return [0.25, 0.5, 0.75, 1].map((level) => {
      const points = Array.from({ length: 6 })
        .map((_, i) => {
          const radius = 100 * level * factor;
          const angle = i * angleStep - Math.PI / 2;
          return `${center + radius * Math.cos(angle)},${center + radius * Math.sin(angle)}`;
        })
        .join(" ");
      return (
        <polygon
          key={level}
          points={points}
          fill="none"
          stroke="#e2e8f0"
          strokeWidth="1"
          strokeDasharray={level === 1 ? "" : "4 2"}
        />
      );
    });
  };

  return (
    <div className="flex flex-col min-h-screen bg-[#f8fafc]">
      <header className="flex items-center justify-between border-b border-slate-200 bg-white/80 backdrop-blur-md px-6 py-4 lg:px-12 sticky top-0 z-50">
        <div className="flex items-center gap-3">
          {/* <div className="size-9 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
             <Target className="w-5 h-5 text-white" />
          </div> */}
          <h2 className="text-slate-900 text-xl font-black tracking-tight">
            ResumeGuidePro{" "}
            <span className="text-blue-600 text-[10px] align-top px-1.5 py-0.5 bg-blue-50 rounded-full">
              v0.3
            </span>
          </h2>
        </div>
      </header>

      <main className="flex-1 max-w-[1240px] mx-auto w-full p-6 lg:p-12 space-y-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 text-center md:text-left">
          <div className="space-y-2">
            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900">
              {data ? "CV-JD Matching Analysis" : "The Ultimate ATS Toolkit"}
            </h1>
            <p className="text-slate-500 font-medium flex items-center justify-center md:justify-start gap-2 text-sm">
              <Zap className="w-4 h-4 text-orange-500" />
              Phân tích CV và JD để có nhìn tổng quan về khả năng thành công của
              bạn!
            </p>
          </div>

          {data && (
            <button
              onClick={() => {
                setShowInput(true);
                setData(null);
              }}
              className="px-5 py-2.5 bg-white border border-slate-200 rounded-xl text-sm font-bold text-slate-600 hover:bg-slate-50 transition-all shadow-sm"
            >
              Try again
            </button>
          )}
        </div>

        <section className="min-h-[500px]">
          <AnimatePresence mode="wait">
            {showInput ? (
              <motion.div
                key="input"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Cột 1: Tải CV */}
                  <div className="bg-white p-10 rounded-[2rem] border border-slate-200 shadow-xl flex flex-col items-center text-center space-y-6">
                    <div className="size-20 bg-blue-50 rounded-2xl flex items-center justify-center border-2 border-dashed border-blue-200 relative group transition-all hover:bg-white hover:border-blue-500 cursor-pointer">
                      <FileUp className="w-8 h-8 text-blue-500 group-hover:scale-110 transition-transform" />
                      <input
                        type="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        className="absolute inset-0 opacity-0 cursor-pointer"
                      />
                    </div>
                    <div>
                      <h3 className="text-lg font-black text-slate-800">
                        {file ? file.name : "Bước 1: Tải CV (PDF)"}
                      </h3>
                      <p className="text-slate-400 text-xs mt-1">
                        Dữ liệu được trích xuất tự động qua pypdf
                      </p>
                    </div>
                  </div>

                  {/* Cột 2: Nhập JD */}
                  <div className="bg-white p-10 rounded-[2rem] border border-slate-200 shadow-xl space-y-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Braces className="w-5 h-5 text-blue-600" />
                      <h3 className="text-lg font-black text-slate-800">
                        Bước 2: Nhập Job Description (Tùy chọn)
                      </h3>
                    </div>
                    <textarea
                      className="w-full h-32 p-4 bg-slate-50 border border-slate-100 rounded-xl outline-none focus:ring-2 focus:ring-blue-500/20 text-sm resize-none"
                      placeholder="Dán yêu cầu công việc vào đây để AI so khớp cụ thể kỹ năng và từ khóa..."
                      value={jdText}
                      onChange={(e) => setJdText(e.target.value)}
                    />
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={loading || !file}
                  className="w-1/2 mx-auto bg-blue-600 hover:bg-blue-700 text-white font-black py-6 rounded-[2rem] flex items-center justify-center gap-3 shadow-2xl shadow-blue-600/30 transition-all hover:-translate-y-1 active:scale-[0.98] disabled:opacity-30"
                >
                  {loading ? (
                    <Clock className="w-6 h-6 animate-spin" />
                  ) : (
                    <Zap className="w-6 h-6" />
                  )}
                  {loading
                    ? "AI đang so khớp CV với JD..."
                    : "Tiên hành phân tích"}
                </button>

                {loading && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="w-full max-w-2xl mx-auto bg-slate-900 rounded-2xl border border-slate-700 p-6 font-mono text-xs shadow-2xl relative overflow-hidden"
                  >
                    <div className="flex items-center gap-1.5 mb-4 border-b border-slate-800 pb-3">
                      <div className="size-2.5 rounded-full bg-red-500/80" />
                      <div className="size-2.5 rounded-full bg-yellow-500/80" />
                      <div className="size-2.5 rounded-full bg-green-500/80" />
                      <span className="ml-2 text-slate-500 font-bold uppercase tracking-wider">
                        Agent Thoughts Stream
                      </span>
                    </div>
                    <div className="space-y-2 h-40 overflow-y-auto custom-scrollbar">
                      {logs.map((log, i) => (
                        <div key={i} className="flex gap-3">
                          <span className="text-blue-500 font-bold shrink-0">
                            step-{i + 1}
                          </span>
                          <span className="text-slate-300">
                            {typeof log === "string"
                              ? log
                              : JSON.stringify(log)}
                          </span>
                        </div>
                      ))}
                      <div className="flex gap-2 items-center text-blue-400 animate-pulse">
                        <span className="size-1 rounded-full bg-blue-400" />
                        <span>Agent đang xử lý chuyên sâu...</span>
                      </div>
                    </div>
                    {/* Hiệu ứng tia sáng quét qua */}
                    <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-blue-500/5 to-transparent shadow-inner" />
                  </motion.div>
                )}
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-10"
              >
                {/* Red Flags & Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="bg-red-50 border border-red-100 p-8 rounded-3xl">
                    <h4 className="flex items-center gap-2 text-red-600 font-black text-xs uppercase mb-4">
                      <AlertTriangle className="w-4 h-4" /> Red Flags (Bị loại
                      thẳng)
                    </h4>
                    <ul className="space-y-3">
                      {Array.isArray(data?.red_flags) &&
                        data?.red_flags.map((flag, idx) => (
                          <li
                            key={idx}
                            className="text-xs text-red-800 flex gap-2"
                          >
                            <span className="shrink-0">•</span>
                            <span>{flag}</span>
                          </li>
                        ))}
                    </ul>
                  </div>
                  <div className="bg-slate-900 p-8 rounded-3xl text-white">
                    <h4 className="text-blue-400 font-black text-xs uppercase mb-4 flex items-center gap-2">
                      <Search className="w-4 h-4" /> Recruiter's Perspective
                    </h4>
                    <p className="text-sm font-medium italic text-slate-300 leading-relaxed">
                      "{data?.recruiter_summary}"
                    </p>
                  </div>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                  <div className="lg:col-span-4 bg-white p-10 rounded-3xl border border-slate-200 flex flex-col items-center justify-center shadow-lg relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-3">
                      <div className="px-2 py-1 bg-red-100 text-red-600 text-[8px] font-black rounded-full uppercase tracking-tighter">
                        Strict Mode
                      </div>
                    </div>
                    <p className="text-[10px] font-black uppercase text-slate-400 tracking-widest mb-6">
                      ATS Score (x/10)
                    </p>
                    <div className="relative">
                      <svg className="w-44 h-44 -rotate-90">
                        <circle
                          className="text-slate-100"
                          cx="88"
                          cy="88"
                          r="80"
                          fill="transparent"
                          stroke="currentColor"
                          strokeWidth="12"
                        />
                        <motion.circle
                          initial={{ strokeDashoffset: 502 }}
                          animate={{
                            strokeDashoffset:
                              502 - (502 * (data?.overall_score || 0)) / 10,
                          }}
                          className="text-red-500"
                          cx="88"
                          cy="88"
                          r="80"
                          fill="transparent"
                          stroke="currentColor"
                          strokeWidth="12"
                          strokeDasharray="502"
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-5xl font-black text-slate-900">
                          {data?.overall_score}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* DYNAMIC RADAR CHART */}
                  <div className="lg:col-span-8 bg-white p-12 rounded-3xl border border-slate-200 shadow-md flex flex-col md:flex-row items-center gap-12">
                    <div className="relative w-64 h-64 flex items-center justify-center">
                      <svg
                        viewBox="0 0 200 200"
                        className="absolute w-full h-full overflow-visible"
                      >
                        {/* Grid Layers */}
                        <RadarGrid />

                        {/* Data Polygon */}
                        <motion.polygon
                          initial={{ opacity: 0, scale: 0 }}
                          animate={{ opacity: 1, scale: 1 }}
                          points={getRadarPoints(data?.metrics)}
                          fill="rgba(239, 68, 68, 0.2)"
                          stroke="#ef4444"
                          strokeWidth="2"
                          strokeLinejoin="round"
                        />
                      </svg>

                      {/* Vertex Labels */}
                      <Label
                        text="Skills"
                        pos="-top-6 left-1/2 -translate-x-1/2"
                      />
                      <Label text="Keywords" pos="top-[15%] -right-10" />
                      <Label text="Format" pos="bottom-[15%] -right-10" />
                      <Label
                        text="Exp"
                        pos="-bottom-6 left-1/2 -translate-x-1/2"
                      />
                      <Label text="Projects" pos="bottom-[15%] -left-10" />
                      <Label text="Awards" pos="top-[15%] -left-10" />
                    </div>
                    <div className="flex-1 w-full grid grid-cols-2 gap-x-3 gap-y-4">
                      <MetricBar
                        label="Skills"
                        value={data?.metrics?.skills || 0}
                      />
                      <MetricBar
                        label="Keywords"
                        value={data?.metrics?.keywords || 0}
                      />
                      <MetricBar
                        label="Format"
                        value={data?.metrics?.formatting || 0}
                      />
                      <MetricBar
                        label="Exp"
                        value={data?.metrics?.experience || 0}
                      />
                      <MetricBar
                        label="Projects"
                        value={data?.metrics?.projects || 0}
                      />
                      <MetricBar
                        label="Awards"
                        value={data?.metrics?.awards || 0}
                      />
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                  <div className="lg:col-span-8 bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-sm">
                    <div className="p-10 h-[600px] overflow-y-auto custom-scrollbar prose prose-slate max-w-none">
                      <ReactMarkdown>
                        {typeof data?.detailed_analysis === "string"
                          ? data.detailed_analysis
                          : JSON.stringify(data?.detailed_analysis || "")}
                      </ReactMarkdown>
                    </div>
                  </div>
                  <div className="lg:col-span-4 space-y-8">
                    <div className="bg-slate-900 p-8 rounded-3xl text-white shadow-xl">
                      <h4 className="text-xs font-black uppercase text-blue-400 mb-6 flex items-center gap-2">
                        <MessageSquareQuote className="w-4 h-4" /> Smart
                        Interview
                      </h4>
                      <div className="space-y-6">
                        {Array.isArray(data?.mock_interview) &&
                          data?.mock_interview.map((m, i) => (
                            <div key={i} className="space-y-2">
                              <p className="text-sm font-bold text-slate-100">
                                Q: {m.question || "Đang phân tích câu hỏi..."}
                              </p>
                              <p className="text-[10px] text-slate-400 italic">
                                Target: {m.purpose || "N/A"}
                              </p>
                            </div>
                          ))}
                        {(!data?.mock_interview ||
                          data.mock_interview.length === 0) && (
                          <p className="text-xs text-slate-500">
                            AI chưa tạo câu hỏi phỏng vấn.
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="bg-blue-50 p-8 rounded-3xl border border-blue-100">
                      <h4 className="text-xs font-black text-blue-600 uppercase mb-4">
                        Checkpoints
                      </h4>
                      {Array.isArray(data?.checklist) &&
                        data?.checklist.map((c, i) => (
                          <div
                            key={i}
                            className="flex items-center justify-between py-2 border-b border-blue-100 last:border-0"
                          >
                            <span className="text-[11px] font-medium text-blue-700">
                              {c.label || "Tiêu chí không xác định"}
                            </span>
                            {c.status ? (
                              <CheckCircle className="w-3 h-3 text-blue-600" />
                            ) : (
                              <AlertTriangle className="w-3 h-3 text-orange-400" />
                            )}
                          </div>
                        ))}
                      {(!data?.checklist || data.checklist.length === 0) && (
                        <p className="text-[10px] text-slate-400">
                          Không có dữ liệu kiểm tra.
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </main>
    </div>
  );
}

// Helpers
function NavItem({ label, active }: { label: string; active?: boolean }) {
  return (
    <a
      className={cn(
        "text-sm font-bold opacity-50",
        active && "text-blue-600 opacity-100",
      )}
      href="#"
    >
      {label}
    </a>
  );
}

function MetricBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-[10px] font-black uppercase text-slate-400 tracking-widest">
        <span>{label}</span>
        <span className="text-blue-600">{value}%</span>
      </div>
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1.5 }}
          className="h-full bg-blue-600 rounded-full"
        />
      </div>
    </div>
  );
}

function Label({ text, pos }: { text: string; pos: string }) {
  return (
    <span
      className={cn(
        "absolute text-[10px] font-black text-slate-400 uppercase tracking-tighter",
        pos,
      )}
    >
      {text}
    </span>
  );
}

function cn(...inputs: any[]) {
  return inputs.filter(Boolean).join(" ");
}
