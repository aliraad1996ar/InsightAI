import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.summary import get_summary


st.set_page_config(
    page_title="InsightAI",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 InsightAI")
st.write("Upload an Excel file to explore and analyze your data.")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"],
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        st.subheader("Data Preview")
        st.dataframe(
            df,
            width="stretch",
        )

        summary = get_summary(df)

        st.subheader("Dataset Information")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", summary["rows"])
        col2.metric("Columns", summary["columns"])
        col3.metric("Missing Values", summary["missing"])
        col4.metric("Duplicate Rows", summary["duplicates"])

        numeric_columns = (
            df.select_dtypes(include="number")
            .columns
            .tolist()
        )

        categorical_columns = (
            df.select_dtypes(exclude="number")
            .columns
            .tolist()
        )

        st.subheader("Executive Summary")

        summary_col1, summary_col2 = st.columns(2)

        summary_col1.metric(
            "Numeric Columns",
            len(numeric_columns),
        )

        summary_col2.metric(
            "Text / Date Columns",
            len(categorical_columns),
        )

        if numeric_columns:
            left_column, right_column = st.columns(2)

            with left_column:
                st.write("### Top 5 Columns by Average")

                top_average = (
                    df[numeric_columns]
                    .mean()
                    .sort_values(ascending=False)
                    .head(5)
                    .reset_index()
                )

                top_average.columns = [
                    "Column",
                    "Average",
                ]

                st.dataframe(
                    top_average,
                    width="stretch",
                    hide_index=True,
                )

            with right_column:
                st.write("### Top 5 Most Variable Columns")

                top_variation = (
                    df[numeric_columns]
                    .std()
                    .sort_values(ascending=False)
                    .head(5)
                    .reset_index()
                )

                top_variation.columns = [
                    "Column",
                    "Standard Deviation",
                ]

                st.dataframe(
                    top_variation,
                    width="stretch",
                    hide_index=True,
                )

            st.subheader("Numeric Summary")

            numeric_summary = (
                df[numeric_columns]
                .describe()
                .transpose()
            )

            st.dataframe(
                numeric_summary,
                width="stretch",
            )

            st.subheader("Create a Chart")

            selected_column = st.selectbox(
                "Select a numeric column",
                numeric_columns,
            )

            chart_type = st.selectbox(
                "Select chart type",
                [
                    "Line Chart",
                    "Bar Chart",
                    "Histogram",
                ],
            )

            chart_data = df[selected_column].dropna()

            if chart_type == "Line Chart":
                st.line_chart(chart_data)

            elif chart_type == "Bar Chart":
                st.bar_chart(chart_data.head(50))

            elif chart_type == "Histogram":
                figure, axis = plt.subplots()

                axis.hist(
                    chart_data,
                    bins=20,
                )

                axis.set_xlabel(selected_column)
                axis.set_ylabel("Frequency")
                axis.set_title(
                    f"Distribution of {selected_column}"
                )

                st.pyplot(figure)
                plt.close(figure)

        else:
            st.warning(
                "No numeric columns were found in this file."
            )

        st.subheader("Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values,
        })

        st.dataframe(
            column_info,
            width="stretch",
            hide_index=True,
        )

    except Exception as error:
        st.error(
            f"Could not read the Excel file: {error}"
        )