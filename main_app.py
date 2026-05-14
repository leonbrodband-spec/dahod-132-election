import streamlit as st
import pandas as pd
import os

# --- FILE SETUP ---
DATA_FILE = "booth_reports.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Booth_No", "Votes"])

def save_data(booth_no, votes):
    df = load_data()
    new_data = pd.DataFrame({"Booth_No": [booth_no], "Votes": [votes]})
    df = pd.concat([df, new_data]).drop_duplicates(subset=['Booth_No'], keep='last')
    df.to_csv(DATA_FILE, index=False)

# --- UI SETUP ---
st.set_page_config(page_title="Dahod 132 Election App", layout="wide")

# Sidebar - Mode Selection
mode = st.sidebar.selectbox("Select Mode", ["Karyakarta (Entry)", "Admin (Dashboard)"])

# --- MODE 1: KARYAKARTA (Sirf Entry) ---
if mode == "Karyakarta (Entry)":
    st.title("📍 Booth Data Reporting")
    st.info("Kripya apna booth number aur kul pade hue votes bharein.")
    
    with st.form("worker_form"):
        b_no = st.number_input("Booth Number (1-360)", min_value=1, max_value=360, step=1)
        v_count = st.number_input("Kul Pade Hue Votes (Total Polled)", min_value=0, step=1)
        submit = st.form_submit_button("Data Bhejein")
        
        if submit:
            save_data(b_no, v_count)
            st.success(f"✅ Booth {b_no} ka data update ho gaya hai!")
            st.balloons()

# --- MODE 2: ADMIN (Dashboard) ---
elif mode == "Admin (Dashboard)":
    st.title("🔐 Admin Login")
    pw = st.text_input("Password Dalein", type="password")
    
    if pw == "raja132": # Aapka Secret Password
        st.success("Welcome, Vashimraja Bhai!")
        df_live = load_data()
        
        # Admin Dashboard Code (Jo sirf aapko dikhega)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Booths", "360")
        c2.metric("Reported", len(df_live))
        total_voted = df_live["Votes"].sum() if not df_live.empty else 0
        c3.metric("Total Voting", f"{total_voted:,}")

        st.subheader("360 Booth Status Grid")
        cols = st.columns(12)
        for i in range(1, 361):
            reported = i in df_live["Booth_No"].values if not df_live.empty else False
            with cols[(i-1)%12]:
                if reported:
                    v = df_live[df_live["Booth_No"] == i]["Votes"].values[0]
                    st.success(f"B-{i}\n({v})")
                else:
                    st.write(f"⚪ B-{i}")
    elif pw != "":
        st.error("❌ Galat Password!")
