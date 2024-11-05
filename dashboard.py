import streamlit as st
import pandas as pd

# Load the cleaned data from the CSV file
csv_file_path = "company_energy_data_with_urls.csv"  # Path to the cleaned file
df = pd.read_csv(csv_file_path)

# Set up the Streamlit dashboard
st.title("Renewable Energy Buyers - India 1000 NSE")

# Sidebar for filtering options
st.sidebar.title("Filter Options")

# Search by company name
company_name = st.sidebar.text_input("Search by Company Name")
if company_name:
    df = df[df["File Name"].str.contains(company_name, case=False, na=False)]

# Filter by energy attributes
st.sidebar.write("### Filter by Energy Attributes")

# Add sliders for numerical filtering
if not df["Total Electricity Consumption (A)"].isnull().all():
    electricity_min, electricity_max = st.sidebar.slider(
        "Total Electricity Consumption (A)",
        float(df["Total Electricity Consumption (A)"].min()),
        float(df["Total Electricity Consumption (A)"].max()),
        (float(df["Total Electricity Consumption (A)"].min()), float(df["Total Electricity Consumption (A)"].max()))
    )
    df = df[(df["Total Electricity Consumption (A)"] >= electricity_min) & (df["Total Electricity Consumption (A)"] <= electricity_max)]

if not df["Total Fuel Consumption (B)"].isnull().all():
    fuel_min, fuel_max = st.sidebar.slider(
        "Total Fuel Consumption (B)",
        float(df["Total Fuel Consumption (B)"].min()),
        float(df["Total Fuel Consumption (B)"].max()),
        (float(df["Total Fuel Consumption (B)"].min()), float(df["Total Fuel Consumption (B)"].max()))
    )
    df = df[(df["Total Fuel Consumption (B)"] >= fuel_min) & (df["Total Fuel Consumption (B)"] <= fuel_max)]

if not df["Energy Intensity"].isnull().all():
    intensity_min, intensity_max = st.sidebar.slider(
        "Energy Intensity",
        float(df["Energy Intensity"].min()),
        float(df["Energy Intensity"].max()),
        (float(df["Energy Intensity"].min()), float(df["Energy Intensity"].max()))
    )
    df = df[(df["Energy Intensity"] >= intensity_min) & (df["Energy Intensity"] <= intensity_max)]

# Display filtered data with URL link
st.write("## Dataset")

# Check if ATTACHMENT column exists before attempting to display it as a link
if 'ATTACHMENT' in df.columns:
    # Create a copy of the DataFrame to modify the URL display
    df_display = df.copy()
    # Convert the ATTACHMENT column to clickable links
    df_display['Company Report URL'] = df_display['ATTACHMENT'].apply(lambda x: f"[Link]({x})" if pd.notnull(x) else "No URL")
    # Reorder columns to display File Name and URL first
    cols = ['File Name', 'Company Report URL'] + [col for col in df_display.columns if col not in ['File Name', 'Company Report URL', 'ATTACHMENT']]
    st.write(df_display[cols].to_markdown(index=False), unsafe_allow_html=True)
else:
    st.write("ATTACHMENT column with URLs is not available in the dataset.")

# Option to download filtered data
st.write("### Download Filtered Data")
filtered_csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=filtered_csv,
    file_name="filtered_company_energy_data.csv",
    mime="text/csv",
)

# Add a reset button to clear filters
if st.sidebar.button("Reset Filters"):
    # Clear all session states for filter keys
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()  # Rerun the app to reset filters
