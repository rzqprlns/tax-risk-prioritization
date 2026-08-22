import pandas as pd
import streamlit as st

from scoring import calculate_risk_score


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Tax Review Prioritization Lab",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --cream:#fffaf2;
    --ink:#172033;
    --muted:#707683;
    --blue:#4169e1;
    --yellow:#ffd95a;
    --mint:#ccefe3;
    --peach:#ffd8c7;
    --line:#ddd8cf;
}

html, body, [class*="css"] {
    font-family:'DM Sans',sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 95% 3%, #e6edff 0, transparent 23%),
        radial-gradient(circle at 4% 16%, #fff1b8 0, transparent 18%),
        var(--cream);
    color:var(--ink);
}

.block-container {
    max-width:1120px;
    padding-top:2rem;
    padding-bottom:5rem;
}

h1 {
    font-weight:700 !important;
    letter-spacing:-0.055em !important;
    line-height:.98 !important;
}

h2, h3 {
    letter-spacing:-0.03em !important;
}

p {
    color:var(--muted);
    line-height:1.75;
}

div[data-testid="stMetric"] {
    background:rgba(255,255,255,.72);
    border:1px solid var(--ink);
    padding:1rem;
    min-height:108px;
}

div[data-testid="stMetricLabel"] {
    font-family:'IBM Plex Mono',monospace;
    text-transform:uppercase;
    letter-spacing:.05em;
    font-size:.68rem;
}

div[data-testid="stMetricValue"] {
    font-weight:700;
    letter-spacing:-.03em;
}

div.stButton > button {
    border-radius:0;
    border:1px solid var(--ink);
    background:var(--ink);
    color:white;
    font-family:'IBM Plex Mono',monospace;
    text-transform:uppercase;
    letter-spacing:.04em;
}

div.stButton > button:hover {
    background:var(--yellow);
    color:var(--ink);
    border-color:var(--ink);
}

div[data-testid="stDataFrame"] {
    border:1px solid var(--line);
}

div[data-testid="stExpander"] {
    border-radius:0;
    border:1px solid var(--line);
    background:rgba(255,255,255,.55);
}

hr {
    border:none;
    border-top:1px solid var(--line);
    margin:3rem 0;
}

header[data-testid="stHeader"] {
    background:transparent;
}

#MainMenu, footer {
    visibility:hidden;
}

