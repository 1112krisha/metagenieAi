import streamlit as st
import pandas as pd
import random
import io

# Data generators for each column
def generate_data_for_column(col):
    if col == "age":
        return random.randint(18, 90)
    elif col == "gender":
        return random.choice(["Male", "Female"])
    elif col == "BMI":
        return round(random.uniform(18.5, 40.0), 1)
    elif col == "glucose_level":
        return random.randint(70, 200)
    elif col == "insulin":
        return round(random.uniform(2.0, 25.0), 2)
    elif col == "blood_pressure":
        return random.randint(90, 180)
    elif col == "cholesterol":
        return random.randint(150, 300)
    elif col == "metabolic_rate":
        return round(random.uniform(1200, 2500), 2)
    else:
        return "N/A"

# Generate target column values
def generate_target(row, target):
    if target == "diabetic_status":
        return "Diabetic" if row.get("glucose_level", 0) >= 126 else "Non-Diabetic"
    elif target == "risk_level":
        if row.get("BMI", 0) > 30 or row.get("blood_pressure", 0) > 140:
            return "High"
        else:
            return "Normal"
    else:
        return "Unknown"

# Streamlit App
st.set_page_config(page_title="MetaGenie-AI", page_icon="🧞", layout="centered")
st.title("🧞 MetaGenie-AI: Metabolics Data Generator")
st.markdown("""
Upload a blank Excel file with column names. The last column should be your target (e.g., `diabetic_status`).
MetaGenie will fill in realistic synthetic data for you.
""")

uploaded_file = st.file_uploader("Upload your blank Excel file", type=["xlsx"])
num_rows = st.slider("Select number of rows to generate", min_value=10, max_value=500, value=100)

if uploaded_file:
    df_template = pd.read_excel(uploaded_file)
    column_names = df_template.columns.tolist()

    if len(column_names) < 2:
        st.error("Please include at least one feature column and one target column.")
    else:
        target_col = column_names[-1]
        data = []
        for _ in range(num_rows):
            row = {}
            for col in column_names:
                if col != target_col:
                    row[col] = generate_data_for_column(col)
            row[target_col] = generate_target(row, target_col)
            data.append(row)

        df_result = pd.DataFrame(data)
        st.success("✅ Data generation complete!")
        st.dataframe(df_result)

        # Download button
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_result.to_excel(writer, index=False)
        st.download_button("Download Filled Excel", data=output.getvalue(), file_name="MetaGenie_Filled.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
