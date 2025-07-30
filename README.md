# Full-Stack Market Sentiment Analysis Platform

This is a full-stack web application that fetches historical financial news for a given stock ticker, performs sentiment analysis on the headlines using a FinBERT model, and displays the daily average sentiment on an interactive dashboard.

---
## Purpose & Insights

This tool is designed to provide a quick, visual understanding of the media sentiment surrounding a public company. By selecting a stock ticker and fetching the 7-day history, a user can instantly see:

- **Sentiment Trend:** Whether the news narrative for the stock has been trending positive, negative, or neutral over the past week.
- **Daily Average Score:** A single, aggregated score for each day, which smooths out the noise from individual articles and provides a clearer picture of that day's overall tone.

Essentially, this platform helps answer the question: **"What has the general feeling of the news been for this company recently?"**

---

## System Architecture

The application consists of three main components that work together:

1.  **Frontend:** A static web page built with HTML and vanilla JavaScript. It uses Chart.js for data visualization.
2.  **Backend API:** A Python backend built with FastAPI that serves the frontend, provides data endpoints, and communicates with the database.
3.  **Database:** A PostgreSQL database managed by Docker, used to store and retrieve historical sentiment analysis results.

---

## Features

- **Backend:** Python, FastAPI
- **NLP Model:** `ProsusAI/finbert` for sentiment analysis.
- **Database:** PostgreSQL, managed with Docker and Docker Compose.
- **Frontend:** HTML, JavaScript, Chart.js for interactive charts.
- **Data Source:** Live financial news from the NewsAPI.

---

## How to Run Locally

1.  **Prerequisites:**
    - Python 3.9+
    - Docker Desktop

2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/saakshh/sentiment-analysis-platform.git](https://github.com/saakshh/sentiment-analysis-platform.git)
    cd sentiment-analysis-platform
    ```

3.  **Set up the environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Start the database:**
    Make sure Docker Desktop is running, then start the PostgreSQL container.
    ```bash
    docker compose up -d
    ```

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

6.  **View the Dashboard:**
    Open your browser and navigate to **`http://127.0.0.1:8000`**.
