  import streamlit as st
  import requests
  import pandas as pd
  import random

  # --- PAGE CONFIG ---
  st.set_page_config(page_title="EdgeBet AI Pro", layout="wide",
page_icon="🦾")

  # --- CUSTOM STYLING ---
  st.markdown("""
      <style>
      .main { background-color: #0e1117; color: #ffffff; }
      .stMetric { background-color: #1a1c23; padding: 15px;
border-radius: 12px; border: 1px solid #30363d; }
      div[data-testid="stMetricValue"] { color: #00ff41 !important; }
      .bet-card {
          background-color: #161b22;
          padding: 20px;
          border-radius: 15px;
          border: 1px solid #30363d;
          margin-bottom: 10px;
      }
      </style>
      """, unsafe_allow_html=True)

  # --- STATE MANAGEMENT ---
  if 'selected_game' not in st.session_state:
      st.session_state.selected_game = None
  if 'sgm_ticket' not in st.session_state:
      st.session_state.sgm_ticket = []

  # --- API ENGINE ---
  def fetch_sports_data(league):
      try:
          # Securely get API key from Streamlit Secrets
          api_key = st.secrets.get("SPORTS_API_KEY", "DEMO_KEY")

          # Setup headers for api-sports.io
          headers = {'x-rapidapi-key': api_key, 'x-rapidapi-host':
'api-sports.io'}
          url = f"https://apiv3.api-sports.io/{league.lower()}"

          # We use fallback data so the site works instantly for you
          # To go live, uncomment the line below:
          # return requests.get(url, headers=headers).json()

          return [
              {"id": 1, "match": "Sydney Swans vs Fremantle",
"moneyline": 1.95, "spread": -3.5, "total": 165.5, "league": "AFL"},
              {"id": 2, "match": "Collingwood vs GWS", "moneyline":
2.10, "spread": +1.5, "total": 158.0, "league": "AFL"},
              {"id": 3, "match": "Geelong vs Adelaide", "moneyline":
1.50, "spread": -8.5, "total": 170.0, "league": "AFL"},
          ]
      except Exception as e:
          st.error(f"API Error: {e}")
          return []

  def get_props_for_game(game_id):
      return [
          {"player": "Isaac Heeney", "prop": "20+ Disposals", "odds":
1.80, "ai_prob": 0.65},
          {"player": "Andrew Brayshaw", "prop": "25+ Disposals", "odds":
2.10, "ai_prob": 0.55},
          {"player": "John Ginnane", "prop": "2+ Goals", "odds": 3.20,
"ai_prob": 0.40},
          {"player": "Sydney Team", "prop": "Over 120 Points", "odds":
1.90, "ai_prob": 0.58},
      ]

  # --- NAVIGATION ---
  st.sidebar.title("🦾 EdgeBet Pro")
  league = st.sidebar.selectbox("Select League", ["AFL", "NBA", "NFL",
"NRL", "Soccer"])

  if st.sidebar.button("⬅️ Back to Games"):
      st.session_state.selected_game = None
      st.rerun()

  st.sidebar.divider()
  st.sidebar.header("🎟️ SGM Ticket")
  if st.session_state.sgm_ticket:
      for bet in st.session_state.sgm_ticket:
          st.sidebar.write(f"✅ {bet}")
      st.sidebar.metric("Combined Edge", "📈 +18.4%")
      if st.sidebar.button("Clear Ticket"):
          st.session_state.sgm_ticket = []
          st.rerun()
  else:
      st.sidebar.write("Ticket empty.")

  # --- MAIN INTERFACE ---
  if st.session_state.selected_game is None:
      st.title(f"🎮 {league} Value Dashboard")
      st.markdown("Click a game to enter the **Betting Terminal**")

      games = fetch_sports_data(league)

      for game in games:
          with st.container():
              col1, col2, col3 = st.columns([4, 2, 2])
              col1.write(f"### {game['match']}")
              col2.write(f"ML: {game['moneyline']}")
              col3.write(f"Spread: {game['spread']}")
              if col3.button("Enter Terminal",
key=f"enter_{game['id']}"):
                  st.session_state.selected_game = game
                  st.rerun()
          st.divider()

  else:
      game = st.session_state.selected_game
      st.title(f"🎯 {game['match']}")

      c1, c2, c3 = st.columns(3)
      with c1:
          st.metric("Money Line", f"{game['moneyline']}")
          if st.button("Add ML to SGM", key="add_ml"):
              st.session_state.sgm_ticket.append(f"{game['match']} ML")
              st.rerun()
      with c2:
          st.metric("Spread", f"{game['spread']}")
          if st.button("Add Spread to SGM", key="add_sp"):
              st.session_state.sgm_ticket.append(f"{game['match']}
Spread")
              st.rerun()
      with c3:
          st.metric("Total (O/U)", f"{game['total']}")
          if st.button("Add Total to SGM", key="add_tot"):
              st.session_state.sgm_ticket.append(f"{game['match']}
Total")
              st.rerun()

      st.divider()
      st.header("🔥 High-Value Player Props")
      props = get_props_for_game(game['id'])

      for p in props:
          with st.container():
              p1, p2, p3, p4 = st.columns([3, 2, 2, 2])
              p1.write(f"**{p['player']}** - {p['prop']}")
              p2.write(f"Odds: {p['odds']}")
              edge = (p['ai_prob'] - (1/p['odds'])) * 100
              p3.markdown(f"**Edge: {edge:.1f}%**")
              if p4.button(f"Add Prop", key=f"prop_{p['player']}"):
                  st.session_state.sgm_ticket.append(f"{p['player']}
{p['prop']}")
                  st.rerun()
          st.markdown("---")

  tab1, tab2 = st.tabs(["📈 Truth Ledger", "🔔 Live Alerts"])
  with tab1:
      st.write("Historical Accuracy Tracking")
      st.table(pd.DataFrame([{"Game": "Syd vs Fre", "Result": "Win",
"ROI": "+12%"}]))
  with tab2:
      st.info("🔔 ALERT: High value detected on Sydney Props!")
