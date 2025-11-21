Blockchain Demo - Hybrid, Validation & Tampering

Ứng dụng mô phỏng Blockchain trực quan, tập trung vào việc minh họa tính bất biến (Immutability) và khả năng tùy biến thuật toán trong công nghệ chuỗi khối hiện đại.

🌟 Tính năng Chính (Key Features)

Đa Thuật Toán Băm (Hashing Algorithms):

Hỗ trợ SHA-256 (Bitcoin Standard).

Hỗ trợ SHA3-256 (Ethereum Standard).

Hỗ trợ BLAKE2b (Tốc độ cao).

Đặc điểm: Cho phép người dùng chọn thuật toán cho từng Block, minh họa kiến trúc linh hoạt (Hybrid Chain).

Đa Cơ chế Đồng thuận (Consensus Mechanisms):

Proof-of-Work (PoW): Mô phỏng quá trình "đào" tốn công sức để giải bài toán nonce.

Proof-of-Authority (PoA): Mô phỏng xác thực nhanh chóng dựa trên danh tính (Validator) và không tốn năng lượng.

Công cụ Kiểm thử Tính toàn vẹn (Validation & Tampering):

Validate (Kiểm tra): Tự động quét toàn bộ chuỗi để xác minh tính toàn vẹn (Hash Integrity & Link Integrity).

Tamper (Sửa dữ liệu): Cho phép người dùng chọn bất kỳ Block nào trong quá khứ và thay đổi dữ liệu của nó để mô phỏng cuộc tấn công.

🚀 Cách chạy ứng dụng

Cài đặt thư viện:

Đảm bảo bạn đã cài đặt các thư viện cần thiết (chỉ cần Streamlit).
<!-- end list -->

pip install -r requirements.txt


Khởi chạy ứng dụng:

streamlit run simple_blockchain.py


💡 Hướng dẫn Kiểm tra Tính Bất biến (Immutability Test)

Sử dụng Tab "🛠️ Sửa & Kiểm Tra (Tamper & Validate)" để chứng minh nguyên lý bất biến của Blockchain:

Đào Block: Đào khoảng 3-4 Block ở Tab "🔨 Đào Block".

Sửa Block:

Chuyển sang Tab "Sửa & Kiểm Tra".

Ở mục "1. Sửa đổi dữ liệu (Tamper)", chọn Block #1 (hoặc Block bất kỳ).

Nhập dữ liệu giả mạo (ví dụ: "Hacked 1000 BTC").

Bấm "⚠️ Ghi đè dữ liệu (Hack Block)".

Kiểm tra:

Hệ thống Realtime sẽ ngay lập tức báo lỗi (🔴).

Bấm "🔍 Quét toàn bộ chuỗi" để nhận thông báo chi tiết: lỗi xảy ra tại Block đã sửa (Hash Integrity fail) và Block liền kề (Link Integrity fail) do Hash của Block trước đã thay đổi.
