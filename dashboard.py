import streamlit as st
import pandas as pd
import numpy as np

# Load the data from the CSV file
csv_file_path = "company_energy_data.csv"  # Replace with your actual file path
original_df = pd.read_csv(csv_file_path)

# Ensure columns are numeric where necessary, replacing non-numeric values with NaN
for col in ["Total Electricity Consumption (A)", "Total Fuel Consumption (B)", "Energy Intensity"]:
    original_df[col] = pd.to_numeric(original_df[col], errors='coerce')

# Initialize a copy of the DataFrame for manipulation
df = original_df.copy()

# Set up the Streamlit dashboard
st.title("Renewable Energy Buyers - India 1000 NSE")

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Search by company name with partial and case-insensitive matching
company_name = st.sidebar.text_input("Search by Company Name")
if company_name:
    df = df[df["File Name"].str.contains(company_name, case=False, na=False)]

# Function to add sliders, handling cases where the column has NaN or a single unique value
def add_slider(column_name, label):
    min_value = df[column_name].min()
    max_value = df[column_name].max()
    
    # Check for NaN or identical min/max values
    if pd.isna(min_value) or pd.isna(max_value):
        st.sidebar.write(f"{label}: No data available")
        return None, None
    elif min_value == max_value:
        st.sidebar.write(f"{label}: {min_value} (Only one value available)")
        return min_value, max_value
    else:
        return st.sidebar.slider(label, min_value=float(min_value), max_value=float(max_value), value=(float(min_value), float(max_value)))

# Set up sliders with handling for edge cases
electricity_min, electricity_max = add_slider("Total Electricity Consumption (A)", "Total Electricity Consumption (A)")
if electricity_min is not None and electricity_max is not None:
    df = df[(df["Total Electricity Consumption (A)"] >= electricity_min) & (df["Total Electricity Consumption (A)"] <= electricity_max)]

fuel_min, fuel_max = add_slider("Total Fuel Consumption (B)", "Total Fuel Consumption (B)")
if fuel_min is not None and fuel_max is not None:
    df = df[(df["Total Fuel Consumption (B)"] >= fuel_min) & (df["Total Fuel Consumption (B)"] <= fuel_max)]

intensity_min, intensity_max = add_slider("Energy Intensity", "Energy Intensity")
if intensity_min is not None and intensity_max is not None:
    df = df[(df["Energy Intensity"] >= intensity_min) & (df["Energy Intensity"] <= intensity_max)]

# Reset button in the sidebar to clear filters
if st.sidebar.button("Reset Filters"):
    # Reset to original data by rerunning the app
    st.session_state.clear()  # Clear session state to reset all filters
    st.rerun()  # Updated from st.experimental_rerun() to st.rerun()

# Reorder columns to have "File Name" (company) first
if "File Name" in df.columns:
    cols = ["File Name"] + [col for col in df.columns if col != "File Name"]
    df = df[cols]

# Display filtered data
st.write("## Dataset")
st.write(df)

# Option to download filtered data
st.write("### Download Filtered Data")
filtered_csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=filtered_csv,
    file_name="filtered_company_energy_data.csv",
    mime="text/csv",
)
