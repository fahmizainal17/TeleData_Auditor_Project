def sanitize_phone_numbers(df):
    # Ensure phonenum column is of string type
    df['phonenum'] = df['phonenum'].astype(str)

    # Step 1: Delete blank rows
    df.dropna(subset=['phonenum'], inplace=True)

    # Plus: Remove '+' signs from each row
    df['phonenum'] = df['phonenum'].str.replace('+', '', regex=False)

    # Step 2: Delete whitespace from each row
    df['phonenum'] = df['phonenum'].str.replace(r'\s+', '', regex=True)

    # Step 3: Remove dashes from each row
    df['phonenum'] = df['phonenum'].str.replace('-', '')

    # Step 4 & 5: Ensure numbers are properly formatted
    df['phonenum'] = df['phonenum'].apply(
        lambda x: '+6' + x if x.startswith('0') else '+60' + x if x.startswith('1') else x
    )

    # Filter numbers to ensure they are at least 9 digits long
    df = df[df['phonenum'].apply(lambda x: len(x) >= 9)]

    # Step 6: Remove decimal points from each phone number actually make it to integer rather than float
    df['phonenum'] = df['phonenum'].astype(float).astype(int)

    # Step 7: Randomize the order of rows
    df = df.sample(frac=1).reset_index(drop=True)

    return df
