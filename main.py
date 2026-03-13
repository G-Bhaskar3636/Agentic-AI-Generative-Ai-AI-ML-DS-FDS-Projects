import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from setuptools.command.rotate import rotate

st.set_page_config(layout="wide", page_title="StartUp Analysis")

df = pd.read_csv(r"C:\Users\bhask\NIT-DS\startup")
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# ---------------- INVESTOR ANALYSIS ---------------- #

def investor_analysis(investor):

    i_df = df[df['investors'].str.contains(investor, case=False, na=False)][
        ['date','startup','vertival','city','round','amount']
    ]
    st.dataframe(i_df)

    col1, col2 = st.columns(2)

    with col1:
        st.header('Biggest Investments')

        top_i = df[df['investors'].str.contains(investor, case=False, na=False)]\
                .groupby('startup')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(top_i.index, top_i.values)
        plt.xticks(rotation=45, ha='right')

        st.pyplot(fig)

    with col2:
        st.header('Sector Investments')

        top_iv = df[df['investors'].str.contains(investor, case=False, na=False)]\
                .groupby('vertival')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig1, ax1 = plt.subplots()

        ax1.pie(top_iv.values, labels=top_iv.index, autopct="%0.2f%%")
        ax1.set_title(f"{investor} Investment by Industry")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        st.header('Funding Round Distribution')

        top_is = df[df['investors'].str.contains(investor, case=False, na=False)]\
                .groupby('round')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig3, ax3 = plt.subplots()
        ax3.pie(top_is.values, labels=top_is.index, autopct="%0.2f%%")

        st.pyplot(fig3)

    with col4:
        st.header('City Distribution')

        top_ic = df[df['investors'].str.contains(investor, case=False, na=False)]\
                .groupby('city')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig4, ax4 = plt.subplots()
        ax4.pie(top_ic.values, labels=top_ic.index, autopct="%0.2f%%")

        st.pyplot(fig4)


    st.header('Funding by Year')

    df['year'] = df['date'].dt.year

    top_iy = df[df['investors'].str.contains(investor, case=False, na=False)] \
            .groupby('year')['amount'].sum() \
            .sort_index()

    fig4, ax4 = plt.subplots(figsize=(8, 4))

    ax4.plot(top_iy.index, top_iy.values, marker='o', linewidth=2)

    ax4.set_xlabel("Year")
    ax4.set_ylabel("Funding Amount")
    ax4.set_title(f"{investor} Yearly Investment Trend")

    ax4.grid(True)

    st.pyplot(fig4)


# ---------------- STARTUP ANALYSIS ---------------- #

def startup_analysis(startup):

    s_df = df[df['startup'].str.contains(startup, case=False, na=False)][
        ['date','investors','vertival','city','round','amount']
    ]
    st.dataframe(s_df)

    col1, col2 = st.columns(2)

    with col1:
        st.header('Top Investors')

        top_s = df[df['startup'].str.contains(startup, case=False, na=False)]\
                .groupby('investors')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(top_s.index, top_s.values)

        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    with col2:
        st.header('Industry Distribution')

        top_sv = df[df['startup'].str.contains(startup, case=False, na=False)]\
                .groupby('vertival')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig1, ax1 = plt.subplots()

        ax1.pie(top_sv.values, labels=top_sv.index, autopct="%0.2f%%")
        ax1.set_title(f"{startup} Investment by Industry")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        st.header('Funding Round Distribution')

        top_sr = df[df['startup'].str.contains(startup, case=False, na=False)]\
                .groupby('round')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig2, ax2 = plt.subplots()

        ax2.pie(top_sr.values, labels=top_sr.index, autopct="%0.2f%%")
        st.pyplot(fig2)

    with col4:
        st.header('City Distribution')

        top_sc = df[df['startup'].str.contains(startup, case=False, na=False)]\
                .groupby('city')['amount'].sum()\
                .sort_values(ascending=False).head()

        fig3, ax3 = plt.subplots()

        ax3.pie(top_sc.values, labels=top_sc.index, autopct="%0.2f%%")
        st.pyplot(fig3)


    st.header('Funding by Year')

    top_sy = df[df['startup'].str.contains(startup, case=False, na=False)] \
            .groupby('year')['amount'].sum() \
            .sort_index()

    fig4, ax4 = plt.subplots(figsize=(8, 4))

    ax4.plot(top_sy.index, top_sy.values, marker='o', linewidth=2)

    ax4.set_xlabel("Year")
    ax4.set_ylabel("Funding Amount")
    ax4.set_title(f"{startup} Yearly Investment Trend")

    ax4.grid(True)

    st.pyplot(fig4)


# ---------------- OVERALL ANALYSIS ---------------- #

