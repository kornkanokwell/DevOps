# DevOps
โครงงานรายวิชาการประยุกต์ใช้ CI/CD และการ Deploy เว็บแอปพลิเคชันบน Render.com

# Movie Booking 🎬
## Tech Stack
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy + Alembic
- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **DevOps**: Docker, GitHub Actions, Render.com

## Local Development

### Backend
\`\`\`bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`