import streamlit as st
import pandas as pd
import sqlite3
from email.utils import parseaddr


# Function to collect user information
def collect_user_info():
    Insured_Name = st.text_input("Enter your insured name:")
    Total_Sum_Insured = st.number_input("Enter your sum insured:", step=1)
    Risk_Location = st.text_input("Enter your risk location:")
    return Insured_Name, Total_Sum_Insured, Risk_Location


# Function to load pincode and zone information from Excel sheet
def load_pincode_zone_data(file_path):
    df = pd.read_excel(file_path)  # Assuming the Excel file contains two columns: 'Pincode' and 'Zone'
    pincode_zone_map = dict(zip(df['Pin_code'], df['txt_eq_zone']))
    return pincode_zone_map


# Function to calculate insurance premium based on user input
def calculate_premium(Total_Sum_Insured, zone, business_type):
    # Your calculation logic here based on Total_Sum_Insured, zone, and other factors
    # For demonstration, let's just return a placeholder value
    Flexa = 0.98
    STFI = 0.35
    Terrorism = st.number_input("Enter the terrorism rate:", step=0.01)
    Zone_Rates = {"IV": 0.05, "III": 0.1, "II": 0.25, "I": 0.5}

    if zone in Zone_Rates:
        EQ_Rate = Zone_Rates[zone]
        if business_type == "BSUS":
            final_rate = Flexa + EQ_Rate + STFI + Terrorism
            Net_Premium = Total_Sum_Insured * final_rate / 1000
            GST = Net_Premium * 18 / 100
            Total_Premium = Net_Premium + GST

        elif business_type == "MSME":
            final_rate = (Flexa + EQ_Rate + STFI) + 0.1
            Net_Premium = Total_Sum_Insured * final_rate / 1000
            GST = Net_Premium * 18 / 100
            Total_Premium = Net_Premium + GST

    return Total_Premium


# Main function to run the calculator
def main():
    # Title
    st.title("Insurance Premium Calculator")

    # Load pincode and zone information
    pincode_zone_map = load_pincode_zone_data('pincode_zone_data.xlsx')  # Update with your file path

    # Collect user information
    Insured_Name, Total_Sum_Insured, Risk_Location = collect_user_info()

    # Get user input for pincode
    pincode = st.text_input("Enter your pincode:")

    # Check if pincode is empty or not a valid integer
    if pincode.strip() == '' or not pincode.isdigit():
        st.error("Please enter a valid pincode.")
        return

    zone = pincode_zone_map.get(int(pincode), "Unknown")

    # Dropdown for business type
    business_type = st.selectbox("Select Business Type:", ["BSUS", "MSME"])

    # Email input for submission
    email = st.text_input("Enter your email (mandatory for accessing the calculated value):")

    # Store Contact Information in Database
    if st.button("Submit"):
        if email == "":
            st.error("Please enter your email to access the calculated value.")
            return
        _, email_address = parseaddr(email)
        if not email_address or "@" not in email_address:
            st.error("Please enter a valid email address.")
            return

        # Calculate insurance premium
        premium = calculate_premium(Total_Sum_Insured, zone, business_type)

        # Display results
        st.write(
            f"Based on your pincode {pincode} in zone {zone}, your insurance premium for {business_type} is: {premium}")

        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_info
                     (insured_name TEXT, sum_insured REAL, risk_location TEXT, pincode TEXT, business_type TEXT, premium REAL, email TEXT)''')
        c.execute("INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (Insured_Name, Total_Sum_Insured, Risk_Location, pincode, business_type, premium, email))
        conn.commit()
        conn.close()
        st.success("Data successfully submitted!")


# Run the main function
if __name__ == "__main__":
    main()
