# EpiRecipes Search Platform

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose
- Python 3.8+
- Node.js 14+

### OpenSearch Setup
1. Install Docker and Docker Compose if not already installed.
2. Navigate to the project root directory.
3. Run the following command to start OpenSearch:
   ```
   docker-compose up -d
   ```
4. Wait for OpenSearch to fully start (this may take a few minutes).

### Data Ingestion and Indexing
1. Navigate to the Backend directory.
2. Run the data ingestion and indexing script:
   ```
   python scripts/ingest_data_to_opensearch.py
   ```
   This script will create the `epi_r_index` and ingest the data from the CSV file.

### Backend Setup
1. Navigate to the Backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env` file (see `.env.example` for required variables)
6. Run the Flask app: `python app.py`

### Frontend Setup
1. Navigate to the Frontend directory
2. Install dependencies: `npm install`
3. Start the React app: `npm start`

## API Endpoints
- GET /api/search: Search recipes
- GET /api/filters: Get available filters
- GET /api/top_rated: Get top-rated recipes
- GET /api/categories: Get recipe categories
- GET /api/popular_recipes: Get popular recipes
- GET /api/recipe/{id}: Get recipe details

## Technologies Used
- Backend: Flask
- Frontend: React
- Database: OpenSearch (running in Docker)
- Data Processing: Python scripts for ingestion and indexing
- Additional: Pixabay API for images
- Containerization: Docker and Docker Compose

## Notes
- The backend is configured to connect to OpenSearch using the `epi_r_index`.
- Make sure Docker is running and OpenSearch is fully started before running the backend application.
- The `index_recipes()` function in `app.py` is called when the app starts, but it's using a different index name ('recipes'). Consider updating this function or removing it if it's not needed.
