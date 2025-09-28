"use client";

import * as React from "react";

interface CircularProgressProps {
  // The size of the circular progress bar (width and height).
  size?: number;
  // The width of the progress bar's stroke.
  strokeWidth?: number;
  // The current progress value (0 to 100).
  progress: number;
  // The color of the progress bar.
  color?: string;
  // The color of the background circle.
  trailColor?: string;
  // Whether to show the progress percentage text in the center.
  showPercentage?: boolean;
  // Custom class name for additional styling.
  className?: string;
}

const CircularProgress: React.FC<CircularProgressProps> = ({
  size = 65,
  strokeWidth = 3,
  progress,
  color = "hsl(var(--primary))",
  trailColor = "hsl(var(--secondary))",
  showPercentage = true,
  className = "",
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={trailColor}
          strokeWidth={strokeWidth}
          fill="transparent"
          className="transition-all duration-300"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-300"
        />
      </svg>
      {showPercentage && (
        <span
          className="absolute font-semibold"
          style={{ color: color }}
        >
          {`${Math.round(progress)}%`}
        </span>
      )}
    </div>
  );
};

export default CircularProgress;
