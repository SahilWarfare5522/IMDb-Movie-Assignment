# 📊 IMDb Top 100 Movies Analysis – SmithWorks Studios
# Author: Sahil Verma
# Objective: Analyze IMDb data to guide movie production decisions

# --- [1] Imports and Setup ---
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display

# Set plotting styles
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8-darkgrid')

# --- [2] Load the Data ---
df = pd.read_csv("G:/Github Assignments Data/IMDb Movie Assignment/Movie Assignment Data/Movie Assignment Data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")

# --- [3] Task 2: Budget Summary ---
print("\n🎯 Budget Summary:")
print(df['budget'].describe())

plt.figure(figsize=(10,5))
sns.histplot(df['budget'], bins=20, kde=True, color='skyblue')
plt.title('📊 Distribution of Movie Budgets')
plt.xlabel('Budget (USD)')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.show()

fig = px.box(df, y='budget', title='🎬 Box Plot of Movie Budgets', points="all", color_discrete_sequence=['indianred'])
fig.show()

# --- [4] Task 3: PG-13 US Movies ---
pg13_us = df[(df['content_rating'] == 'PG-13') & (df['country'] == 'United States')]
print(f"\n🇺🇸 PG-13 Movies from the US: {pg13_us.shape[0]}")

# --- [5] Task 4: 2014 Non-US Movies ---
movies_2014_non_us = df[(df['title_year'] == 2014) & (df['country'] != 'United States')]
print(f"\n🌍 2014 Movies not from US: {movies_2014_non_us.shape[0]}")
print(movies_2014_non_us[['title', 'country']])

# --- [6] Task 5: Genre Count Analysis ---
df['genre_count'] = df[['genre_1','genre_2','genre_3']].notna().sum(axis=1)
genre_counts = df['genre_count'].value_counts().sort_index()
genre_percentages = round((genre_counts / len(df)) * 100, 2)
genre_summary = pd.DataFrame({
    'Number of Genres': genre_counts.index,
    'Number of Movies': genre_counts.values,
    'Percentage': genre_percentages.values
})

fig = px.pie(
    genre_summary,
    values='Percentage',
    names=genre_summary['Number of Genres'].astype(str) + " Genre(s): " + genre_summary['Percentage'].astype(str) + "%",
    title='🎬 Genre Distribution of Top 100 Movies',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig.update_traces(textposition='inside', textinfo='label+percent', pull=[0, 0.05, 0.1])
fig.show()

# --- [7] Task 6: Convert Budget & Gross to Millions ---
df['budget_million'] = (df['budget'] / 1_000_000).round(3)
df['gross_million'] = (df['gross'] / 1_000_000).round(3)

# --- [8] Task 7: Top 10 Profitable Movies ---
df['profit_million'] = df['gross_million'] - df['budget_million']
top_10_profit = df.sort_values(by='profit_million', ascending=False).head(10)
fig = px.bar(
    top_10_profit,
    x='profit_million',
    y='title',
    orientation='h',
    title='💰 Top 10 Most Profitable Movies',
    labels={'profit_million': 'Profit (Million USD)'},
    color='profit_million',
    color_continuous_scale='Viridis'
)
fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=600)
fig.show()

# --- [9] Task 8: Unique Actor List (Interactive Table) ---
all_actors = pd.concat([df['actor_1_name'], df['actor_2_name'], df['actor_3_name']])
unique_actors = sorted(all_actors.dropna().unique())
unique_actor_df = pd.DataFrame(unique_actors, columns=['actor_name'])

fig = go.Figure(data=[go.Table(
    header=dict(values=["🎭 Actor Name"], fill_color='royalblue', align='left', font=dict(color='white', size=14)),
    cells=dict(values=[unique_actor_df['actor_name']], fill_color='lavender', align='left', font=dict(size=13))
)])
fig.update_layout(title='🎬 Unique Actor List from Top 100 Movies', height=600)
fig.show()

# --- [10] Task 9: Top 3 Actors by Appearances ---
actor_counts = all_actors.value_counts()
top_3_actors = actor_counts.head(3).reset_index()
top_3_actors.columns = ['actor_name', 'movie_count']
fig = px.bar(
    top_3_actors,
    x='movie_count',
    y='actor_name',
    orientation='h',
    title='🌟 Top 3 Actors by Number of Appearances',
    color='movie_count',
    color_continuous_scale='tealgrn'
)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show()

# --- [11] Task 10: Country-wise Movie Count ---
country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'movie_count']

fig = px.bar(
    country_counts,
    x='country',
    y='movie_count',
    title='🌎 Top-Rated Movies by Country',
    labels={'movie_count': 'Number of Movies'},
    color='movie_count',
    color_continuous_scale='Blues'
)
fig.update_layout(xaxis_tickangle=-45)
fig.show()

fig_map = px.choropleth(
    country_counts,
    locations="country",
    locationmode="country names",
    color="movie_count",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title='🗺️ Global Distribution of Top-Rated Movies'
)
fig_map.update_geos(showcountries=True, projection_type="natural earth")
fig_map.show()
