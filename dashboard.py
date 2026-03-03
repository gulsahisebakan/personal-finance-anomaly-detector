import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
df = pd.read_csv("transactions_analyzed.csv")
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.strftime("%Y-%m")

# Separate normal and anomaly transactions
anomalies = df[df["anomaly_score"] == -1]
normal = df[df["anomaly_score"] == 1]

# ── 2. BUILD THE DASH APP ─────────────────────────────────────────────────────
# Dash lets us build interactive web dashboards using only Python
# No HTML or JavaScript knowledge needed
app = Dash(__name__)

# ── 3. LAYOUT ─────────────────────────────────────────────────────────────────
# This defines what the dashboard looks like
# Think of it as building blocks stacked on top of each other
app.layout = html.Div([

    # Header
    html.Div([
        html.H1("💰 Personal Finance Anomaly Detector",
                style={"color": "white", "margin": "0", "fontSize": "28px"}),
        html.P("Powered by Isolation Forest ML Algorithm",
               style={"color": "#aaa", "margin": "5px 0 0 0"})
    ], style={
        "background": "#1a1a2e",
        "padding": "25px 30px",
        "marginBottom": "20px"
    }),

    # Summary cards row
    html.Div([
        # Total transactions card
        html.Div([
            html.H3("Total Transactions", style={"color": "#aaa", "fontSize": "14px", "margin": "0"}),
            html.H2(f"{len(df):,}", style={"color": "white", "margin": "8px 0 0 0", "fontSize": "32px"})
        ], style={"background": "#16213e", "padding": "20px", "borderRadius": "10px", "flex": "1"}),

        # Anomalies found card
        html.Div([
            html.H3("Anomalies Found", style={"color": "#aaa", "fontSize": "14px", "margin": "0"}),
            html.H2(f"{len(anomalies):,}", style={"color": "#e94560", "margin": "8px 0 0 0", "fontSize": "32px"})
        ], style={"background": "#16213e", "padding": "20px", "borderRadius": "10px", "flex": "1"}),

        # Total spent card
        html.Div([
            html.H3("Total Spent", style={"color": "#aaa", "fontSize": "14px", "margin": "0"}),
            html.H2(f"${df['amount'].sum():,.0f}", style={"color": "#0f9b8e", "margin": "8px 0 0 0", "fontSize": "32px"})
        ], style={"background": "#16213e", "padding": "20px", "borderRadius": "10px", "flex": "1"}),

        # Anomaly total card
        html.Div([
            html.H3("Anomaly Spend", style={"color": "#aaa", "fontSize": "14px", "margin": "0"}),
            html.H2(f"${anomalies['amount'].sum():,.0f}", style={"color": "#f5a623", "margin": "8px 0 0 0", "fontSize": "32px"})
        ], style={"background": "#16213e", "padding": "20px", "borderRadius": "10px", "flex": "1"}),

    ], style={"display": "flex", "gap": "15px", "padding": "0 30px", "marginBottom": "20px"}),

    # Category filter dropdown
    html.Div([
        html.Label("Filter by Category:", style={"color": "white", "marginBottom": "8px", "display": "block"}),
        dcc.Dropdown(
            id="category-filter",
            options=[{"label": "All Categories", "value": "ALL"}] +
                    [{"label": c, "value": c} for c in sorted(df["category"].unique())],
            value="ALL",
            style={"width": "300px"}
        )
    ], style={"padding": "0 30px", "marginBottom": "20px"}),

    # Charts row
    html.Div([
        # Scatter plot - all transactions
        html.Div([
            dcc.Graph(id="scatter-plot")
        ], style={"flex": "2", "background": "#16213e", "borderRadius": "10px", "padding": "15px"}),

        # Spending by category bar chart
        html.Div([
            dcc.Graph(id="category-chart")
        ], style={"flex": "1", "background": "#16213e", "borderRadius": "10px", "padding": "15px"}),

    ], style={"display": "flex", "gap": "15px", "padding": "0 30px", "marginBottom": "20px"}),

    # Monthly spending trend
    html.Div([
        dcc.Graph(id="monthly-trend")
    ], style={"margin": "0 30px", "background": "#16213e", "borderRadius": "10px", "padding": "15px"}),

    # Anomaly table
    html.Div([
        html.H3("🚨 Flagged Transactions", style={"color": "white", "marginBottom": "15px"}),
        html.Table(
            # Table header
            [html.Tr([
                html.Th(col, style={"color": "#aaa", "padding": "8px 15px", "textAlign": "left", "borderBottom": "1px solid #333"})
                for col in ["Date", "Category", "Amount", "Note", "Z-Score"]
            ])] +
            # Table rows
            [html.Tr([
                html.Td(str(row["date"])[:10], style={"color": "white", "padding": "8px 15px"}),
                html.Td(row["category"], style={"color": "white", "padding": "8px 15px"}),
                html.Td(f"${row['amount']:,.2f}", style={"color": "#e94560", "padding": "8px 15px", "fontWeight": "bold"}),
                html.Td(row["note"], style={"color": "#aaa", "padding": "8px 15px"}),
                html.Td(f"{row['z_score']:.2f}", style={"color": "#f5a623", "padding": "8px 15px"}),
            ]) for _, row in anomalies.sort_values("amount", ascending=False).iterrows()],
            style={"width": "100%", "borderCollapse": "collapse"}
        )
    ], style={"margin": "0 30px 30px 30px", "background": "#16213e", "borderRadius": "10px", "padding": "20px"}),

], style={"background": "#0f0f23", "minHeight": "100vh", "fontFamily": "Arial, sans-serif"})

