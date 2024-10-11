import streamlit as st
import pandas as pd
from component import page_style
from backend import sanitize_phone_numbers

page_style()

st.title("Phone Number Auditor 📞")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file containing phone numbers", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    if 'phonenum' in df.columns:
        st.success("File uploaded successfully!")

        # Display the initial DataFrame
        st.subheader("Initial DataFrame")
        st.write(df)

        # Step 2: Audit Button
        if st.button("Audit"):
            df = sanitize_phone_numbers(df)
            st.subheader("Sanitized Phone Numbers")
            st.write(df)

            # Display counts before and after dropping duplicates
            initial_count = len(df)
            df_deduped = df.drop_duplicates(subset=['phonenum'])
            after_count = len(df_deduped)

            st.write(f"Count of phone numbers before deduplication: {initial_count}")
            st.write(f"Count of phone numbers after deduplication: {after_count}")

            # Update the DataFrame to the deduped version
            df = df_deduped

        # Step 3: Drop Duplicates Button
        if st.button("Drop Duplicates"):
            initial_count = len(df)
            df_deduped = df.drop_duplicates(subset=['phonenum'])
            after_count = len(df_deduped)

            st.write(f"Count of phone numbers before deduplication: {initial_count}")
            st.write(f"Count of phone numbers after deduplication: {after_count}")

            # Update the DataFrame to the deduped version
            df = df_deduped

        # Step 4: Last Audit Button
        if st.button("Last Audit (9 to 13 characters)"):
            last_audit_df = df[df['phonenum'].astype(str).str.len().between(9, 13)]
            st.subheader("Last Audit Result (9 to 13 characters)")
            st.write(last_audit_df)

        # Step 5: Download Button
        if st.button("Download Sanitized DataFrame"):
            # Create a CSV from the DataFrame
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="sanitized_phone_numbers.csv",
                mime="text/csv"
            )
    else:
        st.error("The uploaded CSV file must contain a 'phonenum' column.")
else:
    st.info("Please upload a CSV file to get started.")

