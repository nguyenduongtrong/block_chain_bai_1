import hashlib
import time
import json
import secrets
import streamlit as st

# ==========================================
# 1. CORE LOGIC (LOGIC CỐT LÕI)
# ==========================================

def hash_data(data_string, algo="SHA-256"):
    """Hàm băm hỗ trợ nhiều thuật toán khác nhau"""
    encoded = data_string.encode()
    if algo == "SHA-256":
        return hashlib.sha256(encoded).hexdigest()
    elif algo == "SHA3-256":
        try: return hashlib.sha3_256(encoded).hexdigest()
        except: return hashlib.sha256(encoded).hexdigest()
    elif algo == "BLAKE2b":
        return hashlib.blake2b(encoded).hexdigest()
    return hashlib.sha256(encoded).hexdigest()

class Block:
    def __init__(self, index, timestamp, data, previous_hash='', algo="SHA-256"):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.algo = algo
        self.nonce = 0
        self.validator = "System"
        self.execution_time = 0
        
        # Hash ban đầu sẽ được gán trong mine()
        self.hash = '' 

    def compute_hash(self):
        """
        Tính Hash dựa trên dữ liệu hiện tại của Block.
        FIX BUG: Loại bỏ Validator khỏi đầu vào Hash để đảm bảo Hash ổn định.
        """
        block_content = json.dumps({
            "index": self.index,
            "timestamp": int(self.timestamp), 
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "algo": self.algo,
            # Bỏ "validator" khỏi nội dung băm!
        }, sort_keys=True)
        return hash_data(block_content, self.algo)

    def mine(self, difficulty, consensus_type):
        """Mô phỏng quá trình đào/xác thực"""
        start = time.time()
        
        if consensus_type == "Proof-of-Work (PoW)":
            target = '0' * difficulty
            self.nonce = 0
            
            # Tính Hash tạm thời trong vòng lặp
            current_hash = self.compute_hash() 
            
            while current_hash[:difficulty] != target:
                self.nonce += 1
                current_hash = self.compute_hash() 
            
            # Gán Hash hợp lệ và Validator sau khi tìm thấy Nonce
            self.hash = current_hash 
            self.validator = "Miner (PoW)"
            
        elif consensus_type == "Proof-of-Authority (PoA)":
            time.sleep(0.05)
            self.nonce = secrets.randbelow(999999)
            
            # TÍNH HASH VÀ GÁN VÀO BLOCK SAU KHI ĐỒNG THUẬN XONG
            self.hash = self.compute_hash()
            self.validator = f"Validator-{secrets.randbelow(5)+1} (Authorized)"
            
        self.execution_time = time.time() - start
        return self.execution_time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 3
        self.create_genesis()

    def create_genesis(self):
        # Genesis Block: Gán timestamp là số nguyên để đảm bảo ổn định Hash
        genesis = Block(0, int(time.time()), "Genesis Block", "0", "SHA-256")
        genesis.mine(self.difficulty, "Proof-of-Work (PoW)")
        self.chain.append(genesis)

    def add_block(self, data, current_algo, current_consensus):
        last_block = self.chain[-1]
        # Gán timestamp là số nguyên (int)
        new_block = Block(len(self.chain), int(time.time()), data, last_block.hash, current_algo)
        new_block.mine(self.difficulty, current_consensus)
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        """Kiểm tra tính toàn vẹn của chuỗi"""
        # Kiểm tra Block 0 (Genesis)
        if self.chain[0].hash != self.chain[0].compute_hash():
             return False, "❌ LỖI TẠI BLOCK #0 (Genesis): Dữ liệu bị sửa đổi!"

        # Kiểm tra từ Block 1 trở đi
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]

            # 1. Kiểm tra Hash Integrity: Hash hiện tại có khớp với dữ liệu không?
            if current.hash != current.compute_hash():
                return False, f"❌ LỖI TẠI BLOCK #{i}: Dữ liệu bị sửa đổi! Hash tính lại không khớp."
            
            # 2. Kiểm tra Link Integrity: Previous Hash có trỏ đúng block trước không?
            if current.previous_hash != prev.hash:
                return False, f"❌ LỖI TẠI BLOCK #{i}: Liên kết bị hỏng! Previous Hash không khớp với Hash của Block #{i-1}."

        return True, "✅ Chuỗi Hợp Lệ (Blockchain Valid)"

# ==========================================
# 2. USER INTERFACE (GIAO DIỆN)
# ==========================================
st.set_page_config(page_title="Blockchain Demo", page_icon="⛓️", layout="wide")

st.title("⛓️ Blockchain Simulation: Validation & Tampering")

# Khởi tạo Session State (FIX TOAST BUG: Thêm cờ trạng thái)
if 'chain' not in st.session_state:
    st.session_state['chain'] = Blockchain()
if 'mine_status' not in st.session_state:
    st.session_state['mine_status'] = None

