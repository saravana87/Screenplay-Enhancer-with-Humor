📬 Gmail Auto-Responder with LlamaIndex

This project monitors incoming emails (e.g., price inquiries), uses AI (LlamaIndex + OpenAI) to generate responses based on product data from a CSV, and automatically replies via Gmail.

Useful for anyone running a store and sending price alerts via email — users can just reply to ask about a product, and this bot answers for you.
✅ Features

    Reads incoming replies to your price alert emails (using Gmail API)

    Uses LlamaIndex + OpenAI to answer questions from product CSV

    Sends AI-generated replies in the same email thread

    Supports SKU, product name, brand, inventory, and price queries

    Keeps your business responsive 24×7, hands-free

🧠 How It Works

    You export your product data to products.csv

    The script indexes it using LlamaIndex and OpenAI embeddings

    It monitors your Gmail inbox for new replies with subject: "Price Update"

    When a user asks a question (e.g. “What’s the price of BK002?”):

        It finds the answer using the indexed data

        Sends an auto-reply in the same thread

🛠 Requirements

    Python 3.8+

    OpenAI API key

    Gmail account with Gmail API enabled
