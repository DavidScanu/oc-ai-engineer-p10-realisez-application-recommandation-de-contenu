# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**My Content** - AI-powered article recommendation system built as an OpenClassrooms project. The application uses the Globo.com news dataset (3M clicks, 322K users, 46K articles) to demonstrate a production-ready recommendation engine with cold start handling.

**Stack:**
- Backend: Python 3.11+, FastAPI, scikit-learn
- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- Data: CSV interactions + article embeddings (250D vectors)

## Development Commands

### Backend (FastAPI)
```bash
cd backend

# Start API (recommended)
./start.sh

# Alternative: direct uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test API
python3 scripts/test_api.py

# Test cold start scenarios
python3 scripts/test_cold_start.py

# Run data analysis
python3 data-analysis/analyze_data.py
```

API runs on http://localhost:8000 with Swagger docs at /docs

### Frontend (Next.js)
```bash
cd frontend

# Start dev server (recommended)
./start.sh

# Alternative: manual start
npm install
cp .env.example .env.local
npm run dev

# Production build
npm run build
npm start

# Lint
npm run lint
```

Frontend runs on http://localhost:3000

### Git LFS
Large files (embeddings, clusters) use Git LFS. After cloning:
```bash
git lfs pull
```

## Architecture

### Backend Structure
```
backend/
├── main.py              # FastAPI app with all endpoints
├── config.py            # Settings (Pydantic BaseSettings)
├── models.py            # Pydantic response models
├── data_loader.py       # Centralized data management singleton
├── recommenders/        # 4 recommendation engines
│   ├── base.py         # BaseRecommender (ABC) with cold start logic
│   ├── popularity.py   # Age-normalized popularity with novelty boost
│   ├── content.py      # Embedding similarity + metadata fallback
│   ├── clustering.py   # K-means user segmentation (5 clusters)
│   └── hybrid.py       # Weighted combination (40% clustering, 30% content, 20% popularity, 10% diversity)
├── data/               # CSV files + embeddings (Git LFS)
└── scripts/            # Testing utilities
```

### Key Backend Concepts

**DataLoader Singleton** (`data_loader.py`):
- Single source of truth for all data access
- Lazy-loads CSV files and embeddings
- Provides helper methods: `get_user_history()`, `get_article_info()`, `get_recommendable_articles()`
- Auto-detects reference date from data (2017-11-13)

**Cold Start Handling** (all in `base.py`):
- `_has_sufficient_history(user_id)`: checks if user has ≥5 valid unique articles read
- `_get_valid_user_article_ids(user_id)`: filters history to valid article IDs only
- New users → automatic fallback to popularity method
- New articles → 1.5x boost if <24h, 1.2x if <72h (configured in `config.py`)

**Recommender Pattern**:
- All inherit from `BaseRecommender` (abstract base class)
- Must implement `recommend(user_id, n_recommendations, **kwargs)`
- Use `_format_recommendation()` for consistent output
- Lazy initialization in `main.py` via `get_recommender()` factory

**Endpoint Structure** (`main.py`):
- `POST /recommend/{user_id}?method=hybrid&n_recommendations=5&exclude_seen=true` - main recommendation endpoint
- `GET /users/active?limit=20` - most active users for frontend dropdown
- `GET /articles/recent?hours=48&category_id=281` - new articles (cold start solution)
- `GET /articles/popular?limit=10` - trending articles
- `GET /debug/config`, `GET /debug/data-stats` - debugging

### Frontend Structure
```
frontend/
├── app/
│   ├── page.tsx           # Main page: user selection + recommendations
│   ├── insights/page.tsx  # Analytics: popular & recent articles
│   ├── statistics/page.tsx # Data overview + top users
│   └── layout.tsx         # Global layout with navigation
├── components/
│   ├── ui/               # shadcn/ui components
│   ├── UserSelector.tsx  # Dropdown + manual search
│   ├── MethodSelector.tsx # 4-tab method switcher
│   ├── RecommendationCard.tsx
│   ├── UserStatsCard.tsx
│   └── FallbackAlert.tsx # Yellow/green status indicator
└── lib/
    ├── api.ts           # Typed API client (fetch wrapper)
    ├── types.ts         # TypeScript interfaces
    └── utils.ts         # Utilities (cn, etc.)
```

**API Client** (`lib/api.ts`):
- `apiClient.getRecommendations(userId, method, n, excludeSeen)`
- `apiClient.getActiveUsers(limit)`
- `apiClient.getPopularArticles(limit)`
- `apiClient.getRecentArticles(hours, categoryId, limit)`
- All methods handle errors and return typed responses

## Configuration

### Backend Config (`backend/config.py`)
Key settings in `Settings` class (Pydantic):
- `MIN_UNIQUE_ARTICLES_READ = 5` - cold start threshold (3=permissive, 5=balanced, 10=strict)
- `NOVELTY_BOOST_24H = 1.5` - new article boost <24h
- `NOVELTY_BOOST_72H = 1.2` - new article boost 24-72h
- `HYBRID_WEIGHTS` - dict with clustering/content/popularity/diversity weights
- `N_USER_CLUSTERS = 5` - number of K-means clusters
- `MAX_ARTICLE_AGE_DAYS = 730` - filter articles >2 years old
- `MIN_WORDS_COUNT = 50` - filter very short articles

