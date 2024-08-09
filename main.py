import tkinter as tk
from threading import Thread
from queue import Queue, Empty
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import asyncio

# Replace with your Telegram bot token
TOKEN = ''

# Initialize a queue for communication between threads
queue = Queue()

# Function to update the Tkinter window background color
def change_color(color):
    try:
        root.config(bg=color)
    except tk.TclError:
        print(f"Invalid color: {color}")

# Function to handle messages received by the bot
async def change_background(update: Update, context) -> None:
    color = update.message.text.lower()
    queue.put(color)  # Send the color to the queue
    if queue.put(color):
        await update.message.reply_text(f"Background color changed to {color}!")
    else:
        await update.message.reply_text(f"Invalid color: {color} ")

# Function to start the Telegram bot
def run_bot():
    # Configure logging for the bot
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Define the start command handler
    async def start(update: Update, context) -> None:
        await update.message.reply_text("Send me a color name to change the background!")

    # Set up a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Create an instance of the Telegram application
    application = Application.builder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, change_background))

    # Run the bot's polling loop within the event loop
    try:
        loop.run_until_complete(application.run_polling())
    except Exception as e:
        logging.error(f"Error running the bot: {e}")

# Function for the GUI loop
def run_gui():
    while True:
        try:
            # Get the color from the queue
            color = queue.get(block=False)
            change_color(color)
        except Empty:
            pass  # No new color to change
        root.update_idletasks()
        root.update()

# Create the Tkinter window
root = tk.Tk()
root.title("Background Control with Telegram")
root.geometry("400x300")

# Start the bot thread
thread_bot = Thread(target=run_bot, daemon=True)
thread_bot.start()

# Run the GUI in the main thread
run_gui()