def overall_analysis():
    t_amount = round(df['amount'].sum())
    max_amount = df['amount'].max()
    avg_amount = round(df['amount'].mean())
    no_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Invested Amount", value=f"{t_amount:.2f}Cr")
    with col2:
        st.metric(label="Max Invested Amount", value=f"{max_amount:.2f}Cr")
    with col3:
        st.metric(label="Average Invested Amount", value=f"{avg_amount:.2f}Cr")
    with col4:
        st.metric(label="Total Startups", value=f"{no_startups:.2f}")

    choice = st.selectbox("Select Type", ("Total", "Count"))

    if choice == 'Total':
        p = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        p['year_month'] = pd.to_datetime(p['year'].astype(str) + '-' + p['month'].astype(str))
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(p['year_month'], p['amount'], marker='o', linewidth=0.8)
        ax.set_xlabel("Year-Month")
        ax.set_ylabel("Funding Amount")
        plt.grid(True)
        st.pyplot(fig)
    else:
        p = df.groupby(['year', 'month'])['amount'].count().reset_index()
        p['year_month'] = pd.to_datetime(p['year'].astype(str) + '-' + p['month'].astype(str))
        fig1, ax1 = plt.subplots(figsize=(10,5))
        ax1.plot(p['year_month'], p['amount'], marker='o', linewidth=0.8)
        ax1.set_xlabel("Year-Month")
        ax1.set_ylabel("Funding Count")
        plt.grid(True)
        st.pyplot(fig1)

    st.header("Top Sectors")
    col5, col6 = st.columns(2)

    with col5:
        sum_df = df.groupby('vertival')['amount'].sum().sort_values(ascending=False).head()

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(sum_df.values, labels=sum_df.index, autopct="%0.2f%%")
        ax2.set_title("Funding by Sector")

        st.pyplot(fig2)

    with col6:
        cou_df = df.groupby('vertival')['amount'].count().sort_values(ascending=False).head()

        fig3, ax3 = plt.subplots(figsize=(6, 6))
        ax3.pie(cou_df.values, labels=cou_df.index, autopct="%0.2f%%")
        ax3.set_title("Number of Deals by Sector")

        st.pyplot(fig3)

    st.header("Top Investors")

    choice1 = st.selectbox("Select Type", ("Top Funding", "City Wise Funding"))

    if choice1 == 'Top Funding':
        in_ver = df.groupby('investors')['vertival'].count().reset_index().sort_values('vertival', ascending=False).head()
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(in_ver['investors'], in_ver['vertival'], marker='o', linewidth=0.8)
        ax4.set_xlabel("Investors")
        ax4.set_ylabel("Number of Deals")
        ax4.grid(True)
        st.pyplot(fig4)
    else:
        in_c = df.groupby('city')['amount'].sum().reset_index().sort_values('amount', ascending=False).head()
        fig5, ax5 = plt.subplots(figsize=(10, 5))
        ax5.plot(in_c['city'], in_c['amount'], marker='o', linewidth=0.8)
        ax5.set_xlabel("Investors")
        ax5.set_ylabel("Amount")
        ax5.grid(True)
        st.pyplot(fig5)

    choice1 = st.selectbox("Select Type", ("Yearly Top Startup", "Top Startup"))

    if choice1 == 'Top Startup':
        top_startup = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig6, ax6 = plt.subplots(figsize=(10, 5))
        ax6.plot(top_startup.index, top_startup.values, marker='o', linewidth=0.8)
        ax6.set_ylabel("Amount")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        st.pyplot(fig6)
    else:
        top = df.groupby(['year', 'startup'])['amount'].sum().reset_index().sort_values(['year', 'amount'], ascending=[True, False]).groupby('year').head(1)
        top['year_startup'] = top['year'].astype('str') + '-' + top['startup'].astype('str')
        fig7, ax7 = plt.subplots(figsize=(10, 5))
        ax7.bar(top['year_startup'], top['amount'])
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig7)




# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Startup Funding Analysis")

choice = st.sidebar.selectbox(
    "Select",
    ['OverAll Analysis','StartUp','Investor']
)

if choice == 'OverAll Analysis':

    st.title("Overall Analysis")

    overall_analysis()

elif choice == 'StartUp':

    select_startup = st.sidebar.selectbox(
        'Startup Names',
        ['Select Startup'] + sorted(
            set(df['startup'].str.split(',').explode().str.strip())
        )
    )

    st.title("Startup Analysis")

    btn1 = st.sidebar.button('Startup Analysis')

    if btn1:

        st.header(select_startup)

        startup_analysis(select_startup)


else:

    st.title("Investor")

    select_investor = st.sidebar.selectbox(
        'Investor',
        ['Select Investor'] + sorted(
            set(df['investors'].str.split(',').explode().str.strip())
        )
    )

    btn2 = st.sidebar.button('Investor Analysis')

    if btn2:

        st.header(select_investor)

        investor_analysis(select_investor)