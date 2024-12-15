from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

# Global variable to store progress messages
progress_message = None


# Progress hook function
def progress_hook(d):
    global progress_message

    # Only update progress when downloading
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', '').strip()
        if progress_message and percentage:
            try:
                progress_message.edit_text(f"Downloading... {percentage} complete")
            except:
                pass  # Ignore errors (e.g., if the message was deleted)


# Function to download video
def download_video(url, output_dir="/storage/emulated/0/Download"):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],  # Attach the progress hook
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


# Command handler: /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a video link to download.")


# Message handler: Download video
def download_handler(update: Update, context: CallbackContext):
    global progress_message

    url = update.message.text
    progress_message = update.message.reply_text("Preparing to download...")

    try:
        # Start the video download
        video_path = download_video(url)
        progress_message.edit_text("Uploading video...")

        # Send the video back to the user
        with open(video_path, 'rb') as video:
            update.message.reply_video(video)

        # Clean up the downloaded file
        os.remove(video_path)

        progress_message.edit_text("Download complete!")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")


# Main function
def main():
    API_TOKEN = "7332661762:AAH5RGDt5wGmYUGWV2DB8WjrkrYM2GXiDTw"  # Replace with your BotFather token

    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()