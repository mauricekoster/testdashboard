/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    
    extend: {
      colors: {
        primary: {
          DEFAULT: '#5E81AC',
        }
      },
      brightness: ['hover'],
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

