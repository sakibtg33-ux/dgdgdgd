# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL

import logging
import asyncio
import json
import os
import shutil
import time
from datetime import datetime
from plugins.config import Config
from plugins.script import Translation
from plugins.functions.display_progress import progress_for_pyrogram
from plugins.database.database import db
from plugins.functions.ran_text import random_char

cookies_file = 'cookies.txt'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def youtube_dl_call_back(bot, update):
    try:
        cb_data = update.data
        tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
        random1 = random_char(5)

        # ---------------- SAFETY CHECK ----------------
        if not update.message or not update.message.reply_to_message:
            await update.answer("⚠️ Please reply to the original link message!", show_alert=True)
            return

        if not update.message.reply_to_message.text:
            await update.answer("⚠️ Replied message has no text!", show_alert=True)
            return

        youtube_dl_url = update.message.reply_to_message.text.strip()

        # ---------------- ENSURE DOWNLOAD FOLDER ----------------
        os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)

        save_json = os.path.join(
            Config.DOWNLOAD_LOCATION,
            f"{update.from_user.id}{ranom}.json"
        )

        if not os.path.exists(save_json):
            await update.answer("⚠️ Session expired! Send link again.", show_alert=True)
            return

        with open(save_json, "r", encoding="utf8") as f:
            response_json = json.load(f)

        custom_file_name = f"{response_json.get('title','video')}_{youtube_dl_format}.{youtube_dl_ext}"

        await update.message.edit_caption(
            caption=Translation.DOWNLOAD_START.format(custom_file_name)
        )

        # ---------------- TEMP DIRECTORY ----------------
        tmp_dir = os.path.join(
            Config.DOWNLOAD_LOCATION,
            f"{update.from_user.id}{random1}"
        )
        os.makedirs(tmp_dir, exist_ok=True)

        output_path = os.path.join(tmp_dir, custom_file_name)

        # ---------------- YT-DLP COMMAND ----------------
        command = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--embed-subs",
            "--hls-prefer-ffmpeg",
            "--cookies", cookies_file,
            youtube_dl_url,
            "-o", output_path,
            "--no-warnings"
        ]

        if Config.HTTP_PROXY:
            command.extend(["--proxy", Config.HTTP_PROXY])

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        error_text = stderr.decode().strip()

        if process.returncode != 0:
            await update.message.edit_caption(
                caption=f"❌ Download Failed:\n{error_text}"
            )
            return

        # ---------------- FIND DOWNLOADED FILE ----------------
        if not os.path.isfile(output_path):
            for file in os.listdir(tmp_dir):
                output_path = os.path.join(tmp_dir, file)
                break

        if not os.path.isfile(output_path):
            await update.message.edit_caption(
                caption="❌ Downloaded file not found!"
            )
            return

        file_size = os.stat(output_path).st_size

        if file_size > Config.TG_MAX_FILE_SIZE:
            await update.message.edit_caption(
                caption="⚠️ File exceeds Telegram limit!"
            )
            return

        await update.message.edit_caption(
            caption=Translation.UPLOAD_START.format(custom_file_name)
        )

        start_time = time.time()

        await update.message.reply_document(
            document=output_path,
            caption=response_json.get("fulltitle", ""),
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.UPLOAD_START,
                update.message,
                start_time
            )
        )

        # ---------------- CLEANUP ----------------
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if os.path.exists(save_json):
            os.remove(save_json)

        await update.message.edit_caption(
            caption="✅ Upload Completed Successfully!"
        )

    except Exception as e:
        logger.error(f"CRITICAL ERROR: {e}")
        try:
            await update.answer("❌ Unexpected error occurred!", show_alert=True)
        except:
            pass
