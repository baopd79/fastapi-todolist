import type { Config } from "tailwindcss";

const config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          '"Geist Sans"',
          "Arial",
          "Apple Color Emoji",
          "Segoe UI Emoji",
          "Segoe UI Symbol",
          "sans-serif",
        ],
        mono: [
          '"Geist Mono"',
          "ui-monospace",
          "SFMono-Regular",
          "Roboto Mono",
          "Menlo",
          "Monaco",
          "Liberation Mono",
          "DejaVu Sans Mono",
          "Courier New",
          "monospace",
        ],
      },
      colors: {
        canvas: "#ffffff",
        ink: "#171717",
        muted: "#4d4d4d",
        subtle: "#666666",
        disabled: "#808080",
        ring: "#ebebeb",
        wash: "#fafafa",
        link: "#0072f5",
        focus: "hsla(212, 100%, 48%, 1)",
        develop: "#0a72ef",
        preview: "#de1d8d",
        ship: "#ff5b4f",
        badge: {
          blue: "#ebf5ff",
          text: "#0068d6",
        },
      },
      borderRadius: {
        control: "6px",
        card: "8px",
        media: "12px",
      },
      boxShadow: {
        ring: "rgba(0,0,0,0.08) 0px 0px 0px 1px",
        "ring-light": "rgb(235,235,235) 0px 0px 0px 1px",
        card: "rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 2px, #fafafa 0px 0px 0px 1px",
        "card-full":
          "rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 2px, rgba(0,0,0,0.04) 0px 8px 8px -8px, #fafafa 0px 0px 0px 1px",
      },
      maxWidth: {
        app: "1200px",
      },
    },
  },
  plugins: [],
} satisfies Config;

export default config;
