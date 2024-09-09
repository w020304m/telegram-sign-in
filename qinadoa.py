import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup

# 从环境变量中读取 API ID、API HASH 和 Bot 用户名
api_id = int(os.getenv("API_ID"))  # 从环境变量读取 API ID
api_hash = os.getenv("API_HASH")  # 从环境变量读取 API Hash
bot_username = os.getenv("BOT_USERNAME")  # 从环境变量读取机器人的用户名

# 创建 Pyrogram 客户端
app = Client("my_account", api_id=api_id, api_hash=api_hash)

# 定义一个异步函数，用于签到
async def sign_in():
    async with app:
        # 向机器人发送 /start 指令
        await app.send_message(bot_username, "/start")
        
        # 捕获机器人回复的消息
        @app.on_message(filters.chat(bot_username) & filters.text)
        async def handle_message(client, message):
            # 检查是否有内联按钮（即卡片）
            if message.reply_markup and isinstance(message.reply_markup, InlineKeyboardMarkup):
                # 查找含有 "签到" 的按钮
                for row in message.reply_markup.inline_keyboard:
                    for button in row:
                        if button.text == "签到":  # 确认按钮的文本是“签到”
                            # 点击该按钮
                            await app.request_callback_answer(
                                chat_id=message.chat.id, 
                                message_id=message.message_id, 
                                callback_data=button.callback_data
                            )
                            print("已点击签到按钮！")
                            return
            
            # 输出机器人返回的消息
            if "签到成功" in message.text:
                print(f"签到成功: {message.text}")
            else:
                print(f"收到消息: {message.text}")

        # 持续运行以等待消息
        await app.idle()

# 运行客户端并签到
app.run(sign_in())
