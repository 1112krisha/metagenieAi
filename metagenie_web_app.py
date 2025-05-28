import streamlit as st
import pandas as pd
import random
import io

# Reference values
chemical_classes = ["SCFA", "Amino Acid", "Bile Acid", "Lipid", "Sugar", "Vitamin", "Alkaloid"]
origins = ["Microbial", "Host", "Mixed"]
sample_types = ["Stool", "Plasma", "Urine", "Saliva"]
diets = ["Fiber-rich", "Ketogenic", "High-Protein", "Vegan", "Western"]
gene_pool = ["SLC5A8", "MCT1", "GPR41", "GPR43", "PCK1", "PPARα"]
pathways = ["Butanoate metabolism", "TCA Cycle", "Glycolysis", "Urea Cycle", "Fatty Acid Synthesis"]
diseases = ["IBS", "Ulcerative Colitis", "Type 2 Diabetes", "Obesity", "Crohn's Disease"]
diversity_markers = ["Rich", "Even", "Poor", "Unbalanced"]

# Generator function for one row
def generate_metabolite_row():
    name = f"Metabolite-{random.randint(1000, 9999)}"
    uid = f"HMDB{random.randint(1000000, 9999999)}"
    formula = f"C{random.randint(1, 20)}H{random.randint(2, 40)}O{random.randint(0, 10)}"
    mass = round(random.uniform(50.0, 800.0), 4)
    chem_class = random.choice(chemical_classes)
    origin = random.choice(origins)
    taxa = random.choice(["Faecalibacterium", "Bacteroides", "Lactobacillus", "E. coli", "Clostridium"])
    source = random.choice(sample_types)
    interaction = random.choice(["Digestive Efficiency", "Inflammation Marker", "Immune Modulator"])
    desc = f"A key {origin.lower()} metabolite involved in {random.choice(pathways)}."
    disease = random.choice(diseases)
    pathway = random.choice(pathways)
    diet = random.choice(diets)
    gene = random.choice(gene_pool)
    rda = round(random.uniform(0.1, 100.0), 2)
    rda_unit = random.choice(["µmol/L", "mg/L", "µg/mL"])
    reference = f"https://hmdb.ca/metabolites/{uid}"
    ms_data = f"MS_MS_Ref_{random.randint(1000,9999)}"

    return {
        "Common name": name,
        "Unique ID (HMDB, KEGG, etc.)": uid,
        "Chemical formula": formula,
        "Accurate mass": mass,
        "Metabolite family": chem_class,
        "Microbial / Host / Mixed": origin,
        "Linked microbial taxa": taxa,
        "Biological source": source,
        "Microbial Diversity Marker": random.choice(diversity_markers),
        "Indicates the richness and evenness of microbial species in the gut": desc,
        "Associated diseases": disease,
        "Biological pathway": pathway,
        "Diet sensitivity (e.g., fiber-rich, ketogenic)": diet,
        "Host genes/SNPs linked to metabolism": gene,
        "Recommended daily allowance value": rda,
        "rda_unit": rda_unit,
        "Publication or database link": reference,
        "LC-MS/MS data reference": ms_data,
    }

# Streamlit App
st.set_page_config(page_title="MetaGenie-AI", page_icon="🧬", layout="centered")
st.title("🧬 MetaGenie-AI: Global Metabolomics Data Generator")
st.markdown("Generate unlimited globally realistic metabolite reference data for gut-health research.")

num_rows = st.slider("Select number of rows to generate", min_value=10, max_value=1000, value=100)

if st.button("Generate Data"):
    generated_data = [generate_metabolite_row() for _ in range(num_rows)]
    df_result = pd.DataFrame(generated_data)
    
    st.success("✅ Synthetic data generated successfully!")
    st.dataframe(df_result)

    # Download button
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_result.to_excel(writer, index=False)
    st.download_button("Download Excel", data=output.getvalue(),
                       file_name="Global_Metabolite_Data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