# ── 4. CALLBACKS ──────────────────────────────────────────────────────────────
# Callbacks make the dashboard interactive
# When the user changes the dropdown, these functions automatically re-run
# and update the charts

@app.callback(
    Output("scatter-plot", "figure"),
    Output("category-chart", "figure"),
    Output("monthly-trend", "figure"),
    Input("category-filter", "value")
)
def update_charts(selected_category):
    # Filter data based on dropdown selection
    if selected_category == "ALL":
        filtered = df
    else:
        filtered = df[df["category"] == selected_category]

    # ── Chart 1: Scatter plot of all transactions ──
    fig_scatter = go.Figure()

    # Plot normal transactions
    normal_data = filtered[filtered["anomaly_score"] == 1]
    fig_scatter.add_trace(go.Scatter(
        x=normal_data["date"],
        y=normal_data["amount"],
        mode="markers",
        name="Normal",
        marker=dict(color="#0f9b8e", size=5, opacity=0.6),
        hovertemplate="<b>%{text}</b><br>Amount: $%{y:,.2f}<br>Date: %{x}<extra></extra>",
        text=normal_data["category"]
    ))

    # Plot anomalies in red
    anomaly_data = filtered[filtered["anomaly_score"] == -1]
    fig_scatter.add_trace(go.Scatter(
        x=anomaly_data["date"],
        y=anomaly_data["amount"],
        mode="markers",
        name="Anomaly",
        marker=dict(color="#e94560", size=12, symbol="x", opacity=1),
        hovertemplate="<b>%{text}</b><br>Amount: $%{y:,.2f}<br>Date: %{x}<extra></extra>",
        text=anomaly_data["note"]
    ))

    fig_scatter.update_layout(
        title="All Transactions (Red X = Anomaly)",
        paper_bgcolor="#16213e", plot_bgcolor="#16213e",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333"),
        yaxis=dict(gridcolor="#333")
    )

    # ── Chart 2: Spending by category ──
    cat_spend = filtered.groupby("category")["amount"].sum().reset_index()
    fig_category = px.bar(
        cat_spend, x="amount", y="category",
        orientation="h", title="Total Spend by Category",
        color="amount", color_continuous_scale="teal"
    )
    fig_category.update_layout(
        paper_bgcolor="#16213e", plot_bgcolor="#16213e",
        font=dict(color="white"), showlegend=False,
        coloraxis_showscale=False
    )

    # ── Chart 3: Monthly spending trend ──
    monthly = filtered.groupby("month")["amount"].sum().reset_index()
    fig_monthly = px.line(
        monthly, x="month", y="amount",
        title="Monthly Spending Trend",
        markers=True
    )
    fig_monthly.update_traces(line_color="#0f9b8e", marker=dict(color="#f5a623", size=8))
    fig_monthly.update_layout(
        paper_bgcolor="#16213e", plot_bgcolor="#16213e",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333"),
        yaxis=dict(gridcolor="#333")
    )

    return fig_scatter, fig_category, fig_monthly

# ── 5. RUN THE APP ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)

