# Algo-Trading System with ML & Automation

## Project Overview

This project is a Python-based mini algo-trading prototype designed to demonstrate a complete automated trading pipeline. It connects to a free stock data API, implements a rule-based trading strategy, and automates the logging of all trade analytics to a Google Sheet.

The system is built with a modular and scalable structure, adhering to best practices for code quality and documentation. This project showcases the ability to integrate various components—from data ingestion to a custom trading strategy and external API automation—into a single, cohesive application.

## Trading Strategy

The core trading strategy implemented in this prototype is based on a combination of two well-known technical indicators. This approach aims to identify strong bullish momentum in an oversold market condition.

### 1. **Relative Strength Index (RSI)**
The 14-day RSI is used to gauge momentum and identify potential entry points. A buy signal is initially triggered when the RSI falls **below 30**, indicating that the stock may be oversold and due for a price bounce.

### 2. **Moving Average Crossover**
To confirm the RSI signal and filter out false positives, we use a moving average crossover. A buy is only executed if, on the same day as the RSI condition, the **20-day simple moving average (20-DMA) crosses above the 50-day simple moving average (50-DMA)**. This is a classic bullish signal, confirming a shift in momentum from short-term bearish to short-term bullish.

This strategy was backtested for a period of 6 months on several NIFTY 50 stocks to analyze its performance.

## Setup & Prerequisites

Project Structure

├── .venv/-------------------# Python virtual environment----------------------------------------------------------------
├── .gitignore---------------# Files to ignore for Git-----------------------------------------------------------------------
├── config.ini---------------# Configuration for API keys, stocks, etc.------------------------------------------------------
├── data_handler.py----------# Functions for fetching and processing stock data--------------------------------------------------------------------
├── strategy.py--------------# Contains the trading strategy logic and backtesting engine-------------------------------------------------------
├── google_sheets_api.py-----# Handles all interactions with the Google Sheets API----------------------------------------------------------------
├── ml_model.py--------------# (Bonus) Placeholder for the ML model--------------------------------------------------------------------------------
├── telegram_alerts.py-------# (Bonus) Functions for sending Telegram notifications------------------------------------------------------------
├── main.py------------------# The main script to run the entire system--------------------------------------------------------------------------
├── requirements.txt---------# List of Python dependencies------------------------------------------------------------------------------------------
└── service_account.json-----# Google Sheets API credentials (add to .gitignore!)---------------------------------------------------------------
To run this project, you need a system with Python 3.8 or higher installed.

1.  **Clone this repository:**
    ```bash
    git clone [your-repo-link]
    cd [your-repo-name]
    ```

2.  **Create and activate a virtual environment:**
    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv .venv
    # Activate on macOS/Linux
    source .venv/bin/activate
    # Activate on Windows
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The `requirements.txt` file lists all the necessary Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Google Sheets API Setup:**
    This is a critical step for the automation component.
    * Follow the detailed instructions to create a Google Service Account in the [Google Cloud Console](https://console.cloud.google.com/).
    * Enable the Google Sheets API and Google Drive API for your new project.
    * Create a JSON key file for your service account, rename it to `service_account.json`, and place it in the project's root directory.
    * Create a Google Sheet named "Algo Trading Log" and share it with your service account's email address.

5.  **Configure `config.ini`:**
    * Open the `config.ini` file and fill in the paths and credentials. The file's structure is already provided.
    * **Important:** This file contains sensitive information. Do **not** commit it to your public repository. It is included in the `.gitignore` file for this purpose.

## How to Run

Execute the main script from your terminal:
```bash
python main.py
