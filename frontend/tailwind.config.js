/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        charcoal: '#18202b',
        ink: '#202833',
        mutedBlue: {
          50: '#f4f8fb',
          100: '#e7eef5',
          500: '#4f7296',
          600: '#425f7d',
          700: '#334a62',
        },
      },
      boxShadow: {
        panel: '0 10px 30px rgba(15, 23, 42, 0.06)',
      },
    },
  },
  plugins: [],
};
