# Dự án phát triển Bot cho Server Toán - Tin trên Discord
CMDBot là một dự án mã nguồn mở phát triển Bot cho [Server Toán - Tin](https://discord.gg/bfhvzcJd) trên nền tảng Discord, mục tiêu của dự án là để tạo một môi trường giúp các bạn sinh viên trên server có thể ứng dụng ngay kiến thức lập trình ở trên trường của mình vào một dự án thực tế để đỡ nhàm chán hơn trong việc học, cũng như sẽ giúp và cung cấp cho các bạn một tư duy về phát triển phần mềm từ sớm.s
`(CMDBot = Computer Science + Math + Data Science Bot)`

## Yêu cầu
- Đã cài đặt [Python](https://www.python.org)
- Đã tải source code về
- Đã tạo bot và server riêng để chạy thử nghiệm ([hướng dẫn](https://realpython.com/how-to-make-a-discord-bot-python/))

## Cách dùng
1. Mở terminal ở thư mục chứa source code
2. Tải package cần thiết
```bash
pip install -r requirements.txt
```
3. Tạo file `.env` với cấu trúc như sau
```
DISCORD_TOKEN=<Token của bot>
COMMAND_PREFIX=<Tiền tố command>
GUILD_ID=<ID của server>
WELCOME_CHANNEL_ID=<ID của kênh chào mừng>
ADMIN_ROLE=<Tên role của admin>
MODERATOR_ROLE=<Tên role của quản lý>
```
4. Chạy bot
```bash
python3 main.py
```
