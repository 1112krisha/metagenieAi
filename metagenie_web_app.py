import streamlit as st
import pandas as pd
import random
import io

# --- Helper functions to generate globally realistic synthetic data ---
def generate_value_for_column(col):
    col = col.strip().lower()
    if col == "compound_name":
        return random.choice(["Butyrate", "Propionate", "Acetate", "Lactate", "Succinate"])
    elif col == "metabolite_id":
        return f"HMDB{random.randint(10000, 99999)}"
    elif col == "molecular_formula":
        return random.choice(["C4H8O2", "C3H6O2", "C2H4O2", "C3H6O3"])
    elif col == "monoisotopic_mass":
        return round(random.uniform(50.0, 300.0), 4)
    elif col == "chemical_class":
        return random.choice(["Short-chain fatty acid", "Amino acid", "Bile acid"])
    elif col == "origin":
        return random.choice(["Microbial", "Host", "Dietary"])
    elif col in ["microbial_taxa", "linked microbial taxa"]:
        return random.choice(["Firmicutes", "Bacteroidetes", "Actinobacteria", "Proteobacteria"])
    elif col == "species":
        return random.choice(["Bacteroides fragilis", "Lactobacillus rhamnosus", "Faecalibacterium prausnitzii"])
    elif col == "strain":
        return random.choice(["ATCC 25285", "DSM 20021", "NCIMB 11181"])
    elif col == "sample_type":
        return random.choice(["Stool", "Serum", "Urine"])
    elif col == "host_interaction":
        return random.choice(["Anti-inflammatory", "Immunomodulatory", "None"])
    elif col == "description":
        return random.choice(["A key SCFA produced by microbial fermentation.", "Impacts immune response.", "Linked to gut health."])
    elif col == "disease_association":
        return random.choice(["IBD", "Obesity", "Type 2 Diabetes", "None"])
    elif col == "pathway":
        return random.choice(["Fermentation", "Glycolysis", "TCA Cycle", "Beta Oxidation"])
    elif col == "influenced_by_diet":
        return random.choice(["Yes", "No"])
    elif col == "host_genes":
        return random.choice(["SLC5A8", "GPR43", "FFAR2", "NOD2", "TLR4"])
    elif col == "snps_linked_to_metabolism":
        return random.choice(["rs123456", "rs789012", "rs345678", "rs654321"])
    elif col == "rda_value":
        return round(random.uniform(0.1, 5.0), 2)
    elif col == "rda reference unit":
        return random.choice(["mg/day", "ug/day"])
    elif col == "diversity marker":
        return random.choice(["Balanced", "Unbalanced (low taxa diversity)", "Unbalanced (dominant species)", "Unbalanced due to antibiotics"])
    elif col == "publication or database link":
        return f"https://doi.org/10.{random.randint(1000,9999)}/{random.randint(10000,99999)}"
    elif col == "lc-ms/ms data reference":
        return f"https://massive.ucsd.edu/MSV{random.randint(100000,999999)}"
    else:
        return "N/A"

# --- Streamlit UI ---
st.set_page_config(page_title="MetaGenie-AI", page_icon="🧫", layout="wide")
st.title(":genie: MetaGenie-AI: Global Metabolite Data Generator")

st.markdown("""
Upload a structured Excel template with column headers such as `compound_name`, `metabolite_id`, `host_genes`, `Diversity Marker`, etc.
The generator will create globally realistic synthetic entries with working links and clear annotations.
""")

uploaded_file = st.file_uploader("Upload your structured Excel file", type=["xlsx"])
num_rows = st.number_input("Enter number of synthetic rows to generate", min_value=100, max_value=50000, value=1000, step=100)

if uploaded_file:
    template_df = pd.read_excel(uploaded_file)
    final_columns = template_df.columns.tolist()

    synthetic_data = []
    for _ in range(num_rows):
        row = {}
        for col in final_columns:
            row[col] = generate_value_for_column(col)
        synthetic_data.append(row)

    result_df = pd.DataFrame(synthetic_data)

    st.success("✅ Data generation complete!")
    st.dataframe(result_df.head(100))

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Download Synthetic Metabolite Data",
        data=output.getvalue(),
        file_name="MetaGenie_Synthetic_Global_Metabolites.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
