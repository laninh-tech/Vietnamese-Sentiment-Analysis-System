"""
Insightify Analytics - Multi-Channel Sentiment Analysis & E-Commerce Order Extraction

A real-time Streamlit dashboard for analyzing Vietnamese social media sentiment
and automatically extracting customer order information.

Key Features:
- PhoBERT-based sentiment classification (>85% F1-score)
- Regex-based order extraction (phone, address, product hints)
- URL web scraping with Selenium headless browser
- Interactive visualizations with Plotly
- Excel export for extracted leads

Author: laninh-tech
"""

import torch
import streamlit as st
import pandas as pd
import plotly.express as px
from sentiment_model import SentimentModel
from scraper import scrape_url
from order_extractor import order_extractor
import io

# Page config
st.set_page_config(page_title="Sentiment & Order Tracker", page_icon="📈", layout="wide")

# Custom CSS for modern SaaS aesthetic
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Main Background & Fonts */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global text colors for light theme */
    div, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #1E293B;
    }

    /* Main Container Padding Reset */
    .main .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1600px;
    }

    /* Modern SaaS Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    /* Wrap metrics in a beautiful glass card */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        transition: all 0.2s ease-in-out;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #CBD5E1;
    }
    
    /* Tabs Redesign */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0px;
        padding: 10px 15px;
        border: none;
        color: #64748B;
        font-weight: 600;
        font-size: 1.05rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
    }
    
    /* Sleek DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] hr {
        border-color: #E2E8F0;
    }
    
    /* Custom Headers */
    .header-title {
        color: #0F172A;
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .header-subtitle {
        color: #64748B;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 4px;
        margin-bottom: 24px;
    }
    .section-title {
        color: #1E293B;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Primary Button Redesign */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 1px #2563eb;
    }
    
    /* Make Sidebar Text Visible */
    div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] p {
        color: #1E293B !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# App Header
col_logo, col_title = st.columns([1, 15])
with col_title:
    st.markdown("<h1 class='header-title'>Insightify Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='header-subtitle'>Real-time Social Sentiment & Smart E-Commerce Order Extraction</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Session State
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=[
        'Text', 'Source', 'Sentiment', 'Confidence', 'Time', 
        'Is_Order', 'Phone', 'Address', 'Product'
    ])
if 'model' not in st.session_state:
    st.session_state['model'] = SentimentModel()

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='section-title'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
    st.markdown("Select data pipeline mode below:")
    input_method = st.radio("Pipeline Mode", ["URL Web Scraper", "Manual Data Entry"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

def process_data(texts, sources, times):
    """
    Process input texts through sentiment analysis and order extraction.
    
    For each text: analyzes sentiment using PhoBERT and extracts order information.
    Appends results to session state dataframe for display.
    
    Args:
        texts (list): List of Vietnamese texts to analyze
        sources (list): List of source identifiers (URLs, platforms)
        times (list): List of timestamps for each text
    """
    results = []
    with st.spinner('Analyzing sentiment and extracting orders...'):
        for i, text in enumerate(texts):
            # 1. Sentiment Inference
            pred = st.session_state['model'].predict(text)
            
            # 2. Order Extraction
            order_info = order_extractor.extract(text)
            
            results.append({
                'Text': text,
                'Source': sources[i] if type(sources) == list else sources,
                'Sentiment': pred['label'],
                'Confidence': pred['score'],
                'Time': times[i] if type(times) == list else times,
                'Is_Order': 'Yes' if order_info['is_order'] else 'No',
                'Phone': order_info['phone'],
                'Address': order_info['address_hint'],
                'Product': order_info['product_hint']
            })
    
    new_df = pd.DataFrame(results)
    st.session_state['data'] = pd.concat([new_df, st.session_state['data']], ignore_index=True)

if input_method == "Manual Data Entry":
    st.sidebar.markdown("<h4 style='color:#334155; margin-bottom: 8px;'>Batch Input Text</h4>", unsafe_allow_html=True)
    manual_text = st.sidebar.text_area("Paste customer comments or reviews (one per line is ideal):", height=200)
    if st.sidebar.button("Run Analysis pipeline"):
        if manual_text.strip():
            process_data([manual_text], ["Manual Input"], ["Just now"])
            st.sidebar.success("✅ Analysis completed successfully!")
        else:
            st.sidebar.warning("⚠️ Please enter some text to analyze.")

elif input_method == "URL Web Scraper":
    st.sidebar.markdown("<h4 style='color:#334155; margin-bottom: 8px;'>Target Web URL</h4>", unsafe_allow_html=True)
    target_url = st.sidebar.text_input("Enter URL (Facebook Post, News article):", placeholder="https://www.facebook.com/...")
    
    st.sidebar.markdown("<h4 style='color:#334155; margin-bottom: 8px;'>Facebook Cookie (Optional)</h4>", unsafe_allow_html=True)
    fb_cookie = st.sidebar.text_input("Paste Cookie to bypass Facebook Login:", type="password", placeholder="c_user=...; xs=...")
    
    if st.sidebar.button("Extract & Analyze"):
        if target_url.strip():
            with st.spinner("Connecting to source (Live Scraping)..."):
                scrape_res = scrape_url(target_url, cookies_str=fb_cookie)
                
                if scrape_res['success'] and scrape_res['data']:
                    st.sidebar.success(f"✅ {scrape_res['message']}")
                    texts = [item['text'] for item in scrape_res['data']]
                    sources = [item['source'] for item in scrape_res['data']]
                    times = [item['time'] for item in scrape_res['data']]
                    process_data(texts, sources, times)
                elif not scrape_res['success']:
                    st.sidebar.error(f"❌ " + scrape_res['message'])
                else:
                    st.sidebar.warning("⚠️ No valid data patterns found.")
        else:
             st.sidebar.warning("⚠️ Please provide a URL.")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Dashboard Data"):
    st.session_state['data'] = pd.DataFrame(columns=[
        'Text', 'Source', 'Sentiment', 'Confidence', 'Time', 
        'Is_Order', 'Phone', 'Address', 'Product'
    ])

# Main Content Area
df = st.session_state['data']

if not df.empty:
    
    # Create Tabs for Separation of Concerns
    tab1, tab2 = st.tabs(["📊 Sentiment Dashboard", "🛒 E-Commerce Orders"])
    
    # ---------------------------
    # TAB 1: SENTIMENT DASHBOARD
    # ---------------------------
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        # Use Streamlit's native st.metric to take advantage of our CSS overrides
        col1, col2, col3, col4 = st.columns(4)
        total_comments = len(df)
        positive_count = len(df[df['Sentiment'] == 'Positive'])
        negative_count = len(df[df['Sentiment'] == 'Negative'])
        neutral_count = len(df[df['Sentiment'] == 'Neutral'])
        
        with col1:
            st.metric(label="Total Analyzed Mentions", value=total_comments)
        with col2:
            st.metric(label="Positive Sentiment", value=positive_count, delta=f"{(positive_count/total_comments)*100:.1f}%" if total_comments > 0 else "0%", delta_color="normal")
        with col3:
            st.metric(label="Negative Sentiment", value=negative_count, delta=f"{(negative_count/total_comments)*100:.1f}%" if total_comments > 0 else "0%", delta_color="inverse")
        with col4:
            st.metric(label="Neutral Sentiment", value=neutral_count, delta=f"{(neutral_count/total_comments)*100:.1f}%" if total_comments > 0 else "0%", delta_color="off")
        
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Visualizations Container
        with st.container():
            col_v1, col_v2 = st.columns([1, 1.2])
            
            with col_v1:
                st.markdown("<div class='section-title'>📊 Sentiment Distribution</div>", unsafe_allow_html=True)
                if len(df) > 0:
                    sentiment_counts = df['Sentiment'].value_counts().reset_index()
                    sentiment_counts.columns = ['Sentiment', 'Count']
                    
                    color_discrete_map = {'Positive': '#10B981', 'Negative': '#EF4444', 'Neutral': '#94A3B8'}
                    fig1 = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                                  color='Sentiment', color_discrete_map=color_discrete_map,
                                  hole=0.6)
                    fig1.update_layout(
                        margin=dict(t=10, b=10, l=10, r=10), 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                    )
                    fig1.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color='#ffffff', width=2)))
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("Waiting for data stream to calculate distribution.")

            with col_v2:
                st.markdown("<div class='section-title'>📈 Trends by Data Source</div>", unsafe_allow_html=True)
                if len(df) > 0:
                    source_sentiment = df.groupby(['Source', 'Sentiment']).size().reset_index(name='Count')
                    color_discrete_map = {'Positive': '#10B981', 'Negative': '#EF4444', 'Neutral': '#94A3B8'}
                    fig2 = px.bar(source_sentiment, x='Source', y='Count', color='Sentiment', barmode='group',
                                  color_discrete_map=color_discrete_map)
                    fig2.update_layout(
                        margin=dict(t=10, b=20, l=10, r=10), 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis_title=None,
                        yaxis_title="Mention Count",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                    )
                    # hide grid defaults
                    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                     st.info("Waiting for data stream to chart source trends.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Real-time Feed
        st.markdown("<div class='section-title'>💬 Latest Analyzed Insights Feed</div>", unsafe_allow_html=True)
        
        # Format confidence as percentage
        display_df = df[['Text', 'Source', 'Sentiment', 'Confidence', 'Time']].copy()
        display_df['Confidence'] = display_df['Confidence'].apply(lambda x: f"{x:.2%}")
        
        def highlight_sentiment(val):
            color = '#10B981' if val == 'Positive' else '#EF4444' if val == 'Negative' else '#94A3B8'
            return f'color: {color}; font-weight: 600;'
        
        st.dataframe(display_df.style.map(highlight_sentiment, subset=['Sentiment']), use_container_width=True, hide_index=True, height=250)

    # ---------------------------
    # TAB 2: E-COMMERCE ORDERS
    # ---------------------------
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📦 Automated Order Extraction Feed</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b; margin-bottom:24px;'>The regex NLP engine automatically scans unstructured text for phone numbers, Vietnam addresses, and purchase intents to extract potential leads and orders.</p>", unsafe_allow_html=True)
        
        # Filter for rows that are identified as orders
        orders_df = df[df['Is_Order'] == 'Yes'].copy()
        orders_display_df = orders_df[['Phone', 'Product', 'Address', 'Sentiment', 'Text']]
        
        if not orders_display_df.empty:
            st.dataframe(orders_display_df, use_container_width=True, hide_index=True, height=300)
            
            # Excel Export Setup
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                orders_display_df.to_excel(writer, index=False, sheet_name='Đơn Hàng')
            excel_data = output.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_export_1, col_export_2 = st.columns([1, 3])
            with col_export_1:
                st.download_button(
                    label="📥 Export Leads to CRM (.xlsx)",
                    data=excel_data,
                    file_name="extracted_orders_list.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        else:
            st.info("No actionable orders detected in the analyzed stream yet. Waiting for keywords (buy, ship, phone numbers) to trigger NLP extraction.")

else:
    # Empty State Landing Page
    st.markdown("""
    <div style='background-color: #FFFFFF; padding: 40px; border-radius: 16px; border: 1px dashed #CBD5E1; text-align: center; margin-top: 40px;'>
        <h2 style='color: #0F172A; font-family:"Plus Jakarta Sans", sans-serif; font-size: 1.8rem;'>Welcome to Insightify Analytics Workspace 👋</h2>
        <p style='color: #64748B; font-size: 1.1rem; max-width: 600px; margin: 10px auto 30px auto;'>
            Connect your data sources using the Control Panel on the left to activate the Dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div style='background: #F8FAFC; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;'>
            <h4 style='color: #2563EB; margin-bottom: 8px;'>1. NLP Sentiment 🧠</h4>
            <p style='color: #475569; font-size: 0.95rem; margin:0;'>Utilizes Pre-trained PhoBERT to classify text context at a >85% baseline F1 accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div style='background: #F8FAFC; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;'>
            <h4 style='color: #10B981; margin-bottom: 8px;'>2. Lead Extraction 🛒</h4>
            <p style='color: #475569; font-size: 0.95rem; margin:0;'>Automatically extracts raw unformatted texts into actionable E-commerce variables (Phone, VN Address).</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div style='background: #F8FAFC; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;'>
            <h4 style='color: #F59E0B; margin-bottom: 8px;'>3. CRM Export 📥</h4>
            <p style='color: #475569; font-size: 0.95rem; margin:0;'>Zero copy-pasting. 1-click export generated leads into cleanly formatted Excel sheets for shipping systems.</p>
        </div>
        """, unsafe_allow_html=True)