### Frontend Config (`frontend/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Data Flow

### Recommendation Request Flow
1. **Frontend** calls `apiClient.getRecommendations(userId, method)`
2. **main.py** `POST /recommend/{user_id}` receives request
3. **Factory** `get_recommender(method)` creates/retrieves recommender instance
4. **Recommender** checks cold start via `_has_sufficient_history(user_id)`:
   - If insufficient → fallback to popularity method
   - If sufficient → proceed with requested method
5. **Recommender** calls `recommend()` → returns list of article IDs + scores
6. **main.py** formats response with metadata:
   - `fallback_applied: bool`
   - `actual_method` (may differ from requested)
   - `fallback_reason` (explanation if fallback occurred)
   - User stats, article metadata
7. **Frontend** displays recommendations + yellow alert if fallback occurred

### Cold Start Decision Tree
```
User requests method X for user Y
├─ method == "popularity" → execute directly (no history needed)
└─ method in ["content", "clustering", "hybrid"]
   ├─ _has_sufficient_history(Y)?
   │  ├─ YES → execute method X normally
   │  └─ NO → fallback to popularity method
   │     └─ Set: fallback_applied=true, actual_method="popularity"
```

## Common Tasks

### Adding a new endpoint
1. Define Pydantic response model in `backend/models.py`
2. Add endpoint function in `backend/main.py` with proper error handling
3. Add method to `lib/api.ts` in frontend (if needed)
4. Update TypeScript types in `lib/types.ts`

### Modifying recommendation logic
1. Edit relevant recommender in `backend/recommenders/`
2. Restart backend (`./start.sh`)
3. Test with `python3 scripts/test_api.py`
4. Check fallback scenarios with `scripts/test_cold_start.py`

### Adjusting cold start threshold
Edit `MIN_UNIQUE_ARTICLES_READ` in `backend/config.py` (no restart needed with uvicorn --reload)

### Adding a new recommender method
1. Create `backend/recommenders/my_method.py` inheriting `BaseRecommender`
2. Implement `recommend(user_id, n_recommendations, **kwargs)`
3. Add factory case in `main.py` `get_recommender()`
4. Add method option to `/recommend/{user_id}` validation
5. Update frontend `MethodSelector.tsx` with new tab

## Testing

### Backend
- `python3 scripts/test_api.py` - comprehensive API test suite
- `python3 scripts/test_cold_start.py` - cold start scenarios
- `curl http://localhost:8000/health` - quick health check
- Test users: 5890 (active), 1 (new user for cold start)

### Frontend
- `npm run build` - validates TypeScript + production build
- `npm run lint` - ESLint checks
- Manual testing: select user 1 or 322897 to trigger cold start fallback

## Important Notes

### Date Reference System
- `reference_date` (2017-11-13): last click in dataset - used for all temporal calculations
- `max_article_date` (2018-03-13): last article published - different dataset extraction time
- System correctly uses `reference_date` for recommendations to avoid "future" articles

### Embeddings & Large Files
- `articles_embeddings.pickle` (364MB): 250D Sentence-BERT vectors for all articles
- `clusters_cache.pkl` (5MB): cached K-means user clusters
- Managed via Git LFS - always run `git lfs pull` after clone

### Cold Start Philosophy
- **Users**: explicit fallback to popularity (transparent to user via API metadata)
- **Articles**: implicit boost via novelty multiplier (no separate fallback)
- **Validation**: checks both quantity (≥5 articles) AND quality (valid article IDs)

### Performance Considerations
- Embeddings loaded on-demand (first content recommendation request)
- Clusters computed lazily (first clustering recommendation)
- User interactions filtered efficiently via pandas DataFrames
- Recommendable articles pre-filtered (age, word count) and cached

## Deployment

### Backend → Azure Functions
- See `documentation/TODO.md` for Azure deployment tasks
- Requires: Python 3.11 runtime, consumption plan
- Environment variables: all settings from `config.py`

### Frontend → Vercel
```bash
cd frontend
vercel
# Set NEXT_PUBLIC_API_URL to production backend URL
```

### Frontend → Azure Static Web Apps
```bash
npm run build
az staticwebapp create --name my-content-frontend --resource-group my-content-rg --source .
```

## Troubleshooting

### "Backend not responding"
```bash
curl http://localhost:8000/health
cd backend && ./start.sh
```

### "Cannot connect to API" (frontend)
Check `frontend/.env.local` contains `NEXT_PUBLIC_API_URL=http://localhost:8000`

### "No recommendations returned"
- Verify user exists: `curl http://localhost:8000/users/5890/stats`
- Check fallback metadata in response JSON
- Use known good users: 5890, 7654, 12345

### "Missing embeddings error"
Run `git lfs pull` from repository root

### Port conflicts
```bash
# Kill port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## Code Style

- **Backend**: PEP 8, type hints encouraged, logging via `logger.info()`
- **Frontend**: Prettier defaults, TypeScript strict mode
- **Naming**: snake_case (Python), camelCase (TypeScript)
- **Comments**: docstrings for functions/classes, inline comments for complex logic
