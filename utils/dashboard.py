import pandas as pd


def find_column(df: pd.DataFrame, possible_names: list[str]) -> str | None:
    normalized_columns = {
        str(column).strip().lower().replace(" ", "_"): column
        for column in df.columns
    }

    for name in possible_names:
        normalized_name = name.strip().lower().replace(" ", "_")

        if normalized_name in normalized_columns:
            return normalized_columns[normalized_name]

    return None


def get_dashboard_metrics(df: pd.DataFrame) -> dict:
    active_column = find_column(
        df,
        [
            "active_users",
            "active_user",
            "active",
        ],
    )

    churn_column = find_column(
        df,
        [
            "churn_users",
            "churn_user",
            "churn",
        ],
    )

    new_column = find_column(
        df,
        [
            "new_users",
            "new_user",
            "new",
        ],
    )

    inactive_column = find_column(
        df,
        [
            "inactive_users",
            "inactive_user",
            "inactive",
        ],
    )

    metrics = {
        "total_active": None,
        "total_churn": None,
        "total_new": None,
        "total_inactive": None,
        "churn_rate": None,
    }

    if active_column is not None:
        metrics["total_active"] = float(
            pd.to_numeric(
                df[active_column],
                errors="coerce",
            ).sum()
        )

    if churn_column is not None:
        metrics["total_churn"] = float(
            pd.to_numeric(
                df[churn_column],
                errors="coerce",
            ).sum()
        )

    if new_column is not None:
        metrics["total_new"] = float(
            pd.to_numeric(
                df[new_column],
                errors="coerce",
            ).sum()
        )

    if inactive_column is not None:
        metrics["total_inactive"] = float(
            pd.to_numeric(
                df[inactive_column],
                errors="coerce",
            ).sum()
        )

    if (
        metrics["total_active"] is not None
        and metrics["total_churn"] is not None
    ):
        total_users = (
            metrics["total_active"]
            + metrics["total_churn"]
        )

        if total_users > 0:
            metrics["churn_rate"] = (
                metrics["total_churn"]
                / total_users
            ) * 100

    return metrics