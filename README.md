Ứng dụng Mô phỏng Blockchain (Blockchain Demo App)

Dự án này là một ứng dụng web tương tác được xây dựng bằng Python và Streamlit, nhằm minh họa trực quan các khái niệm cốt lõi của Blockchain như: cấu trúc Khối (Block), cơ chế Bằng chứng công việc (Proof-of-Work), tính Bất biến (Immutability) và xác thực chuỗi.

📋 Tính năng chính

Mô phỏng Đào Coin (Mining):

Tạo giao dịch mới (Người gửi, Người nhận, Số tiền).

Thực hiện Proof-of-Work để tìm nonce hợp lệ.

Thêm khối mới vào chuỗi.

Sổ cái (Ledger Explorer):

Xem chi tiết từng khối trong chuỗi (Hash, Previous Hash, Timestamp, Data).

Giao diện trực quan dạng thẻ.

Kiểm tra & Tấn công (Simulation):

Công cụ Hacker: Cho phép sửa đổi dữ liệu của một khối đã tồn tại để mô phỏng tấn công.

Xác thực (Validator): Quét toàn bộ chuỗi để phát hiện sự thay đổi dữ liệu hoặc đứt gãy liên kết.

🛠️ Yêu cầu hệ thống

Python 3.8 trở lên.

🚀 Cài đặt và Chạy ứng dụng

Bước 1: Cài đặt thư viện

Mở terminal (hoặc Command Prompt) tại thư mục chứa dự án và chạy lệnh sau để cài đặt các thư viện cần thiết:

pip install -r requirements.txt


Bước 2: Chạy ứng dụng

Sử dụng lệnh streamlit run để khởi chạy ứng dụng:

streamlit run simple_blockchain.py


Sau khi chạy lệnh, trình duyệt web sẽ tự động mở ra tại địa chỉ http://localhost:8501.

📚 Cấu trúc dự án

simple_blockchain.py: Mã nguồn chính chứa logic Blockchain và giao diện Streamlit.

requirements.txt: Danh sách các thư viện Python cần thiết.

README.md: Tài liệu hướng dẫn này.

🧠 Nguyên lý hoạt động (Tóm tắt)

Block: Mỗi khối chứa một liên kết (previous_hash) đến khối trước đó, tạo thành một chuỗi.

Proof-of-Work: Để thêm khối, hệ thống phải giải một bài toán tìm mã băm bắt đầu bằng số lượng số 0 nhất định (độ khó).

Immutability: Nếu hacker sửa dữ liệu ở Khối A, mã Hash của Khối A thay đổi -> Khối B (trỏ đến A) sẽ bị sai liên kết -> Chuỗi bị vô hiệu hóa.