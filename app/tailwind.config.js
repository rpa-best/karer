/** @type {import('tailwindcss').Config} */
import primeui from 'tailwindcss-primeui'

export default {
  content: [
    "./src/**/*.{html,js}",
    "./pages/**/*.{js,ts,vue}",
    "./components/**/*.{js,ts,vue}",
  ],
  darkMode: false,
  theme: {
    extend: {},
  },
  plugins: [primeui, require("tailwindcss-animated")],
}