bc = st.session_state['chain']

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Cấu Hình Đào")
    algo_opt = st.selectbox("Thuật toán Băm", ["SHA-256", "SHA3-256", "BLAKE2b"])
    cons_opt = st.selectbox("Cơ chế Đồng thuận", ["Proof-of-Work (PoW)", "Proof-of-Authority (PoA)"])
    
    if cons_opt == "Proof-of-Work (PoW)":
        new_diff = st.slider("Độ khó (Difficulty)", 1, 5, 3)
        if bc.difficulty != new_diff:
            bc.difficulty = new_diff
            st.success(f"Đã cập nhật độ khó: {new_diff}")
            
    st.divider()
    if st.button("🗑️ Reset Chuỗi"):
        st.session_state['chain'] = Blockchain()
        st.session_state['mine_status'] = None # Reset cờ
        st.rerun()

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🔨 Đào Block (Mining)", "🛠️ Sửa & Kiểm Tra (Tamper & Validate)", "📜 Sổ cái (Ledger)"])

# TAB 1: ĐÀO BLOCK
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Tạo Block Mới")
        with st.form("mine_form"):
            tx_data = st.text_input("Dữ liệu giao dịch", value=f"Giao dịch mẫu {len(bc.chain)}")
            submitted = st.form_submit_button("Đào ngay 🚀", type="primary")
            
            if submitted:
                with st.spinner(f"Đang xử lý bằng {algo_opt}..."):
                    new_b = bc.add_block(tx_data, algo_opt, cons_opt)
                
                # FIX TOAST BUG: Lưu thông báo vào Session State
                st.session_state['mine_status'] = f"Block #{new_b.index} đã được đào thành công bằng {new_b.algo}!"
                
                st.rerun() # Bắt buộc phải rerun để cập nhật Ledger và hiển thị Toast

    with col2:
        st.info("Thông tin Blockchain hiện tại")
        st.markdown(f"**Tổng số Block:** `{len(bc.chain)}`")
        st.markdown(f"**Độ khó:** `{bc.difficulty}`")

# TAB 2: SỬA & KIỂM TRA (TÍNH NĂNG MỚI)
with tab2:
    st.header("Công cụ Kiểm thử Tính toàn vẹn")
    st.markdown("Thử thay đổi dữ liệu của một khối trong quá khứ và xem điều gì xảy ra với trạng thái Validation.")

    col_tamper, col_validate = st.columns(2)

    # Cột trái: Công cụ sửa dữ liệu (Tamper)
    with col_tamper:
        st.subheader("1. Sửa đổi dữ liệu (Tamper)")
        if len(bc.chain) > 0:
            block_idx = st.number_input("Chọn Block Index để sửa", min_value=0, max_value=len(bc.chain)-1, value=0)
            current_block = bc.chain[block_idx]
            
            st.text(f"Dữ liệu hiện tại của Block #{block_idx}:")
            st.code(current_block.data)
            
            new_data = st.text_input("Nhập dữ liệu giả mạo:", value="Hacked Data!")
            
            if st.button("⚠️ Ghi đè dữ liệu (Hack Block)"):
                current_block.data = new_data
                st.toast(f"Đã sửa dữ liệu Block #{block_idx}!", icon="😈")
                st.rerun()
        else:
            st.warning("Chưa có Block nào để sửa.")

    # Cột phải: Công cụ Validate
    with col_validate:
        st.subheader("2. Kiểm tra (Validate)")
        
        if st.button("🔍 Quét toàn bộ chuỗi"):
            is_valid, msg = bc.is_valid()
            if is_valid:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)
                
        # Hiển thị trạng thái realtime
        st.markdown("---")
        st.markdown("**Trạng thái Realtime:**")
        valid_realtime, msg_realtime = bc.is_valid()
        if valid_realtime:
            st.caption("🟢 Hệ thống đang ổn định")
        else:
            st.caption(f"🔴 {msg_realtime}")

# TAB 3: SỔ CÁI
with tab3:
    st.subheader("Chi tiết các khối")
    for b in reversed(bc.chain):
        # Highlight block bị lỗi nếu chuỗi không hợp lệ
        is_tampered = b.hash != b.compute_hash()
        
        with st.expander(f"Block #{b.index} | {b.algo} {'❌ (BỊ SỬA)' if is_tampered else ''}", expanded=(b.index == len(bc.chain)-1)):
            if is_tampered:
                st.error("⚠️ CẢNH BÁO: Hash của khối này không khớp với dữ liệu!")
            
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Hash đã lưu:** `{b.hash}`")
                st.write(f"**Hash thực tế:** `{b.compute_hash()}`")
            with c2:
                st.write(f"**Prev Hash:** `{b.previous_hash}`")
                st.write(f"**Nonce:** `{b.nonce}`")
            st.info(f"Data: {b.data}")

# --- GLOBAL TOAST CHECK (FIX TOAST BUG) ---
# Kiểm tra cờ và hiển thị toast sau khi script đã chạy xong phần UI
if st.session_state['mine_status']:
    st.toast(st.session_state['mine_status'], icon="🎉")
    st.session_state['mine_status'] = None # Xóa cờ sau khi hiển thị
