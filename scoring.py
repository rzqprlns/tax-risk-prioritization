import pandas as pd
import numpy as np


def calculate_features(df):
    """
    Create analytical features from the raw synthetic dataset.
    """

    data = df.copy()

    # 1. Revenue growth
    data["revenue_growth"] = (
        (data["revenue_curr"] - data["revenue_prev"])
        / data["revenue_prev"]
    )

    # 2. Payment growth
    data["payment_growth"] = (
        (data["payment_curr"] - data["payment_prev"])
        / data["payment_prev"]
    )

    # 3. Payment-to-revenue ratio for each period
    data["payment_ratio_prev"] = (
        data["payment_prev"] / data["revenue_prev"]
    )

    data["payment_ratio_curr"] = (
        data["payment_curr"] / data["revenue_curr"]
    )

    # 4. Change in payment-to-revenue ratio
    data["payment_ratio_change"] = (
        data["payment_ratio_curr"]
        - data["payment_ratio_prev"]
    )

    return data


def calculate_risk_score(df):
    """
    Apply transparent heuristic rules.

    IMPORTANT:
    These rules and weights are created solely for this synthetic
    portfolio project. They are NOT official DJP methodology.
    """

    data = calculate_features(df)

    data["risk_score"] = 0

    # ---------------------------------------------------------
    # RULE 1 — Opposite movement
    # Revenue grows >= 20%, while payment decreases.
    # Weight: 35 points
    # ---------------------------------------------------------

    rule_1 = (
        (data["revenue_growth"] >= 0.20)
        & (data["payment_growth"] < 0)
    )

    data.loc[rule_1, "risk_score"] += 35


    # ---------------------------------------------------------
    # RULE 2 — Material payment-ratio decline
    # Payment/revenue ratio falls by >= 1 percentage point.
    # Weight: 25 points
    # ---------------------------------------------------------

    rule_2 = (
        data["payment_ratio_change"] <= -0.01
    )

    data.loc[rule_2, "risk_score"] += 25


    # ---------------------------------------------------------
    # RULE 3 — Repeated late filing
    #
    # 1 late filing  = 10 points
    # >= 2 filings   = 20 points
    # ---------------------------------------------------------

    data.loc[
        data["late_filings"] == 1,
        "risk_score"
    ] += 10

    data.loc[
        data["late_filings"] >= 2,
        "risk_score"
    ] += 20


    # ---------------------------------------------------------
    # RULE 4 — Very large revenue growth
    # Revenue increases >= 40%.
    # Weight: 20 points
    # ---------------------------------------------------------

    rule_4 = (
        data["revenue_growth"] >= 0.40
    )

    data.loc[rule_4, "risk_score"] += 20


    # Keep score between 0 and 100
    data["risk_score"] = data["risk_score"].clip(
        lower=0,
        upper=100
    )


    # ---------------------------------------------------------
    # PRIORITY CLASSIFICATION
    # ---------------------------------------------------------

    data["priority"] = pd.cut(
        data["risk_score"],
        bins=[-1, 39, 69, 100],
        labels=["LOW", "MEDIUM", "HIGH"]
    )


    # ---------------------------------------------------------
    # EXPLANATION
    # ---------------------------------------------------------

    explanations = []

    for _, row in data.iterrows():

        reasons = []

        if (
            row["revenue_growth"] >= 0.20
            and row["payment_growth"] < 0
        ):
            reasons.append(
                "Revenue increased while payment decreased (+35)"
            )

        if row["payment_ratio_change"] <= -0.01:
            reasons.append(
                "Payment-to-revenue ratio declined (+25)"
            )

        if row["late_filings"] == 1:
            reasons.append(
                "One late filing (+10)"
            )

        elif row["late_filings"] >= 2:
            reasons.append(
                "Repeated late filings (+20)"
            )

        if row["revenue_growth"] >= 0.40:
            reasons.append(
                "Revenue increased by at least 40% (+20)"
            )

        if not reasons:
            reasons.append(
                "No risk rule triggered"
            )

        explanations.append(
            " | ".join(reasons)
        )

    data["score_explanation"] = explanations

    return data
