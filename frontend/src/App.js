import React, { useState } from 'react';
import { Upload, Target, TrendingUp, CheckCircle2, Circle, Award, RefreshCw, BookOpen, Code, Lightbulb, ArrowRight, Star, Zap, Clock, BarChart3, Sparkles } from 'lucide-react';

// API Base URL - Update this to your backend URL
const API_BASE_URL = "https://agenticai-backend.onrender.com";

// UploadResume Component
const UploadResume = ({ onAnalysisComplete }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        setResumeFile(file);
        setError('');
      } else {
        setError('Please upload a PDF file only');
      }
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Please upload a PDF file only');
        return;
      }
      setResumeFile(file);
      setError('');
    }
  };

  const handleAnalyze = async () => {
    if (!resumeFile || !targetRole) {
      setError('Please upload resume and enter target role');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', resumeFile);
    formData.append('target_role', targetRole);

    try {
      const response = await fetch(`${API_BASE_URL}/upload-resume`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze resume');
      }

      const data = await response.json();
      onAnalysisComplete(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 p-4 md:p-8 flex items-center justify-center">
      <div className="max-w-4xl w-full">
        {/* Hero Section */}
        <div className="text-center mb-8 md:mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-sm rounded-3xl mb-6 animate-pulse">
            <Sparkles className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 leading-tight">
            Transform Your Career
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-2">
            AI-Powered Career Roadmap Generator
          </p>
          <p className="text-blue-200 text-sm md:text-base max-w-2xl mx-auto">
            Upload your resume and let our AI create a personalized 90-day learning plan to land your dream job
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-6 md:p-10 backdrop-blur-lg">
          <div className="space-y-8">
            {/* Step 1: Upload Resume */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-bold">
                  1
                </div>
                <label className="text-lg font-bold text-gray-900">
                  Upload Your Resume
                </label>
              </div>
              
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-2xl p-8 md:p-12 text-center transition-all ${
                  dragActive 
                    ? 'border-blue-500 bg-blue-50' 
                    : resumeFile 
                    ? 'border-green-400 bg-green-50' 
                    : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50/50'
                }`}
              >
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept=".pdf"
                  className="hidden"
                  id="resume-upload"
                  disabled={loading}
                />
                <label htmlFor="resume-upload" className="cursor-pointer block">
                  {resumeFile ? (
                    <div className="animate-in fade-in duration-300">
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                        <CheckCircle2 className="w-8 h-8 text-green-600" />
                      </div>
                      <p className="text-green-700 font-semibold text-lg mb-2">{resumeFile.name}</p>
                      <p className="text-green-600 text-sm">Ready to analyze!</p>
                    </div>
                  ) : (
                    <div>
                      <Upload className="w-12 h-12 md:w-16 md:h-16 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-700 font-semibold mb-2 text-base md:text-lg">
                        Drop your resume here or click to browse
                      </p>
                      <p className="text-sm text-gray-500">PDF format • Max 10MB</p>
                    </div>
                  )}
                </label>
              </div>
            </div>

            {/* Step 2: Target Role */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-bold">
                  2
                </div>
                <label className="text-lg font-bold text-gray-900">
                  What's Your Dream Role?
                </label>
              </div>
              
              <div className="relative">
                <Target className="absolute left-4 top-4 w-6 h-6 text-gray-400" />
                <input
                  type="text"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  placeholder="e.g., Senior Full Stack Developer, Data Scientist, Product Manager"
                  disabled={loading}
                  className="w-full pl-14 pr-4 py-4 border-2 border-gray-300 rounded-2xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-base md:text-lg"
                />
              </div>
              
              <div className="mt-4 flex flex-wrap gap-2">
                <span className="text-sm text-gray-500">Popular roles:</span>
                {['Full Stack Developer', 'Data Scientist', 'UX Designer', 'DevOps Engineer'].map(role => (
                  <button
                    key={role}
                    onClick={() => setTargetRole(role)}
                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs hover:bg-blue-200 transition-colors"
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm flex items-center gap-2 animate-in slide-in-from-top duration-300">
                <Circle className="w-4 h-4 fill-current" />
                {error}
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={!resumeFile || !targetRole || loading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-5 rounded-2xl font-bold text-lg hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-xl hover:shadow-2xl flex items-center justify-center gap-3"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-6 h-6 animate-spin" />
                  Analyzing Your Profile...
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  Generate My Career Roadmap
                  <ArrowRight className="w-6 h-6" />
                </>
              )}
            </button>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 border-t">
              {[
                { icon: Star, text: 'AI-Powered Analysis' },
                { icon: Clock, text: '90-Day Action Plan' },
                { icon: BarChart3, text: 'Track Your Progress' }
              ].map((feature, i) => (
                <div key={i} className="flex items-center gap-3 text-gray-600">
                  <feature.icon className="w-5 h-5 text-blue-600" />
                  <span className="text-sm font-medium">{feature.text}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ReadinessScore Component
const ReadinessScore = ({ score }) => {
  const getScoreColor = () => {
    if (score >= 80) return 'from-green-500 to-emerald-600';
    if (score >= 60) return 'from-blue-500 to-blue-700';
    if (score >= 40) return 'from-yellow-500 to-orange-600';
    return 'from-red-500 to-pink-600';
  };

  const getScoreLabel = () => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good Progress';
    if (score >= 40) return 'Getting There';
    return 'Just Started';
  };

  return (
    <div className={`bg-gradient-to-br ${getScoreColor()} rounded-2xl p-6 text-white shadow-lg transform hover:scale-105 transition-transform`}>
      <div className="flex items-center justify-between mb-4">
        <span className="text-white/90 font-medium">Career Readiness</span>
        <Award className="w-6 h-6" />
      </div>
      <div className="flex items-end gap-2 mb-3">
        <div className="text-5xl md:text-6xl font-bold">{score}</div>
        <div className="text-2xl text-white/80 mb-2">/ 100</div>
      </div>
      <div className="text-sm text-white/90 mb-4">{getScoreLabel()}</div>
      <div className="w-full bg-white/20 rounded-full h-2.5">
        <div
          className="bg-white rounded-full h-2.5 transition-all duration-1000 ease-out"
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
};

// SkillGap Component
const SkillGap = ({ missingSkills, currentSkills }) => {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
        <TrendingUp className="w-5 h-5 text-blue-600" />
        Skill Analysis
      </h3>
      
      <div className="space-y-5">
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-bold text-gray-700 uppercase tracking-wide">Your Skills</h4>
            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-semibold">
              {currentSkills?.length || 0} skills
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {currentSkills?.map(skill => (
              <span key={skill} className="px-4 py-2 bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 rounded-xl text-sm font-medium shadow-sm">
                ✓ {skill}
              </span>
            ))}
          </div>
        </div>
        
        <div className="border-t pt-5">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-bold text-gray-700 uppercase tracking-wide">Skills to Learn</h4>
            <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full font-semibold">
              {missingSkills?.length || 0} skills
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {missingSkills?.map(skill => (
              <span key={skill} className="px-4 py-2 bg-gradient-to-r from-orange-100 to-amber-100 text-orange-700 rounded-xl text-sm font-medium shadow-sm">
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Roadmap Component
const Roadmap = ({ roadmap, userId, onTaskComplete }) => {
  const [activeTab, setActiveTab] = useState('30');
  const [loading, setLoading] = useState(null);

  const handleMarkComplete = async (period, taskIndex) => {
    setLoading(`${period}-${taskIndex}`);
    
    try {
      const response = await fetch(`${API_BASE_URL}/update-progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          period: period,
          task_index: taskIndex,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to update progress');
      }

      await onTaskComplete();
    } catch (err) {
      console.error('Error updating progress:', err);
    } finally {
      setLoading(null);
    }
  };

  const tabs = [
    { days: '30', label: 'Foundation', color: 'blue' },
    { days: '60', label: 'Intermediate', color: 'purple' },
    { days: '90', label: 'Advanced', color: 'indigo' }
  ];

  const getTabColor = (color) => {
    const colors = {
      blue: 'border-blue-600 text-blue-600 bg-blue-50',
      purple: 'border-purple-600 text-purple-600 bg-purple-50',
      indigo: 'border-indigo-600 text-indigo-600 bg-indigo-50'
    };
    return colors[color];
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
        <Clock className="w-5 h-5 text-blue-600" />
        Your Learning Journey
      </h3>

      {/* Tabs */}
      <div className="flex flex-wrap gap-3 mb-6">
        {tabs.map(tab => (
          <button
            key={tab.days}
            onClick={() => setActiveTab(tab.days)}
            className={`flex-1 min-w-[140px] px-6 py-3 rounded-xl font-semibold transition-all transform hover:scale-105 ${
              activeTab === tab.days
                ? `${getTabColor(tab.color)} border-2 shadow-md`
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200 border-2 border-transparent'
            }`}
          >
            <div className="text-lg">{tab.days} Days</div>
            <div className="text-xs opacity-80">{tab.label}</div>
          </button>
        ))}
      </div>

      {/* Roadmap Items */}
      <div className="space-y-4">
        {roadmap?.[activeTab]?.map((item, index) => (
          <div 
            key={index} 
            className={`border-2 rounded-2xl p-5 transition-all ${
              item.completed 
                ? 'bg-green-50 border-green-200' 
                : 'bg-white border-gray-200 hover:border-blue-300 hover:shadow-md'
            }`}
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                {item.completed ? (
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center animate-in zoom-in duration-300">
                    <CheckCircle2 className="w-5 h-5 text-white" />
                  </div>
                ) : (
                  <div className="w-8 h-8 border-2 border-gray-300 rounded-full flex items-center justify-center">
                    <Circle className="w-5 h-5 text-gray-300" />
                  </div>
                )}
              </div>

              <div className="flex-1">
                <h4 className={`text-lg font-bold mb-3 ${item.completed ? 'text-green-700 line-through' : 'text-gray-900'}`}>
                  {item.skill}
                </h4>

                <div className="space-y-3 text-sm">
                  <div className="flex items-start gap-3 bg-blue-50 p-3 rounded-xl">
                    <Target className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-semibold text-blue-900 mb-1">Learning Goal</div>
                      <p className="text-blue-700">{item.goal}</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3 bg-purple-50 p-3 rounded-xl">
                    <BookOpen className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-semibold text-purple-900 mb-1">Resources</div>
                      <p className="text-purple-700">{item.resources}</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3 bg-green-50 p-3 rounded-xl">
                    <Code className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-semibold text-green-900 mb-1">Practice Project</div>
                      <p className="text-green-700">{item.mini_project}</p>
                    </div>
                  </div>
                </div>

                {!item.completed && (
                  <button
                    onClick={() => handleMarkComplete(activeTab, index)}
                    disabled={loading === `${activeTab}-${index}`}
                    className="mt-4 w-full md:w-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-300 disabled:to-gray-400 transition-all font-semibold flex items-center justify-center gap-2 shadow-md hover:shadow-lg transform hover:scale-105"
                  >
                    {loading === `${activeTab}-${index}` ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        Updating...
                      </>
                    ) : (
                      <>
                        <CheckCircle2 className="w-4 h-4" />
                        Mark as Complete
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ProgressTracker Component
const ProgressTracker = ({ userId, progress, onRefresh }) => {
  const [loading, setLoading] = useState(false);

  const handleRefreshScore = async () => {
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/adaptive-roadmap/${userId}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to refresh score');
      }

      const data = await response.json();
      await onRefresh(data);
    } catch (err) {
      console.error('Error refreshing score:', err);
    } finally {
      setLoading(false);
    }
  };

  const completionPercentage = progress?.completion_percentage || 0;
  const completedTasks = progress?.completed_tasks || 0;
  const totalTasks = progress?.total_tasks || 0;

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
        <BarChart3 className="w-5 h-5 text-blue-600" />
        Progress Overview
      </h3>

      <div className="space-y-5">
        <div>
          <div className="flex justify-between items-center mb-3">
            <span className="text-sm font-semibold text-gray-700">Overall Completion</span>
            <span className="text-2xl font-bold text-blue-600">{completionPercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4 shadow-inner">
            <div
              className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full h-4 transition-all duration-1000 ease-out shadow-md"
              style={{ width: `${completionPercentage}%` }}
            />
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 border border-blue-100">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <Lightbulb className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-gray-900">Tasks Completed</span>
          </div>
          <p className="text-4xl font-bold text-blue-600">
            {completedTasks} <span className="text-xl text-gray-500">of {totalTasks}</span>
          </p>
          <div className="mt-3 flex items-center gap-2 text-sm text-gray-600">
            <Star className="w-4 h-4 text-yellow-500 fill-current" />
            Keep up the great work!
          </div>
        </div>

        <button
          onClick={handleRefreshScore}
          disabled={loading}
          className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all flex items-center justify-center gap-2 font-semibold shadow-md hover:shadow-lg transform hover:scale-105 disabled:from-gray-300 disabled:to-gray-400"
        >
          {loading ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              Updating...
            </>
          ) : (
            <>
              <RefreshCw className="w-5 h-5" />
              Update Adaptive Score
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  const [userId, setUserId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [progressData, setProgressData] = useState(null);

  const handleAnalysisComplete = async (data) => {
    setUserId(data.user_id);
    setAnalysisData(data);
    await fetchProgress(data.user_id);
  };

  const fetchProgress = async (uid) => {
    try {
      const response = await fetch(`${API_BASE_URL}/progress/${uid}`);
      if (response.ok) {
        const data = await response.json();
        setProgressData(data);
      }
    } catch (err) {
      console.error('Error fetching progress:', err);
    }
  };

  const handleTaskComplete = async () => {
    if (userId) {
      await fetchProgress(userId);
    }
  };

  const handleRefreshScore = async (data) => {
    setAnalysisData(prev => ({
      ...prev,
      readiness_score: data.readiness_score,
      roadmap: data.roadmap,
    }));
    await fetchProgress(userId);
  };

  if (!userId) {
    return <UploadResume onAnalysisComplete={handleAnalysisComplete} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-3xl shadow-xl p-6 md:p-8 mb-8 border border-gray-100">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Career Dashboard
                </h1>
              </div>
              <p className="text-gray-600 text-sm md:text-base ml-15">
                🎯 Target Role: <span>{analysisData?.market_profile?.trend}</span>
              </p>
            </div>
            <button
              onClick={() => {
                setUserId(null);
                setAnalysisData(null);
                setProgressData(null);
              }}
              className="px-6 py-3 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 border-2 border-gray-300 rounded-xl hover:from-gray-200 hover:to-gray-300 transition-all font-semibold transform hover:scale-105"
            >
              ← Start New Analysis
            </button>
          </div>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
          {/* Left Column - Metrics */}
          <div className="lg:col-span-1 space-y-6">
            <ReadinessScore
               score={analysisData?.roadmap?.career_readiness_score || 0}
            />


<SkillGap
  missingSkills={analysisData?.skill_gap?.missing_skills || []}
  currentSkills={analysisData?.student_profile?.skills || []}
/>
            <ProgressTracker
              userId={userId}
              progress={progressData}
              onRefresh={handleRefreshScore}
            />
          </div>

          {/* Right Column - Roadmap */}
          <div className="lg:col-span-2">
            <Roadmap
              roadmap={analysisData?.roadmap}
              userId={userId}
              onTaskComplete={handleTaskComplete}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;