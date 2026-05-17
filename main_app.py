import streamlit as st
import pandas as pd
import os

# --- FILE SETUP ---
DATA_FILE = "booth_reports.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=["Booth_No", "Votes"])
    return pd.DataFrame(columns=["Booth_No", "Votes"])

def save_data(booth_no, votes):
    df = load_data()
    new_data = pd.DataFrame({"Booth_No": [booth_no], "Votes": [votes]})
    df = pd.concat([df, new_data]).drop_duplicates(subset=['Booth_No'], keep='last')
    df.to_csv(DATA_FILE, index=False)

def reset_all_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.cache_data.clear()

# --- UI SETUP ---
st.set_page_config(page_title="AG ENTERPRISE - Dahod 132", layout="wide")

# Sidebar
mode = st.sidebar.selectbox("Select Mode / मोड चुनें", ["Karyakarta (Entry)", "Admin (Dashboard)"])
st.sidebar.markdown("---")
st.sidebar.caption("Powered by: **AG ENTERPRISE**")

# --- MODE 1: KARYAKARTA ENTRY FORM ---
if mode == "Karyakarta (Entry)":
    st.title("📍 AG ENTERPRISE - Ground Reporting System")
    st.markdown("### Dahod 132 | कार्यकर्ता भाई, अपने बूथ का डेटा यहाँ भरें:")
    
    with st.form("worker_entry_form", clear_on_submit=True):
        b_no = st.number_input("Booth Number (1 se 360)", min_value=1, max_value=360, step=1)
        v_count = st.number_input("Matdar Yadi Ke Hisab Se Kul Votes (Total Polled)", min_value=0, step=1)
        submit = st.form_submit_button("Data Bhejein / Submit")
        
        if submit:
            save_data(b_no, v_count)
            st.success(f"✅ Booth No. {b_no} ka data AG ENTERPRISE Control Room ko bhej diya gaya hai!")
            st.balloons()

# --- MODE 2: ADMIN DASHBOARD ---
elif mode == "Admin (Dashboard)":
    st.title("🔐 AG ENTERPRISE - Admin Verification")
    pw = st.text_input("Enter Secret Password", type="password")
    
    if pw == "raja132":
        st.success("Welcome, Vashimraja Bhai! AG ENTERPRISE Master Control Room Active.")
        df_live = load_data()
        
        # RESET BUTTON (Sirf Admin ko Sidebar mein dikhega)
        st.sidebar.subheader("Danger Zone")
        if st.sidebar.button("⚠️ CLEAR ALL DATA (RESET)"):
            reset_all_data()
            st.sidebar.error("Sare booths ka data delete ho gaya!")
            st.rerun()
            
        # Top Metrics
        st.markdown("## 📊 Dahod 132 Live Monitor")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Booths", "360")
        c2.metric("Reported Booths", len(df_live))
        total_voted = df_live["Votes"].sum() if not df_live.empty else 0
        c3.metric("Total Polled Votes", f"{total_voted:,}")
        
        st.markdown("---")
        
        # Live 360 Grid
        st.subheader("📌 360 Booth Status Grid")
        cols = st.columns(15)
        
        for i in range(1, 361):
            reported = i in df_live["Booth_No"].values if not df_live.empty else False
            with cols[(i-1)%15]:
                if reported:
                    vote_val = df_live[df_live["Booth_No"] == i]["Votes"].values[0]
                    st.success(f"B-{i}\n({vote_val})")
                else:
                    st.write(f"⚪ B-{i}")
                    
        # Table view
        st.markdown("---")
        with st.expander("Sari Reports Ek Saath Dekhein (Table View)"):
            if not df_live.empty:
                st.dataframe(df_live.sort_values("Booth_No"), use_container_width=True)
            else:
                st.write("Abhi koi data nahi mila hai.")
                
    elif pw != "":
        st.error("❌ Galat Password! Aapko dashboard dekhne ki anumati nahi hai.")
