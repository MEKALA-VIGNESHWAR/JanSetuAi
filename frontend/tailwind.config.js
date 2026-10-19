/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef8ff',
          100: '#d8efff',
          200: '#b9e2ff',
          300: '#89d1ff',
          400: '#52b7ff',
          500: '#2a97ff',
          600: '#1479f5',
          700: '#0c60e1',
          800: '#104db6',
          900: '#13428f',
          950: '#102957',
        },
         saffron: {
          500: '#f97316',
          600: '#ea580c',
        },
        forest: {
          500: '#10b981',
          600: '#059669',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
