import hashlib
import time
import json
import streamlit as st

# ==========================================
# PHẦN 1: CORE LOGIC (CORE BLOCKCHAIN)
# ==========================================

class Block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Sắp xếp keys=True để đảm bảo tính nhất quán của chuỗi JSON
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        # Tạo một placeholder để hiển thị tiến trình đào trên UI
        status_text = st.empty() 
        
        start_time = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            # Cập nhật UI mỗi 100000 nonce để tránh lag giao diện
            if self.nonce % 100000 == 0:
                status_text.text(f"⛏️ Đang đào... Nonce: {self.nonce}")
        
        end_time = time.time()
        status_text.text(f"✅ Đã đào xong! Mất {end_time - start_time:.4f} giây.")
        return self.hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 3 # Độ khó mặc định (số lượng số 0 ở đầu hash)
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block (Khối nguyên thủy)", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 1. Kiểm tra Hash hiện tại: Dữ liệu có bị thay đổi không?
            if current_block.hash != current_block.calculate_hash():
                return False, f"Block {i} bị sai dữ liệu (Hash không khớp)!"

            # 2. Kiểm tra liên kết: Previous Hash có khớp với Hash của khối trước không?
            if current_block.previous_hash != previous_block.hash:
                return False, f"Liên kết giữa Block {i-1} và Block {i} bị đứt!"
        
        return True, "Chuỗi hợp lệ toàn vẹn."

# ==========================================
# PHẦN 2: GIAO DIỆN STREAMLIT (UI)
# ==========================================

# Cấu hình trang
st.set_page_config(page_title="Blockchain Demo", page_icon="🔗", layout="wide")

# Tiêu đề
st.title("🔗 Ứng dụng Mô phỏng Blockchain")
st.markdown("Hệ thống minh họa cơ chế hoạt động của Blockchain, Proof-of-Work và tính toàn vẹn dữ liệu.")

# 1. KHỞI TẠO SESSION STATE (LƯU TRỮ TRẠNG THÁI)
# Streamlit sẽ chạy lại code mỗi khi có tương tác, nên cần lưu blockchain vào bộ nhớ đệm
if 'blockchain' not in st.session_state:
    st.session_state['blockchain'] = Blockchain()

blockchain = st.session_state['blockchain']

# 2. SIDEBAR - CẤU HÌNH
with st.sidebar:
    st.header("⚙️ Cấu hình")
    
    # Điều chỉnh độ khó
    selected_difficulty = st.slider("Độ khó (Difficulty)", min_value=1, max_value=5, value=blockchain.difficulty)
    if selected_difficulty != blockchain.difficulty:
        blockchain.difficulty = selected_difficulty
        st.success(f"Đã cập nhật độ khó thành: {blockchain.difficulty}")

    st.divider()
    
    # Công cụ Hacker
    st.header("🛠️ Công cụ Hacker")
    st.info("Thử sửa đổi dữ liệu của một khối để xem điều gì xảy ra với chuỗi.")
    
    # Chọn block để hack (trừ Genesis block nếu chuỗi ngắn)
    max_idx = len(blockchain.chain) - 1
    block_index_to_hack = st.number_input("Chọn Block Index để hack", min_value=1, max_value=max_idx if max_idx > 0 else 1, step=1)
    hack_data = st.text_input("Dữ liệu giả mạo", "Hacked Data!")
    
    if st.button("Tấn công (Hack Block)"):
        if len(blockchain.chain) > 1 and block_index_to_hack < len(blockchain.chain):
            block = blockchain.chain[block_index_to_hack]
            block.data = hack_data
            st.toast(f"😈 Đã thay đổi dữ liệu Block {block_index_to_hack}!", icon="😈")
        else:
            st.warning("Chưa có Block nào hợp lệ để hack (trừ Genesis).")

# 3. GIAO DIỆN CHÍNH - CÁC TAB
tab1, tab2, tab3 = st.tabs(["➕ Thêm Giao Dịch (Đào)", "📜 Xem Chuỗi (Ledger)", "🛡️ Kiểm Tra (Validate)"])

# --- TAB 1: ĐÀO BLOCK MỚI ---
with tab1:
    st.subheader("Thêm Block mới vào chuỗi")
    
    col1, col2 = st.columns(2)
    with col1:
        sender = st.text_input("Người gửi", "Alice")
    with col2:
        receiver = st.text_input("Người nhận", "Bob")
    
    amount = st.number_input("Số lượng Coin", min_value=0.1, value=10.0)
    
    if st.button("🔨 Đào Block (Mine)", type="primary"):
        # Gom dữ liệu giao dịch
        transaction_data = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        
        # Tạo Block mới
        new_block = Block(
            index=len(blockchain.chain),
            timestamp=time.time(),
            data=transaction_data
        )
        
        # Thêm vào chuỗi (quá trình này sẽ thực hiện Proof-of-Work)
        with st.spinner('Đang thực hiện Proof-of-Work...'):
            blockchain.add_block(new_block)
        
        st.success("Đã thêm Block mới thành công!")
        st.balloons()

# --- TAB 2: XEM CHUỖI ---
with tab2:
    st.subheader("Sổ cái Blockchain hiện tại")
    
    if len(blockchain.chain) == 0:
        st.write("Chuỗi đang rỗng.")
    else:
        # Hiển thị từng Block dưới dạng Card có thể mở rộng
        for block in blockchain.chain:
            block_title = f"Block {block.index}"
            if block.index == 0:
                block_title += " (Genesis Block)"
            
            with st.expander(f"{block_title} - {block.hash[:10]}...", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Timestamp:** `{time.ctime(block.timestamp)}`")
                    st.markdown(f"**Nonce:** `{block.nonce}`")
                    st.markdown(f"**Previous Hash:**")
                    st.code(block.previous_hash)
                    st.markdown(f"**Current Hash:**")
                    st.code(block.hash)
                with c2:
                    st.markdown("**Data (Giao dịch):**")
                    st.json(block.data)

# --- TAB 3: KIỂM TRA (VALIDATE) ---
with tab3:
    st.subheader("Kiểm tra tính toàn vẹn hệ thống")
    
    st.markdown("""
    Chức năng này sẽ duyệt qua toàn bộ chuỗi khối để kiểm tra 2 điều kiện:
    1. **Hash Integrity:** Hash của khối có khớp với dữ liệu bên trong không?
    2. **Link Integrity:** Previous Hash của khối này có khớp với Hash của khối trước không?
    """)

    if st.button("🔍 Quét toàn bộ chuỗi"):
        is_valid, message = blockchain.is_chain_valid()
        
        if is_valid:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")
            st.warning("⚠️ Dữ liệu đã bị thay đổi! Hãy kiểm tra lại các Block trong Tab 'Xem Chuỗi'.")
