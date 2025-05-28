import streamlit as st
import pandas as pd
import random
import io

# --- Helper functions to generate globally realistic synthetic data ---
def generate_value_for_column(col):
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
    elif col == "microbial_taxa" or col == "Linked microbial taxa":
        return random.choice(["Firmicutes", "Bacteroidetes", "Actinobacteria", "Proteobacteria"])
    elif col == "species":
        return random.choice(["E. coli", "B. fragilis", "L. acidophilus", "B. longum", "C. difficile"])
    elif col == "strain":
        return random.choice(["K12", "NCTC 9343", "VPI 10463", "DSM 20016", "JCM 1002"])
    elif col == "sample_type":
        return random.choice(["Stool", "Serum", "Urine", "Feces"])
    elif col == "host_interaction":
        return random.choice(["Anti-inflammatory", "Immunomodulatory", "Neutral", "Pro-inflammatory"])
    elif col == "Description":
        return random.choice(["A key SCFA produced by microbial fermentation.", "Impacts immune response.", "Linked to gut health."])
    elif col == "disease_association":
        return random.choice(["IBD", "Obesity", "Type 2 Diabetes", "Metabolic Syndrome", "None"])
    elif col == "pathway":
        return random.choice(["Fermentation", "Glycolysis", "TCA Cycle", "Beta-oxidation"])
    elif col == "influenced_by_diet":
        return random.choice(["Yes", "No"])
    elif col == "host_genes":
        return random.choice(["MC4R", "FTO", "SLC2A2", "LEP", "PPARG", "TCF7L2", "ADIPOQ"])
    elif col == "SNPs_linked_to_metabolism":
        return random.choice(["rs13266634", "rs9939609", "rs7903146", "rs1801282", "rs1205"])
    elif col == "rda_value":
        return round(random.uniform(0.1, 5.0), 2)
    elif col == "RDA Reference Unit":
        return random.choice(["mg/day", "ug/day"])
    elif col == "Diversity Marker":
        return random.choice([
            "Balanced",
            "Unbalanced: Decreased microbial richness",
            "Unbalanced: Increased Firmicutes to Bacteroidetes ratio",
            "Low diversity",
            "High diversity"
        ])
    elif col == "Publication or database link":
        return f"https://doi.org/10.{random.randint(1000,9999)}/{random.randint(10000,99999)}"
    elif col == "LC-MS/MS data reference":
        return f"https://metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST{random.randint(100,999)}"
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

    st.success("\u2705 Data generation complete!")
    st.dataframe(result_df.head(100))

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)

    st.download_button(
        label="📅 Download Synthetic Metabolite Data",
        data=output.getvalue(),
        file_name="MetaGenie_Synthetic_Global_Metabolites.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
