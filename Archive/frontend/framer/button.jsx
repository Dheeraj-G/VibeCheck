import React from "react";
import { motion } from "framer-motion";

/**
 * @typedef {Object} Props
 * @property {string} [title] - Button text
 * @property {string} [link] - URL to open
 * @property {boolean} [newTab] - Open link in new tab
 * @property {boolean} [smoothScroll] - Enable smooth scroll
 * @property {React.CSSProperties} [style] - Custom styles
 * @property {string} [className] - Custom className
 * @property {React.ReactNode} [children] - Children
 */

const defaultStyle = {
  borderRadius: 8,
  padding: "0px 24px",
  height: 44,
  minWidth: 120,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  background: "linear-gradient(180deg, rgb(19, 20, 21) 0%, rgb(5, 5, 5) 100%)",
  color: "#fff",
  cursor: "pointer",
  position: "relative",
  overflow: "visible",
  border: "none",
  outline: "none",
  fontWeight: 700,
  fontFamily: 'Satoshi, sans-serif',
  fontSize: 16,
};

const hoverVariants = {
  initial: {
    background: "linear-gradient(180deg, rgb(19, 20, 21) 0%, rgb(5, 5, 5) 100%)",
    boxShadow: "0 0 0px rgba(255,255,255,0)",
  },
  hover: {
    background: "linear-gradient(180deg, rgb(34, 38, 35) 0%, rgb(5, 5, 5) 100%)",
    boxShadow: "0 0 16px 2px rgba(255,255,255,0.15)",
    transition: { type: "spring", stiffness: 500, damping: 60 },
  },
};

export default function Button({
  title = "Hover me",
  link,
  newTab = false,
  smoothScroll = false,
  className = "",
  style = {},
  children,
  ...rest
}) {
  const content = (
    <motion.div
      variants={hoverVariants}
      initial="initial"
      whileHover="hover"
      style={{ ...defaultStyle, ...style }}
      className={className}
      {...rest}
    >
      {children || title}
    </motion.div>
  );

  if (link) {
    return (
      <a
        href={link}
        target={newTab ? "_blank" : undefined}
        rel={newTab ? "noopener noreferrer" : undefined}
        style={{ textDecoration: "none" }}
        {...(smoothScroll ? { scroll: "smooth" } : {})}
      >
        {content}
      </a>
    );
  }
  return content;
}
