

import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Pro Kabaddi League (PKL) Analysis", layout="wide")


#  logo 
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/2/2b/919-9198627_the-league-will-continue-its-existing-format-and.png' width='350' height = '200'/>
        <h1 style='margin-top:10px;'>🏆 Pro Kabaddi League (Seasons 1–10) Analysis Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Loading cleaned data directly
m2 = pd.read_csv("notebooks/pkl_matches_cleaned.csv")
r = pd.read_csv("notebooks/pkl_rosters_cleaned.csv")


# CREATE TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Basic Overview",
    "🎯 Match-Level Analysis",
    "🏅 Team Analysis",
    "🏟️ Venue Insights",
    "👤 Player-Level Analysis"
])


# TAB 1 - BASIC OVERVIEW
with tab1:
    st.header("📊 Basic PKL Overview")

    # Centered KPIs
    total_matches = len(m2['match_id'].unique())
    total_players = len(r['player_id'].unique())

    st.markdown(
        f"""
        <div style="text-align:center; font-size:20px; margin-top:20px;">
        <b>Total Matches:</b> {total_matches}<br>    <b>Total Players:</b> {total_players}
        </div>
        """,
    unsafe_allow_html=True
    )


    st.subheader("🏆 Winner per Season")
    ws = pd.DataFrame(m2[m2['league_stage'] == 'Final'][['season', 'winner']])
    ws['count'] = 1
    fig1 = px.bar(ws, x='season', y='count', color='winner', text='winner',
                  title='Winner per Season', height=500)
    fig1.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🏟️ Number of Matches per League Stage")
    stage_counts = m2['league_stage'].value_counts().reset_index()
    stage_counts.columns = ['league_stage', 'count']
    fig2 = px.bar(stage_counts, x='league_stage', y='count', text='count',
                  color='league_stage', title='Number of Matches per League Stage', height=500)
    fig2.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)


# TAB 2 - MATCH LEVEL ANALYSIS
with tab2:
    st.header("🎯 Match-Level Analysis")

    # Max Scoring Matches per Season
    max_points = m2.groupby('season')['total_points_match'].max().reset_index()
    max_matches = pd.merge(
        max_points,
        m2[['season', 'team_name_1', 'team_name_2', 'total_points_match']],
        on=['season', 'total_points_match'],
        how='left'
    )
    max_matches['match'] = max_matches['team_name_1'] + " vs " + max_matches['team_name_2']
    fig3 = px.line(max_matches, x='season', y='total_points_match', text='total_points_match',
                   hover_data=['match'], markers=True,
                   title='Max Scoring Matches per Season')
    fig3.update_traces(textposition='top center')
    fig3.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    # Year wise matches
    ym = m2['year'].value_counts().reset_index()
    ym.columns = ['year', 'total matches']
    fig4 = px.line(ym.sort_values('year'), x='year', y='total matches', text='total matches',
                   title='📅 Year-wise Number of Matches', markers=True)
    fig4.update_layout(title_x=0.5, hovermode='x unified')
    st.plotly_chart(fig4, use_container_width=True)

    # Top 10 highest winning margin
    top10_margin = m2.sort_values(by='winning_margin', ascending=False)[
        ['season', 'winner', 'loser', 'winning_margin', 'match_name']
    ].head(10)
    fig5 = px.bar(top10_margin, x='season', y='winning_margin', color='winner',
                  text='winning_margin', hover_data=['match_name', 'winner', 'loser'],
                  title='Top 10 Matches with Highest Winning Margin (All Seasons)')
    fig5.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)


# TAB 3 - TEAM ANALYSIS
with tab3:
    st.header("🏅 Team Analysis")

    # Titles per team
    w = pd.DataFrame(m2[m2['league_stage'] == 'Final']['winner'].value_counts()).reset_index()
    w.columns = ['winner', 'titles']
    fig6 = px.bar(w, x='winner', y='titles', color='winner', text='titles',
                  title='🏆 Number of PKL Titles per Team')
    fig6.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

    # Max scoring team per season
    max_scores = m2.groupby('season')['max_score'].max().reset_index().rename(columns={'max_score': 'max_team_points'})
    candidates = pd.merge(
        max_scores,
        m2[['season', 'team_name_1', 'team_name_2', 'team_score_1', 'team_score_2', 'max_score']],
        left_on=['season', 'max_team_points'],
        right_on=['season', 'max_score'],
        how='left'
    )
    def get_max_scoring_team(row):
        teams = []
        if row['team_score_1'] == row['max_team_points']:
            teams.append(row['team_name_1'])
        if row['team_score_2'] == row['max_team_points']:
            teams.append(row['team_name_2'])
        return ",".join(teams)
    candidates['max_scoring_team'] = candidates.apply(get_max_scoring_team, axis=1)
    final_max = (candidates.groupby(['season', 'max_team_points'])['max_scoring_team']
                 .agg(lambda x: ",".join(sorted(set(x.str.split(", ").sum()))))
                 .reset_index())
    fig7 = px.bar(final_max, x='season', y='max_team_points', text='max_scoring_team',
                  title='Max Scoring Team(s) per Season', color='max_team_points')
    fig7.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)

    # Top 5 final playing teams
    finals = m2[m2['league_stage'] == 'Final']
    final_counts = finals.groupby('team_name_1').size().add(finals.groupby('team_name_2').size(), fill_value=0)
    final_counts = final_counts.reset_index()
    final_counts.columns = ['team_name', 'finals_played']
    top5_final_teams = final_counts.sort_values(by='finals_played', ascending=False).head(5)
    fig8 = px.bar(top5_final_teams, x='team_name', y='finals_played', color='finals_played',
                  text='finals_played', title='🏁 Top 5 Most Final-Playing Teams')
    fig8.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)

    # Top 10 most winning teams
    mw = m2['winner'].value_counts().reset_index().head(10)
    mw.columns = ['winner', 'wins']
    fig9 = px.bar(mw, x='winner', y='wins', color='wins', text='wins',
                  title='🏆 Top 10 Most Winning Teams (All Seasons)')
    fig9.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)



