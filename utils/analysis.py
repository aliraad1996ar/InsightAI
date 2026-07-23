import pandas as pd


def analyze_by(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    analysis = (
        df.groupby(group_column, dropna=False)
        .agg(
            Active_Users=("Active_Users", "sum"),
            Inactive_Users=("Inactive_Users", "sum"),
            Churn_Users=("Churn_Users", "sum"),
            New_Users=("New_Users", "sum"),
        )
        .reset_index()
    )

    total_users = (
        analysis["Active_Users"]
        + analysis["Inactive_Users"]
        + analysis["Churn_Users"]
    )

    analysis["Churn_Rate"] = (
        analysis["Churn_Users"]
        / total_users.replace(0, pd.NA)
        * 100
    )

    return analysis