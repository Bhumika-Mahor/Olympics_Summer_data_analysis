import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import requests
from streamlit_lottie import st_lottie


def load_lottie_olympic(url):
    r= requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_olympic = load_lottie_olympic("https://assets7.lottiefiles.com/private_files/lf30_9dpbs7iq.json")


st.set_page_config(layout="wide")
first, last = st.columns([6,2])
first.title("OLYMPICS DATA ANALYSIS (Summer)")
with last:
    st_lottie(lottie_olympic, key="Olympics")


st.sidebar.title("Olympics Analysis")
st.sidebar.image("Olympics.jpg")

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select the Analysis',
    ('Home', 'Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis ', 'World Map')
)

if user_menu == 'Home':
    st.header("Home")

    st.subheader("Data Analysis of Olympics for the Summer season , "
             "is done to find out how many sports are played till now from 1900 to 2016. "
             "Which country have participated and  how much time it participated and which country have won which medal in which year "
             "and much more information. Basically, The reason for the development of this analysis is to learn data visualization for given inputs")
    st.image("Olympics.jpg", width=800)


if user_menu == 'Medal Tally':

    st.sidebar.title("Medal Tally")

    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("select Year", years)
    selected_country = st.sidebar.selectbox("select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header("Overall Olympics Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != "Overall":
        st.header(selected_country + " Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(selected_country + " Performance in " + str(selected_year))


    def load_medal_olympic(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    medal_olympic = load_medal_olympic("https://assets7.lottiefiles.com/private_files/lf30_htpumt01.json")
    st_lottie(medal_olympic, width= 200, key="medal")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.header("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Year wise Editions")
        st.title(editions)
    with col2:
        st.subheader("Hosting Cities")
        st.title(cities)
    with col3:
        st.subheader("Organising Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Participating Athletes")
        st.title(athletes)
    with col3:
        st.subheader("Nations Participated")
        st.title(nations)


    st.header("Most Successful Athletes")

    def load_successful_athlete_olympic(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    successful_athlete = load_successful_athlete_olympic("https://assets7.lottiefiles.com/packages/lf20_i0f0vmp8.json")
    st_lottie(successful_athlete, width= 200, key="successful-athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select the Sport', sport_list)
    x = helper.most_succesful(df, selected_sport)
    st.table(x)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the Year:-")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.header("Occurring Events over the Year:-")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.header("Athletes over the Year:-")
    st.plotly_chart(fig)

    st.header("No. of Events over time( Every Sport)")
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)



if user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country wise Analysis')

    st.header('Country wise Analysis')

    def load_country_olympic(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    country = load_country_olympic("https://assets8.lottiefiles.com/packages/lf20_21xiiubl.json")
    st_lottie(country, width= 200, key="Country")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.header("Medal Tally of " + selected_country + " over the Years")
    st.plotly_chart(fig)

    st.header("Top 10 athletes of " + selected_country)

    def load_top10_olympic(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    top10 = load_top10_olympic("https://assets5.lottiefiles.com/private_files/lf30_j57dwawi.json")
    st_lottie(top10, width=200, key="top10")

    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

    st.header(selected_country + " excels in the following sport")

    def load_excels_olympic(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    excels_sport = load_excels_olympic("https://assets7.lottiefiles.com/packages/lf20_ksnjgcd3.json")
    st_lottie(excels_sport, width=200, key="excels")

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)



if user_menu == 'Athlete wise Analysis ':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age w.r.t Sports for Gold Medalist")

    def load_gold_medal(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    gold_medal = load_gold_medal("https://assets8.lottiefiles.com/packages/lf20_ly62jiq0.json")
    st_lottie(gold_medal, width=200, key="gold")

    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age w.r.t Sports for Silver Medalist")

    def load_silver_medal(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    silver_medal = load_silver_medal("https://assets7.lottiefiles.com/datafiles/NvSZw4XogL6CADr/data.json")
    st_lottie(silver_medal, width=200, key="silver")

    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.header('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.header("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

if user_menu == 'World Map':
    st.header("World Map")
    def load_worldmap(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    worldmap = load_worldmap("https://assets5.lottiefiles.com/packages/lf20_j1pdRk.json")
    st_lottie(worldmap, width=300, key="world")
    st.map()


st.text("This website is made by Bhumika-Mahor")