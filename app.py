import streamlit as st
import pandas as pd
import sqlite3

# Function to collect user information
def collect_user_info():
    Name = st.text_input("Enter your name:")
    Contact = st.text_input("Enter your contact:")
    Insured_Name = st.text_input("Enter your insured name:")
    Total_Sum_Insured = st.number_input("Enter your sum insured:", step=1)
    Risk_Location = st.text_input("Enter your risk location:")
    return Name, Contact, Insured_Name, Total_Sum_Insured, Risk_Location

# Function to load pincode and zone information from Excel sheet
def load_pincode_zone_data(file_path):
    df = pd.read_excel(file_path)  # Assuming the Excel file contains two columns: 'Pincode' and 'Zone'
    pincode_zone_map = dict(zip(df['Pin_code'], df['txt_eq_zone']))
    return pincode_zone_map

# Function to calculate insurance premium based on user input
def calculate_premium(Total_Sum_Insured, zone):
    # Your calculation logic here based on Total_Sum_Insured, zone, and other factors
    # For demonstration, let's just return a placeholder value
    Flexa = 0.98
    STFI = 0.35
    Terrorism = st.number_input("Enter the terrorism rate:", step=0.01)
    Zone_Rates = {"IV": 0.05, "III": 0.1, "II": 0.25, "I": 0.5}
    if zone in Zone_Rates:
        EQ_Rate = Zone_Rates[zone]
        final_rate = Flexa + EQ_Rate + STFI + Terrorism
        Net_Premium = Total_Sum_Insured * final_rate / 1000
        GST = Net_Premium * 18 / 100
        Total_Premium = Net_Premium + GST
    return Total_Premium

# Main function to run the calculator
def main():

    #Title
    st.title("Insurance Premium Calculator")

    # Load pincode and zone information
    pincode_zone_map = load_pincode_zone_data('pincode_zone_data.xlsx')  # Update with your file path

    # Collect user information
    Name, Contact, Insured_Name, Total_Sum_Insured, Risk_Location = collect_user_info()

    # Get user input for pincode
    pincode = st.text_input("Enter your pincode:")
    zone = pincode_zone_map.get(int(pincode), "Unknown")

    # Calculate insurance premium
    premium = calculate_premium(Total_Sum_Insured, zone)

    # Display results
    st.write(f"Hi {Name}, based on your pincode {pincode} in zone {zone}, your insurance premium is: {premium}")

    # Store Contact Information in Database
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_info
                 (name TEXT, contact TEXT, sum_insured REAL, risk_location TEXT, pincode TEXT, premium REAL)''')
    c.execute("INSERT INTO user_info VALUES (?, ?, ?, ?, ?, ?)", (Name, Contact, Total_Sum_Insured, Risk_Location, pincode, premium))
    conn.commit()
    conn.close()

# Run the main function
if __name__ == "__main__":
    main()
