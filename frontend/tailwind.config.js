/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        luxury: {
          emerald: '#284139',        // Primary Emerald Green
          wasabi: '#809078',         // Secondary Wasabi Green
          earth: '#B88230',          // Egyptian Earth (Accent/CTA)
          noir: '#111319',           // Noir de Vigne (Dark Base)
          card: '#1A1E24',           // Card/Container Background
          white: '#FFFFFF',
          grey: '#E5E5E5',           // Soft Grey (Body Text)
        },
      },
      fontFamily: {
        display: ['Playfair Display', 'Cinzel', 'serif'],
        body: ['Inter', 'Poppins', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
      boxShadow: {
        'luxury': '0 4px 20px rgba(40, 65, 57, 0.3)',
        'luxury-lg': '0 8px 30px rgba(40, 65, 57, 0.4)',
        'gold': '0 4px 20px rgba(184, 130, 48, 0.2)',
      },
    },
  },
  plugins: [],
}

