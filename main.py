import streamlit as st
import pandas as pd
from component import page_style
from backend import sanitize_phone_numbers

page_style()

st.title("Phone Number Auditor 📞")

# Initialize session state variables
if 'df_original' not in st.session_state:
    st.session_state['df_original'] = None
if 'df_sanitized' not in st.session_state:
    st.session_state['df_sanitized'] = None
if 'df_deduped' not in st.session_state:
    st.session_state['df_deduped'] = None

# Step 1: Upload CSV files
uploaded_files = st.file_uploader("Upload CSV files containing phone numbers", accept_multiple_files=True, type=["csv"])

if uploaded_files:
    # Read the uploaded CSV files and concatenate them into a single DataFrame
    dataframes = []
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        dataframes.append(df)

    # Concatenate all DataFrames into one
    df = pd.concat(dataframes, ignore_index=True)

    if 'phonenum' in df.columns:
        st.success("Files uploaded successfully!")

        # Store the original DataFrame in session state
        st.session_state['df_original'] = df

        # Display the initial DataFrame
        st.subheader("Initial DataFrame")
        st.write(st.session_state['df_original'])

        # Step 2: Audit Button
        if st.button("Sanitize Phone Numbers"):
            # Apply the sanitize_phone_numbers function to the DataFrame
            st.session_state['df_sanitized'] = sanitize_phone_numbers(st.session_state['df_original'])
            st.subheader("Sanitized Phone Numbers")
            st.write(st.session_state['df_sanitized'])

        # Step 3: Drop Duplicates Button
        if st.button("Drop Duplicates"):
            initial_count = len(st.session_state['df_sanitized']) if st.session_state['df_sanitized'] is not None else 0
            st.session_state['df_deduped'] = st.session_state['df_sanitized'].drop_duplicates(subset=['phonenum'])
            after_count = len(st.session_state['df_deduped'])

            st.write(f"Count of phone numbers before deduplication: {initial_count}")
            st.write(f"Count of phone numbers after deduplication: {after_count}")

        # Step 4: Last Audit Button
        if st.button("Last Audit (9 to 13 characters)"):
            df_deduped = st.session_state['df_deduped']

            if df_deduped is not None:  # Ensure df_deduped is defined
                last_audit_df = df_deduped[df_deduped['phonenum'].astype(str).str.len().between(9, 13)]

                # Check if any phone numbers were found
                if last_audit_df.empty:
                    st.warning("No phone numbers found with lengths between 9 and 13 characters.")
                else:
                    # Group by the length of the phone numbers
                    last_audit_grouped = last_audit_df.groupby(last_audit_df['phonenum'].astype(str).str.len()).phonenum.apply(list).reset_index(name='phonenumber_character_len')

                    st.subheader("Last Audit Result (9 to 13 characters)")
                    st.write(last_audit_grouped)
            else:
                st.warning("Please sanitize or drop duplicates first.")

        # Step 5: Download Button
        if st.session_state['df_deduped'] is not None:  # Check if df_deduped exists to prevent errors
            csv = st.session_state['df_deduped'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Sanitized DataFrame",
                data=csv,
                file_name="sanitized_phone_numbers.csv",
                mime="text/csv"
            )
    else:
        st.error("The uploaded CSV files must contain a 'phonenum' column.")
else:
    st.info("Please upload CSV files to get started.")
