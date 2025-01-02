/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/src/templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
}
