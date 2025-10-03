# Project Overview: News Recommendation System MVP

## Educational Objectives
- Select appropriate software architecture for business needs
- Design and execute end-to-end AI processing pipelines

## Project Context

**My Content** is a startup aiming to encourage reading by recommending relevant content to users. As CTO and co-founder (alongside CEO Samia), you're building an MVP application.

### Initial Scope
- Test recommendation solution for articles and books for individuals
- Use publicly available data (Globo.com News Portal dataset) due to lack of user data
- Dataset includes: user interactions, article metadata (word count), session info (start/end times), and user interactions with articles

## Dataset Information

### Globo.com (G1) Dataset
- **Source**: Most popular news portal in Brazil
- **Period**: October 1-16, 2017
- **Scale**: ~3M clicks, 1M+ sessions, 314K users, 46K+ articles
- **Contents**:
  - User session interactions (clicks by hour in CSV files)
  - Article metadata (364K articles)
  - Article embeddings (250-dimensional vectors from CHAMELEON ACR module)
- **Note**: Full article text not provided due to licensing; embeddings available for content representation

### Key Dataset Files
- `clicks.csv` - User sessions and interactions
- `articles_metadata.csv` - Article information
- `articles_embeddings.pickle` - Pre-trained content embeddings

### Sample Data Structure
**Clicks**: user_id, session_id, session_start, session_size, click_article_id, click_timestamp, click_environment, click_deviceGroup, click_os, click_country, click_region, click_referrer_type

**Articles**: article_id, category_id, created_at_ts, publisher_id, words_count

## Core Requirement

**Critical User Story**: "As an application user, I will receive a selection of five articles."

**Key Architectural Consideration**: The solution must accommodate new users and new articles in the target architecture.

## Technical Guidance (from Julien, Web Developer)

### Recommended Architectures

**Option 1: API-Based**
- Create API to develop and expose recommendation system
- Use Azure Functions to connect application with recommendation system

**Option 2: Direct Integration**
- Skip API layer
- Use Azure Blob storage input binding to retrieve files and models
- Integrate predictions directly into Azure Functions

### Implementation Notes
- **Platform**: Azure Functions (serverless architecture recommended)
- **Application**: Simple local interface
  - List user IDs
  - Call Azure Functions with selected ID
  - Display 5 recommended articles
- **Tip**: If embeddings file is too large for free Azure tier, use PCA for dimensionality reduction

### Azure Management
⚠️ **Important**: Monitor and stop Azure services when not in use to avoid charges. OpenClassrooms is not responsible for Azure costs on personal accounts.

## Deliverables

### 1. Application
Simple application with serverless recommendation system that:
- Accepts user ID as input
- Returns top 5 article recommendations
- Demonstrates functionality to Samia and future users

### 2. Code Repository
Git-managed codebase (pushed to GitHub) enabling end-to-end deployment, including:
- All development scripts
- Deployment configurations
- Version control history

### 3. Presentation (PDF, 15-25 slides)
- Brief functional description of application
- Analysis of different models tested (advantages/disadvantages)
- Architecture diagram of implemented solution
- Presentation of recommendation system
- Target architecture diagram for handling new users/articles

## Presentation Format (20 minutes + 5 min discussion)

As CTO, present to Samia (played by evaluator):

1. **Model Approaches** (10 min) - Different modeling approaches tested
2. **System Features** (6 min) - Recommendation system functionality in application
3. **Technical Architecture** (2 min) - Architecture retained
4. **Demo** (2 min) - Live application demonstration
5. **Discussion** (5 min) - Evaluator challenges your choices
6. **Debrief** (5 min) - Joint reflection

## Recommendation Approaches to Consider

### 1. Content-Based
- User interaction (articles consulted) → Embedding similarity
- Calculate similarity scores (cosine) → Return similar article IDs
- **Missing**: Article titles and text (Solution: Use LLM API for title generation/summarization)

### 2. Collaborative Filtering
- **Option A**: User behavior clustering → Recommend articles similar users consulted
- **Option B**: Recommend articles frequently viewed together

### 3. RNN/Model Training
- Use embeddings and article metadata
- Train predictive models

## Infrastructure

### Backend
- Azure Functions
- API endpoint

### Frontend
- Local Next.js/Streamlit application

## Implementation Considerations

### New Users (Cold Start)
- Determine recommendation method when user ID doesn't exist
- Suggestion: Use popularity-based recommendations

### New Articles
- Process for adding to database:
  - Articles table
  - Clicks table
- Create embeddings for new content
- Automatic integration into recommendation pool

### Popularity Metric
- **Period**: Last 3 months
- **Normalization**: By article age to remove recency bias
  - Example: For 8-month-old article, divide by number of months

### Novelty Parameter
- Add novelty consideration to recommendations

## Technical Details from Research Paper

The project references the CHAMELEON meta-architecture for contextual hybrid session-based news recommendation using RNNs. Key insights:

- **Challenges addressed**: Fast item decay, extreme cold-start, high item volume, shifting user preferences
- **Approach**: Combines content, context, and collaborative signals
- **Modules**: ACR (Article Content Representation) + NAR (Next-Article Recommendation)
- **Features**: Recency, popularity, user context, article content embeddings
- **Evaluation**: Temporal protocol simulating realistic news portal dynamics