## Setup

1.  **Clone the repository**

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

## How to Run

1.  **Run the scraper:**
    This will populate `mcdonalds.db` file with the latest outlet data otherwise clear the db or use script
    ```bash
    python scraper/scraper.py
    ```

2.  **Run the backend server:**
    ```bash
    uvicorn api.main:app --reload
    ```

3.  **Open your browser** and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the McScraper, I guess.