# TAB 4 - VENUE INSIGHTS
with tab4:
    st.header("🏟️ Venue Insights")

    v = m2['venue'].value_counts().head(10).reset_index()
    v.columns = ['venue', 'matches hosted']
    fig10 = px.bar(v, x='venue', y='matches hosted', color='matches hosted',
                   text='matches hosted', title='🎪 Top 10 Most Matches Hosting Venues')
    fig10.update_layout(title_x=0.5, showlegend=False, xaxis_tickangle=45)
    st.plotly_chart(fig10, use_container_width=True)



# TAB 5 - PLAYER LEVEL ANALYSIS
with tab5:
    st.header("👤 Player-Level Analysis")

    # Card totals
    cards = r[['green_card_count', 'yellow_card_count', 'red_card_count']].sum().reset_index()
    cards.columns = ['Card Type', 'Total Count']
    custom_colors = {'green_card_count': 'green', 'yellow_card_count': 'gold', 'red_card_count': 'red'}
    fig11 = px.bar(cards, x='Card Type', y='Total Count', color='Card Type',
                   color_discrete_map=custom_colors, text='Total Count',
                   title='Total Number of Cards Issued till Season 10')
    fig11.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig11, use_container_width=True)

    # Player card lookup
    st.subheader("🎴 Player Card Lookup")
    player_options = sorted(r['name'].unique())
    selected_player = st.selectbox("Select a player:", player_options)
    if selected_player:
        player_cards = r[r['name'] == selected_player][['green_card_count', 'yellow_card_count', 'red_card_count']].sum()
        st.metric("🟢 Green Cards", int(player_cards['green_card_count']))
        st.metric("🟡 Yellow Cards", int(player_cards['yellow_card_count']))
        st.metric("🔴 Red Cards", int(player_cards['red_card_count']))


    # Top 10 Green, Yellow, Red card receivers
    green = r.groupby('name', as_index=False)['green_card_count'].sum().sort_values(by='green_card_count', ascending=False).head(10)
    fig14 = px.bar(green, x='name', y='green_card_count', color='green_card_count', text='green_card_count',
                   title='🟢 Top 10 Players with Most Green Cards')
    fig14.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig14, use_container_width=True)

    yellow = r.groupby('name', as_index=False)['yellow_card_count'].sum().sort_values(by='yellow_card_count', ascending=False).head(10)
    fig15 = px.bar(yellow, x='name', y='yellow_card_count', color='yellow_card_count', text='yellow_card_count',
                   title='🟡 Top 10 Players with Most Yellow Cards')
    fig15.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig15, use_container_width=True)

    red = r.groupby('name', as_index=False)['red_card_count'].sum().sort_values(by='red_card_count', ascending=False).head(3)
    fig16 = px.bar(red, x='name', y='red_card_count', color='red_card_count', text='red_card_count',
                   title='🔴 Players with Red Cards')
    fig16.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig16, use_container_width=True)


    # Top raiders
    raider_stats = r.groupby('name', as_index=False)[['top_raider_count', 'total_points']].sum()
    top_raiders = raider_stats.sort_values(by='total_points', ascending=False).head(10)
    fig12 = px.bar(top_raiders, x='name', y='total_points', color='top_raider_count', text='total_points',
                   title='🔥 Top 10 Most Successful Raiders (by Total Points)', color_continuous_scale='sunset')
    fig12.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig12, use_container_width=True)

    # Top players by matches played
    player_stats = r.groupby(['player_id', 'name']).agg(
        total_matches=('played_count', 'sum'),
        seasons_played=('season', 'nunique')
    ).reset_index()
    most_played = player_stats.sort_values(by='total_matches', ascending=False).head(10)
    fig13 = px.bar(most_played, x='name', y='total_matches', color='seasons_played', text='total_matches',
                   title='🏅 Top 10 Players with Most Matches Played (till season 10)')
    fig13.update_layout(title_x=0.5, showlegend=False)
    st.plotly_chart(fig13, use_container_width=True)


    

