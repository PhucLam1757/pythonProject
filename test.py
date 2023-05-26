from pytube import YouTube
import os

# Link của video YouTube bạn muốn tải
video_url = "https://www.youtube.com/watch?v=0es3cayAwYw"

# Tạo đối tượng YouTube với URL của video
yt = YouTube(video_url)

# Lấy thông tin về video
video_title = yt.title
video_thumbnail = yt.thumbnail_url

print("Tiêu đề: ", video_title)
print("URL hình thu nhỏ: ", video_thumbnail)

# Chọn định dạng và chất lượng video bạn muốn tải
# Ở đây, chúng ta chọn định dạng đầu tiên (itag = 22) và chất lượng cao nhất
video = yt.streams.get_by_itag(22)

# Lưu video vào thư mục hiện tại
current_dir = os.getcwd()
video_path = os.path.join(current_dir, "video.mp4")

# Tải video xuống máy tính
video.download(output_path=current_dir, filename="video")

print("Video đã được tải xuống và lưu tại:", video_path)
