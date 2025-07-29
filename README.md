# AI Telegram SMM Assistant Bot

This is a Telegram bot that acts as a personal SMM assistant, powered by an AI model. It includes an admin panel for user management and request tracking.

## Features

- AI-powered SMM advice.
- Admin panel to view user statistics.
- Ability for admin to view user chat history.
- Conversation history management (clearing history).
- Secure configuration using a `.env` file.

## Prerequisites

- Python 3.10+

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repository-url>
   cd AI_TelegramBot
   ```

2. **Create and activate a virtual environment:**
   ```sh
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**
   - Create a `.env` file by copying the example file:
     ```sh
     # For Windows
     copy .env.example .env

     # For macOS/Linux
     cp .env.example .env
     ```
   - Open the `.env` file and add your credentials.

## Running the Bot

To start the bot, run the following command:

```sh
python main.py
```

## Configuration

The following environment variables are used for configuration:

- `BOT_TOKEN`: Your Telegram Bot Token.
- `OPENAI_API_KEY`: Your API key for the AI model (e.g., OpenRouter, OpenAI).
- `ADMIN_ID`: Your personal Telegram User ID for admin access.