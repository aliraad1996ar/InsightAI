import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="InsightAI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 InsightAI")
st.write("Upload an Excel file to explore and analyze your data.")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Dataset Information")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isnull().sum().sum()))
        col4.metric("Duplicate Rows", int(df.duplicated().sum()))

        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        

        st.subheader("Numeric Summary")

        if numeric_columns:
            st.dataframe(
                df[numeric_columns].describe().transpose(),
                use_container_width=True
            )

            st.subheader("Create a Chart")

            selected_column = st.selectbox(
                "Select a numeric column",
                numeric_columns
            )

            chart_type = st.selectbox(
                "Select chart type",
                ["Line Chart", "Bar Chart", "Histogram"]
            )

            chart_data = df[selected_column].dropna()

            if chart_type == "Line Chart":
                st.line_chart(chart_data)

            elif chart_type == "Bar Chart":
                st.bar_chart(chart_data.head(50))

            elif chart_type == "Histogram":
                figure, axis = plt.subplots()
                axis.hist(chart_data, bins=20)
                axis.set_xlabel(selected_column)
                axis.set_ylabel("Frequency")
                axis.set_title(f"Distribution of {selected_column}")

                st.pyplot(figure)
                plt.close(figure)

        else:
            st.warning("No numeric columns were found in this file.")

        st.subheader("Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns.astype(str),
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(column_info, use_container_width=True)

    except Exception as error:
        st.error(f"Could not read the excel file:{error}")