@media(max-width:760px) {
    .block-container {
        padding-left:1rem;
        padding-right:1rem;
        padding-top:1.4rem;
    }

    h1 {
        font-size:3.25rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("synthetic_tax_data.csv")


def label(text):
    st.caption(text.upper())


def rupiah_short(value):
    if value >= 1_000_000_000:
        return f"Rp{value / 1_000_000_000:.2f} B"
    elif value >= 1_000_000:
        return f"Rp{value / 1_000_000:.1f} M"
    return f"Rp{value:,.0f}"


def percent(value):
    return f"{value * 100:+.1f}%"


# =========================================================
# HERO
# =========================================================

label("Rizqi / Data Lab · 02")

st.title("Which cases\ndeserve attention first?")

st.write(
    """
A synthetic rule-based analytics project exploring how
administrative records can be prioritized for further review
using transparent and explainable indicators.
"""
)

st.info(
    "This is an educational portfolio simulation. All records are "
    "synthetic, and the rules, thresholds, and weights are independently "
    "designed for demonstration purposes. They are not DJP methodology."
)


# =========================================================
# LOAD DATA
# =========================================================

raw_df = load_data()
scored_df = calculate_risk_score(raw_df)


high_count = (scored_df["priority"] == "HIGH").sum()
medium_count = (scored_df["priority"] == "MEDIUM").sum()
low_count = (scored_df["priority"] == "LOW").sum()


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Synthetic records", f"{len(scored_df):,}")

with m2:
    st.metric("High priority", f"{high_count:,}")

with m3:
    st.metric("Medium priority", f"{medium_count:,}")

with m4:
    st.metric("Low priority", f"{low_count:,}")


st.divider()


# =========================================================
# CONCEPT
# =========================================================

label("How it works")
st.header("Signals, not verdicts.")

st.write(
    """
The system does not attempt to decide whether a taxpayer is compliant
or non-compliant. It identifies records whose synthetic data patterns
trigger predefined review signals.

A higher score simply means that more — or more heavily weighted —
rules were triggered.
"""
)


c1, c2, c3, c4 = st.columns(4)

with c1:
    label("01 / Measure")
    st.subheader("Calculate")
    st.caption(
        "Calculate revenue growth, payment growth, and payment ratios."
    )

with c2:
    label("02 / Detect")
    st.subheader("Check rules")
    st.caption(
        "Test each record against transparent heuristic conditions."
    )

with c3:
    label("03 / Score")
    st.subheader("Add points")
    st.caption(
        "Combine triggered indicators using predefined weights."
    )

with c4:
    label("04 / Review")
    st.subheader("Prioritize")
    st.caption(
        "Rank records into low, medium, or high review priority."
    )


st.divider()


# =========================================================
# RAW DATA
# =========================================================

label("Step 01 · Synthetic records")
st.header("Start with the underlying data.")

st.write(
    """
The raw dataset contains only basic period-to-period information.
Growth rates, ratios, scores, and priority levels are calculated
by Python rather than stored in the original CSV.
"""
)

with st.expander("Preview synthetic raw data", expanded=True):
    st.dataframe(
        raw_df,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# =========================================================
# FEATURE ENGINEERING
# =========================================================

label("Step 02 · Feature engineering")
st.header("Turn raw numbers into signals.")

st.write(
    """
The application derives analytical features from the original values.
For example, revenue growth measures how much revenue changed relative
to the previous period.
"""
)


example = scored_df.iloc[0]

f1, f2, f3 = st.columns(3)

with f1:
    st.metric(
        "Revenue growth",
        percent(example["revenue_growth"]),
    )

with f2:
    st.metric(
        "Payment growth",
        percent(example["payment_growth"]),
    )

with f3:
    st.metric(
        "Payment ratio change",
        f"{example['payment_ratio_change'] * 100:+.2f} pp",
    )

st.caption(
    f"Example shown above: {example['taxpayer_id']}. "
    "pp = percentage points."
)


st.divider()


# =========================================================
# RULES
# =========================================================

label("Step 03 · Rule-based scoring")
st.header("Four transparent rules.")

st.write(
    """
The weights below are heuristic choices created for this synthetic
portfolio project. They are visible by design so every score can
be explained.
"""
)


r1, r2 = st.columns(2)

with r1:
    st.subheader("+35 · Opposite movement")
    st.write(
        "Revenue grows by at least 20%, while payment decreases."
    )

    st.subheader("+25 · Ratio decline")
    st.write(
        "Payment-to-revenue ratio declines by at least "
        "1 percentage point."
    )

with r2:
    st.subheader("+20 · Repeated late filing")
    st.write(
        "Two or more late filings. One late filing receives +10."
    )

    st.subheader("+20 · Large revenue growth")
    st.write(
        "Revenue grows by at least 40% between periods."
    )


st.divider()


# =========================================================
# PRIORITY OVERVIEW
# =========================================================

label("Step 04 · Prioritization")
st.header("See where the records land.")

priority_order = ["HIGH", "MEDIUM", "LOW"]

overview = (
    scored_df["priority"]
    .value_counts()
    .reindex(priority_order, fill_value=0)
    .rename_axis("Priority")
    .reset_index(name="Records")
)

st.bar_chart(
    overview,
    x="Priority",
    y="Records",
)


priority_filter = st.multiselect(
    "Filter priority",
    ["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM", "LOW"],
)

sector_filter = st.multiselect(
    "Filter sector",
    sorted(scored_df["sector"].unique()),
    default=sorted(scored_df["sector"].unique()),
)


filtered_df = scored_df[
    scored_df["priority"].astype(str).isin(priority_filter)
    & scored_df["sector"].isin(sector_filter)
].copy()


display_df = filtered_df[
    [
        "taxpayer_id",
        "sector",
        "revenue_growth",
        "payment_growth",
        "late_filings",
        "risk_score",
        "priority",
    ]
].copy()

display_df["revenue_growth"] = (
    display_df["revenue_growth"] * 100
).round(1)

display_df["payment_growth"] = (
    display_df["payment_growth"] * 100
).round(1)


st.dataframe(
    display_df.sort_values(
        "risk_score",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
)
st.divider()


# =========================================================
# CASE EXPLORER
# =========================================================

label("Case explorer")
st.header("Why was this case flagged?")

st.write(
    """
Select one synthetic record to inspect the numbers behind its score.
This makes the prioritization process explainable rather than returning
a score with no context.
"""
)


case_options = (
    scored_df
    .sort_values("risk_score", ascending=False)["taxpayer_id"]
    .tolist()
)

selected_id = st.selectbox(
    "Choose a synthetic taxpayer",
    case_options,
)

case = scored_df[
    scored_df["taxpayer_id"] == selected_id
].iloc[0]


# =========================================================
# CASE HEADER
# =========================================================

case1, case2, case3 = st.columns(3)

with case1:
    st.metric(
        "Risk score",
        f"{int(case['risk_score'])} / 100"
    )

with case2:
    st.metric(
        "Review priority",
        str(case["priority"])
    )

with case3:
    st.metric(
        "Sector",
        case["sector"]
    )


# =========================================================
# PERIOD COMPARISON
# =========================================================

st.subheader("Period comparison")

p1, p2 = st.columns(2)

with p1:
    label("Previous period")

    st.metric(
        "Revenue",
        rupiah_short(case["revenue_prev"])
    )

    st.metric(
        "Payment",
        rupiah_short(case["payment_prev"])
    )


with p2:
    label("Current period")

    st.metric(
        "Revenue",
        rupiah_short(case["revenue_curr"]),
        percent(case["revenue_growth"])
    )

    st.metric(
        "Payment",
        rupiah_short(case["payment_curr"]),
        percent(case["payment_growth"])
    )


# =========================================================
# SIGNALS
# =========================================================

st.subheader("What triggered the score?")

triggered = False


if (
    case["revenue_growth"] >= 0.20
    and case["payment_growth"] < 0
):
    st.warning(
        "＋35 · Opposite movement — revenue increased by at least "
        "20% while payment decreased."
    )
    triggered = True


if case["payment_ratio_change"] <= -0.01:
    st.warning(
        "＋25 · Ratio decline — the payment-to-revenue ratio "
        "declined by at least 1 percentage point."
    )
    triggered = True


if case["late_filings"] == 1:
    st.warning(
        "＋10 · One late filing recorded in the synthetic dataset."
    )
    triggered = True

elif case["late_filings"] >= 2:
    st.warning(
        f"＋20 · Repeated late filing — {int(case['late_filings'])} "
        "late filings recorded."
    )
    triggered = True


if case["revenue_growth"] >= 0.40:
    st.warning(
        "＋20 · Large revenue movement — revenue increased "
        "by at least 40%."
    )
    triggered = True


if not triggered:
    st.success(
        "No scoring rule was triggered for this synthetic record."
    )


# =========================================================
# INTERPRETATION
# =========================================================

st.subheader("How to interpret this")

if str(case["priority"]) == "HIGH":
    st.info(
        "HIGH means this record triggered enough weighted signals "
        "to appear near the top of the review queue. It does not mean "
        "that non-compliance has been established."
    )

elif str(case["priority"]) == "MEDIUM":
    st.info(
        "MEDIUM means some review signals were detected, but the "
        "combined score is below the high-priority threshold."
    )

else:
    st.info(
        "LOW means few or no rules were triggered under this "
        "synthetic scoring framework."
    )


# =========================================================
# EXPORT
# =========================================================

st.divider()

label("Export")
st.header("Take the scored dataset.")

export_df = scored_df.copy()

export_csv = export_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download scored synthetic data",
    export_csv,
    "scored_synthetic_tax_data.csv",
    "text/csv",
)


# =========================================================
# METHODOLOGY
# =========================================================

st.divider()

label("Methodology note")
st.header("Why rule-based instead of machine learning?")

st.write(
    """
This project intentionally uses rule-based weighted scoring rather
than a predictive machine-learning model.

The synthetic dataset does not contain validated ground-truth labels
for taxpayer risk or non-compliance. Training a supervised model on
artificially assigned labels would therefore create an appearance of
predictive accuracy without a defensible target variable.

Rule-based scoring is more appropriate for this demonstration because
the assumptions remain visible, auditable, and explainable.
"""
)

st.warning(
    "The resulting risk score is a point score, not a probability "
    "of non-compliance."
)


st.divider()

label("Rizqi Aprilianes · Data Analytics / Risk Prioritization")
st.caption(
    "Synthetic educational reconstruction · "
    "Not an official tax administration system"
)
