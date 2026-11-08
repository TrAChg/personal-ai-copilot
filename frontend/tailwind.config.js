/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fr: {
          navy: '#002654',
          blue: '#0055A5',
          bg: '#F8FAFC',
          card: '#FFFFFF',
          border: '#002654',
          hairline: '#CBD5E1',
          text: '#0F172A',
          muted: '#475569',
        }
      },
      borderRadius: {
        DEFAULT: '0px',
        none: '0px',
        sm: '0px',
        md: '0px',
        lg: '0px',
        xl: '0px',
        '2xl': '0px',
        '3xl': '0px',
        full: '0px',
      }
    },
  },
  plugins: [],
}

