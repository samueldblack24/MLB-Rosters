import streamlit as st
import pandas as pd

# Load team data
@st.cache_data
def load_teams():
    return pd.read_csv("teams.csv")

# Load rosters data
@st.cache_data
def load_rosters():
    return pd.read_csv("rosters.csv")

teams_df = load_teams()
rosters_df = load_rosters()

# Set level order for sorting
level_order = {
    'Major League Baseball': 0, 'Triple-A': 1, "Double-A": 2, "High-A": 3, "Single-A": 4, "Rookie": 5
}

# Normalize levels
teams_df['display_level'] = teams_df['level'].replace({
    'Major League Baseball': "MLB",
    'Triple-A': "AAA",
    'Double-A': "AA",
    'High-A': "A+",
    'Single-A': "A",
    'Rookie': "ROK"
})
teams_df['level_rank'] = teams_df['display_level'].map(level_order)

# Get all MLB teams (one per organization)
mlb_teams = teams_df[teams_df['display_level'] == "MLB"].sort_values("organization")
mlb_names = mlb_teams['team'].tolist()

# MLB selection dropdown
selected_mlb = st.sidebar.selectbox("Select MLB Organization", mlb_names)

# Get the org name associated with the selected MLB team
selected_org = mlb_teams[mlb_teams['team'] == selected_mlb].iloc[0]['organization']

# Filter all teams in that org
org_teams = teams_df[teams_df['organization'] == selected_org].sort_values("level_rank")

# Expander for selecting affiliate
with st.sidebar.expander(f"{selected_org} Affiliates", expanded=True):
    affiliate_names = org_teams['team'].tolist()
    affiliate_display = [
        f"{row['team']} ({row['display_level']})"
        for _, row in org_teams.iterrows()
    ]
    selected_affiliate = st.radio("Select a Team", affiliate_display, index=0)

# Match the selection back to team name
selected_team = selected_affiliate.split(" (")[0]
team = teams_df[teams_df['team'] == selected_team].iloc[0]

# Display team page
st.title(f"{team['team']} ({team['abbreviation']})")
st.subheader(f"Level: {team['level']}")
st.markdown(
    f"**League:** {team['league']}  \n"
    f"**Division:** {team['division']}  \n"
    f"**Organization:** {team['organization']}"
)

# Filter the roster for selected team
team_roster = rosters_df[rosters_df['team'] == selected_team]

# Show roster section
st.subheader("Roster")

if team_roster.empty:
    st.info(f"No roster data available for {selected_team}.")
else:
    #Select columns and rename for display
    display_roster = team_roster[['name', 'number', 'position']]
    display_roster = display_roster.rename(columns={
        'name': "Name",
        'number': "#",
        'position': "Pos"
    })

    # Define custom position order
    position_order = {
        "P": 0, "C": 1, "1B": 2, "2B": 3, "SS": 4, "3B": 5,
        "LF": 6, "CF": 7, "RF": 8, "OF": 9, "DH": 10,
        "TWP": 11, "UT": 12
    }

    # Add a column for sorting
    display_roster["position_rank"] = display_roster["Pos"].map(position_order)

    # Sort and drop the helper column
    display_roster = display_roster.sort_values("position_rank").drop(columns="position_rank")

    # Show the roster table
    st.dataframe(display_roster.set_index('#'), use_container_width=True)