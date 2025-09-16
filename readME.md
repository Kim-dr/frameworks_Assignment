# CORD-19 Data Analysis Project

## Overview
This project analyzes the CORD-19 research dataset to explore trends in COVID-19 research publications. It includes data exploration, visualization, and an interactive Streamlit web application.

## Dataset
- **Source**: CORD-19 Research Challenge from Kaggle
- **File used**: metadata.csv
- **Content**: Metadata for COVID-19 research papers including titles, authors, journals, and publication dates

## Features
- **Data Exploration**: Basic statistics and data quality assessment
- **Visualizations**: 
  - Publications by year
  - Top publishing journals
  - Word frequency analysis
  - Word cloud generation
- **Interactive Web App**: Streamlit dashboard with filtering capabilities

## Installation

1. Clone this repository:
```bash
git clone [https://github.com/Kim-dr/frameworks_Assignment.git]
cd Frameworks_Assignment
```

2. Install required packages:
```bash
pip install pandas matplotlib seaborn streamlit wordcloud jupyter
```

3. Download the metadata.csv file from Kaggle and place it in the project directory

## Usage

### Run Jupyter Notebook Analysis
```bash
jupyter notebook CORD19_Analysis.ipynb
```

### Run Streamlit App
```bash
streamlit run streamlit_app.py
```

## Project Structure
```
Frameworks_Assignment/
│
├── CORD19_Analysis.ipynb    # Jupyter notebook with analysis
├── streamlit_app.py         # Main Streamlit application
├── metadata.csv             # Dataset (download separately)
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Key Findings
- Peak publication year for COVID-19 research
- Most active journals in COVID-19 research
- Common themes in research paper titles
- Trends in publication volume over time

## Technologies Used
- **Python 3.13.5**
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **Streamlit**: Web application framework
- **WordCloud**: Text visualization
- **Jupyter**: Interactive development

## Learning Outcomes
- Real-world dataset handling and cleaning
- Data visualization best practices
- Web application development with Streamlit
- Basic text analysis and word frequency counting

## Future Improvements
- Abstract text analysis
- Author collaboration networks
- Advanced NLP techniques
- More sophisticated filtering options
- Export functionality for visualizations

## Author
[Kimberly Kagasi]

## License

This project is for educational purposes.
