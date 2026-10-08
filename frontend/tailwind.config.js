/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        civic: {
          50: '#ecfeff',
          500: '#10b981',
          700: '#047857',
        },
      },
    },
  },
  plugins: [],
};
