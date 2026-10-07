# 🌐 Workforce Intelligence Engine: UI Architecture

This directory (`/frontend`) contains the **Next.js 14 / React** frontend for the Workforce Intelligence Engine. 

It was built from the ground up to replace standard data-science dashboards (like Streamlit) with a world-class, Awwwards-quality intelligence product.

## 🏗️ Architecture Stack
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS (v4) with a bespoke Charcoal/Electric Cyan design system
- **Motion & Choreography:** Framer Motion & Anime.js
- **Icons:** Lucide React
- **Data Visualization Base:** Recharts

## 🎨 Design Philosophy
The interface enforces the fundamental product principle: **"The datasets meet at constructs, not at rows."** 
It utilizes:
- Deep Charcoal / Graphite surfaces
- Hairline borders (`border-white/10`)
- Subtle glassmorphism (`backdrop-blur`)
- Strict tabular numerals for scientific data
- A central Command Palette (`⌘K`)
- Progressive disclosure (avoiding "chart walls")

## 🚀 Running the Frontend

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies (if not already done)
npm install

# 3. Start the development server
npm run dev
```

Visit **`http://localhost:3000`** to experience the animated Hero workforce field and the full application dashboard.

## 📁 Key Directories
- `src/app/page.tsx`: The cinematic Landing Experience (WOW 1).
- `src/app/overview`: The Command Center and Big Finding insight cards.
- `src/app/market`: The Market Radar (Career Opportunity Frontier).
- `src/app/senior`: The SDS Forensics panel explicitly explaining the 0.998 AUC anomaly.
- `src/app/lab`: The Model Lab and Cross-Validation leaderboards.
- `src/components/Sidebar.tsx`: The global navigation shell.
