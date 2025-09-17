import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud

# Configure page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide"
)

# Cache data loading
# Cache data loading
@st.cache_data
def load_data(sample_size=50000):
    """Load and clean the CORD-19 metadata in a memory-efficient way"""
    
    use_cols = ['title', 'publish_time', 'journal', 'authors']

    try:
        # Try to load the full dataset (local machine only)
        df = pd.read_csv('metadata.csv', usecols=use_cols, low_memory=True)
    except FileNotFoundError:
        # Fallback to the smaller sample dataset (on Streamlit Cloud)
        df = pd.read_csv('metadata_sample.csv', usecols=use_cols, low_memory=True)

    # Drop missing critical values
    df = df.dropna(subset=['title', 'publish_time'])

    # Convert dates
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df = df.dropna(subset=['publish_time'])
    df['year'] = df['publish_time'].dt.year.astype('int16')

    # Filter for COVID-19 era
    df = df[(df['year'] >= 2019) & (df['year'] <= 2023)]

    # Add feature: title word count
    df['title_word_count'] = df['title'].str.split().str.len().astype('int16')

    # Convert journal to category (saves memory)
    df['journal'] = df['journal'].astype('category')

    # Optional: sample down the dataset for faster use
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=42)

    return df



# Load data
df = load_data()

# App header
st.title("🦠 CORD-19 Research Data Explorer")
st.markdown("### Exploring COVID-19 Research Papers")
st.markdown(f"**Dataset contains:** {len(df):,} research papers")

# Sidebar controls
st.sidebar.header("Filter Options")
year_range = st.sidebar.slider(
    "Select Year Range", 
    int(df['year'].min()), 
    int(df['year'].max()), 
    (int(df['year'].min()), int(df['year'].max()))
)

# Filter data based on selection
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Publications by Year")
    yearly_counts = filtered_df['year'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(yearly_counts.index, yearly_counts.values, color='steelblue')
    ax.set_title('COVID-19 Research Publications by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    st.pyplot(fig)
    
    # Display statistics
    st.metric("Total Papers in Range", len(filtered_df))
    st.metric("Peak Year", yearly_counts.idxmax())
    st.metric("Peak Publications", yearly_counts.max())

with col2:
    st.subheader("📰 Top Publishing Journals")
    top_journals = filtered_df['journal'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_journals.plot(kind='barh', ax=ax, color='coral')
    ax.set_title('Top 10 Journals Publishing COVID-19 Research')
    ax.set_xlabel('Number of Publications')
    st.pyplot(fig)

# Word analysis section
st.subheader("🔤 Title Word Analysis")

# Word frequency
def get_word_frequency(titles):
    all_words = []
    for title in titles.dropna():
        # Remove common stop words and extract meaningful words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'they', 'been', 'have', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'can', 'may', 'use', 'her', 'him', 'his', 'she', 'was', 'one', 'our', 'had', 'but', 'not', 'what', 'all', 'any', 'your', 'how', 'did', 'its'}
        words = [w for w in words if w not in stop_words]
        all_words.extend(words)
    return Counter(all_words)

word_freq = get_word_frequency(filtered_df['title'])
common_words = dict(word_freq.most_common(20))

col3, col4 = st.columns(2)

with col3:
    st.write("**Most Common Words in Titles**")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(list(common_words.keys())[:15], list(common_words.values())[:15], color='lightgreen')
    ax.set_title('Most Common Words in Paper Titles')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    st.write("**Word Cloud**")
    if len(common_words) > 0:
        wordcloud = WordCloud(width=400, height=300, background_color='white').generate_from_frequencies(common_words)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

# Data sample section
st.subheader("📋 Sample Data")
st.write(f"Showing 10 random papers from {year_range[0]}-{year_range[1]}:")
sample_cols = ['title', 'authors', 'journal', 'year', 'title_word_count']
available_cols = [col for col in sample_cols if col in filtered_df.columns]
st.dataframe(filtered_df[available_cols].sample(min(10, len(filtered_df))))

# Summary statistics
st.subheader("📈 Summary Statistics")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Total Papers", f"{len(filtered_df):,}")
with col6:
    st.metric("Unique Journals", filtered_df['journal'].nunique())
with col7:
    avg_words = filtered_df['title_word_count'].mean()
    st.metric("Avg Title Length", f"{avg_words:.1f} words")
with col8:
    date_range = filtered_df['year'].max() - filtered_df['year'].min() + 1
    st.metric("Years Covered", f"{date_range} years")

# Footer
st.markdown("---")
st.markdown("**Data Source:** CORD-19 Dataset from Kaggle")
st.markdown("**Built with:** Streamlit, Pandas, Matplotlib")