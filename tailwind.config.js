/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/src/templates/**/*.html",
    "./app/src/routes/**/*.py",
    "./app/src/templates/**/*.jinja2"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
  future: {
    hoverOnlyWhenSupported: true,
  },
  experimental: {
    optimizeUniversalDefaults: true,
  },
  // Suprimir advertencias específicas
  corePlugins: {
    preflight: true,
  },
  // Desactivar advertencias específicas
  variants: {
    extend: {},
  },
  // Configuración para reducir advertencias
  safelist: [
    {
      pattern: /^(bg-|text-|border-)/
    }
  ]
}
