# Activity 1 - Data Mining
# Universidad de la Costa
# Camilo Andres Visbal Beltran

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

st.set_page_config(
    page_title="University Dashboard",
    page_icon="",
    layout="wide"
)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/camilovisbal/dashboard-universitario/main/university_student_data.csv"
    return pd.read_csv(url)

df = load_data()

st.title("University Analytics Dashboard")
st.markdown("""
**Universidad de la Costa | Data Mining | Activity 1**  
Camilo Andres Visbal Beltran | Professor: Jose Escorcia-Gutierrez, Ph.D.
""")
st.markdown("---")

st.sidebar.header("Filters")

available_years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Year(s):",
    options=available_years,
    default=available_years
)

available_terms = df['Term'].unique().tolist()
selected_terms = st.sidebar.multiselect(
    "Select Term(s):",
    options=available_terms,
    default=available_terms
)

# apply filters
df_filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Term'].isin(selected_terms))
]

if df_filtered.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop()

# KPI CARDS
st.subheader("Key Indicators")
col1, col2, col3, col4 = st.columns(4)

total_applicants  = int(df_filtered['Applications'].sum())
total_enrolled    = int(df_filtered['Enrolled'].sum())
avg_retention     = round(df_filtered['Retention Rate (%)'].mean(), 1)
avg_satisfaction  = round(df_filtered['Student Satisfaction (%)'].mean(), 1)

col1.metric("Total Applicants",      f"{total_applicants:,}")
col2.metric("Total Enrolled",        f"{total_enrolled:,}")
col3.metric("Avg Retention Rate",    f"{avg_retention}%")
col4.metric("Avg Satisfaction",      f"{avg_satisfaction}%")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "Retention Rate",
    "Student Satisfaction",
    "Spring vs Fall",
    "Enrollment by Department"
])

sns.set_theme(style="whitegrid")

with tab1:
    st.markdown("### Retention Rate by Year")
    retention = df_filtered.groupby('Year')['Retention Rate (%)'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(retention['Year'], retention['Retention Rate (%)'],
            marker='o', linewidth=2.5, color='steelblue', markersize=7)
    for x, y in zip(retention['Year'], retention['Retention Rate (%)']):
        ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Retention Rate (%)")
    ax.set_xticks(retention['Year'])
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("Retention rate shows a positive trend from 2015 to 2024, with a slight drop in 2020.")

with tab2:
    st.markdown("### Student Satisfaction by Year")
    satisfaction = df_filtered.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=satisfaction, x='Year', y='Student Satisfaction (%)',
                 marker='s', linewidth=2.5, color='darkorange', ax=ax)
    for x, y in zip(satisfaction['Year'], satisfaction['Student Satisfaction (%)']):
        ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha='center', fontsize=8)
    ax.set_xlabel("Year")
    ax.set_ylabel("Satisfaction (%)")
    ax.set_xticks(satisfaction['Year'])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("Student satisfaction grew from 78% in 2015 to 88% in 2024.")

with tab3:
    st.markdown("### Spring vs Fall Comparison")
    comparison = df_filtered.groupby('Term')[
        ['Enrolled', 'Retention Rate (%)', 'Student Satisfaction (%)']
    ].mean().reset_index()

    metrics = ['Enrolled', 'Retention Rate (%)', 'Student Satisfaction (%)']
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    colors = ['#4C72B0', '#DD8452']

    for i, metric in enumerate(metrics):
        axes[i].bar(comparison['Term'], comparison[metric],
                    color=colors[:len(comparison)], edgecolor='white', width=0.5)
        axes[i].set_title(metric, fontsize=10, fontweight='bold')
        axes[i].set_ylabel("Average")
        for j, val in enumerate(comparison[metric]):
            axes[i].text(j, val + 0.3, f"{val:.1f}", ha='center', fontsize=10, fontweight='bold')

    fig.suptitle("Spring vs Fall", fontsize=13, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("Spring and Fall terms show similar metrics across all indicators.")

with tab4:
    st.markdown("### Enrollment by Department")
    departments = ['Engineering Enrolled', 'Business Enrolled',
                   'Arts Enrolled', 'Science Enrolled']
    dept_by_year = df_filtered.groupby('Year')[departments].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4))
    for col in departments:
        ax.plot(dept_by_year['Year'], dept_by_year[col],
                marker='o', linewidth=2, label=col.replace(' Enrolled', ''))
    ax.set_xlabel("Year")
    ax.set_ylabel("Students enrolled")
    ax.set_xticks(dept_by_year['Year'])
    ax.legend(title="Department")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("Engineering leads enrollment with a growing trend. Science shows a slight decline in recent years.")

st.markdown("---")

with st.expander("View filtered data"):
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

st.caption("Activity 1 - Data Mining - Universidad de la Costa")
