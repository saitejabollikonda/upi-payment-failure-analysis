import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

st.set_page_config(page_title="UPI Failure Intelligence", layout="wide")
st.title("🔴 UPI Payment Failure Intelligence System")
st.markdown("**Identifying and quantifying payment failure patterns across bank corridors**")

conn = sqlite3.connect('/Users/saitejabollikonda/Downloads/upi_project.db')
df = pd.read_sql_query("SELECT * FROM upi_transactions", conn)
conn.close()

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Transactions", f"{len(df):,}")
with col2:
    failure_rate = (df['txn_status'] == 'failed').mean() * 100
    st.metric("Platform Failure Rate", f"{failure_rate:.2f}%")
with col3:
    damage = df[df['txn_status'] == 'failed']['amount'].sum() / 100000
    st.metric("Total Revenue Loss", f"₹{damage:.2f}L")
with col4:
    worst_corridor_rate = df.groupby('bank_corridor')['txn_status'].apply(lambda x: (x == 'failed').mean() * 100).max()
    st.metric("Worst Corridor Rate", f"{worst_corridor_rate:.2f}%")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Bank Corridors", "Time Windows", "Merchants", "Failure Reasons"])

# TAB 1 - BANK CORRIDORS (DETAILED)
with tab1:
    st.subheader("💰 Top 15 Corridors by Revenue Loss")
    
    corridor_analysis = df.groupby('bank_corridor').agg(
        total_txns=('txn_id', 'count'),
        failed_txns=('txn_status', lambda x: (x == 'failed').sum()),
        failure_rate_pct=('txn_status', lambda x: round((x == 'failed').mean() * 100, 2)),
        revenue_loss_lakhs=('amount', lambda x: round(x[df['txn_status'] == 'failed'].sum() / 100000, 2))
    ).sort_values('revenue_loss_lakhs', ascending=False).head(15)
    
    # Display table
    st.dataframe(corridor_analysis, use_container_width=True, height=400)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Failure Rate by Corridor (Top 10)")
        fig, ax = plt.subplots(figsize=(10, 6))
        top_10 = corridor_analysis.head(10).sort_values('failure_rate_pct')
        ax.barh(top_10.index, top_10['failure_rate_pct'], color='#E74C3C')
        ax.axvline(x=failure_rate, color='black', linestyle='--', linewidth=2, label=f'Avg: {failure_rate:.2f}%')
        ax.set_xlabel('Failure Rate %')
        ax.set_title('Corridors Above Platform Average')
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Revenue Loss by Corridor (Top 10)")
        fig, ax = plt.subplots(figsize=(10, 6))
        top_loss = corridor_analysis.head(10).sort_values('revenue_loss_lakhs')
        ax.barh(top_loss.index, top_loss['revenue_loss_lakhs'], color='#C0392B')
        ax.set_xlabel('Loss (₹ Lakhs)')
        ax.set_title('Highest Revenue Impact')
        st.pyplot(fig)
    
    # Drill down
    st.subheader("🔍 Drill Down: Analyze Specific Corridor")
    selected_corridor = st.selectbox("Select a corridor:", df['bank_corridor'].unique())
    
    corridor_df = df[df['bank_corridor'] == selected_corridor]
    st.metric(label="Failure Rate", value=f"{(corridor_df['txn_status'] == 'failed').mean() * 100:.2f}%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Transactions", len(corridor_df))
    with col2:
        st.metric("Failed Transactions", (corridor_df['txn_status'] == 'failed').sum())
    
    st.write("**Failure Reasons Breakdown:**")
    failure_reasons = corridor_df[corridor_df['txn_status'] == 'failed']['failure_reason'].value_counts()
    st.bar_chart(failure_reasons)

# TAB 2 - TIME WINDOWS
with tab2:
    st.subheader("⏰ Failure Patterns by Time Window")
    
    time_analysis = df.groupby('time_window').agg(
        total_txns=('txn_id', 'count'),
        failed_txns=('txn_status', lambda x: (x == 'failed').sum()),
        failure_rate_pct=('txn_status', lambda x: round((x == 'failed').mean() * 100, 2)),
        revenue_loss_lakhs=('amount', lambda x: round(x[df['txn_status'] == 'failed'].sum() / 100000, 2))
    ).sort_values('revenue_loss_lakhs', ascending=False)
    
    st.dataframe(time_analysis, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Failure Rate by Time")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(time_analysis.index, time_analysis['failure_rate_pct'], color='#3498DB')
        ax.axhline(y=failure_rate, color='black', linestyle='--', label=f'Avg: {failure_rate:.2f}%')
        ax.set_ylabel('Failure Rate %')
        ax.set_title('Which Hours Are Worst?')
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Revenue Loss by Time")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(time_analysis.index, time_analysis['revenue_loss_lakhs'], color='#E67E22')
        ax.set_ylabel('Loss (₹ Lakhs)')
        ax.set_title('When Do We Lose Most Money?')
        plt.xticks(rotation=45)
        st.pyplot(fig)

# TAB 3 - MERCHANTS
with tab3:
    st.subheader("🛍️ Failure Analysis by Merchant Category")
    
    merchant_analysis = df.groupby('merchant_category').agg(
        total_txns=('txn_id', 'count'),
        failed_txns=('txn_status', lambda x: (x == 'failed').sum()),
        failure_rate_pct=('txn_status', lambda x: round((x == 'failed').mean() * 100, 2)),
        revenue_loss_lakhs=('amount', lambda x: round(x[df['txn_status'] == 'failed'].sum() / 100000, 2))
    ).sort_values('revenue_loss_lakhs', ascending=False)
    
    st.dataframe(merchant_analysis, use_container_width=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(merchant_analysis.index, merchant_analysis['revenue_loss_lakhs'], color='#2ECC71')
    ax.set_ylabel('Loss (₹ Lakhs)')
    ax.set_title('Which Merchant Categories Lose Most?')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# TAB 4 - FAILURE REASONS
with tab4:
    st.subheader("❌ Failure Reason Analysis")
    
    failure_analysis = df[df['txn_status'] == 'failed'].groupby('failure_reason').agg(
        count=('txn_id', 'count'),
        revenue_loss_lakhs=('amount', lambda x: round(x.sum() / 100000, 2))
    ).sort_values('revenue_loss_lakhs', ascending=False)
    
    st.dataframe(failure_analysis, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Failure Count by Reason")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(failure_analysis.index, failure_analysis['count'], color='#9B59B6')
        ax.set_xlabel('Count')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Revenue Loss by Reason")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(failure_analysis.index, failure_analysis['revenue_loss_lakhs'], color='#E74C3C')
        ax.set_xlabel('Loss (₹ Lakhs)')
        st.pyplot(fig)

st.divider()
st.markdown("""
### 📊 Key Insights
1. **Yes Bank → HDFC** corridor has 24.5% failure rate — **2x platform average** — causing ₹10.65L damage
2. **Midnight-6AM** window accounts for ₹147L damage — **33% of total losses** — suggests reduced bank server capacity
3. **Food Delivery** category suffers highest losses despite smaller transaction sizes — batch transactions or negotiate minimum thresholds
""")