# Import necessary libraries
import streamlit as st
import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('vehicle_info.db')
c = conn.cursor()

# Create a table to store vehicle information if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY,
        vehicle_name TEXT,
        vehicle_no TEXT,
        vehicle_info TEXT,
        fault TEXT,
        date TEXT,
        price REAL
    )
''')
conn.commit()

# Define the Streamlit app
def main():
    # Set app title and background color
    st.markdown("<h1 style='text-align: center; color: #009688;'>Apna Pela App</h1>", unsafe_allow_html=True)
    st.markdown("<style>body {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)

    # Sidebar for user input with a background color
    st.sidebar.markdown("<h3 style='color: #009688;'>Add Vehicle</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border: 2px solid #009688;'>", unsafe_allow_html=True)
    
    # User input fields with styling
    vehicle_name = st.sidebar.text_input("Vehicle Name", help="Enter vehicle name")
    vehicle_no = st.sidebar.text_input("Vehicle Number", help="Enter vehicle number")
    vehicle_info = st.sidebar.text_area("Vehicle Information", help="Enter vehicle information")
    fault = st.sidebar.text_input("Vehicle Fault", help="Enter fault")
    date = st.sidebar.text_input("Date", help="Enter date")
    price = st.sidebar.number_input("Price")

    if st.sidebar.button("Add Vehicle"):
        c.execute("INSERT INTO vehicles (vehicle_name, vehicle_no, vehicle_info, fault, date, price) VALUES (?, ?, ?, ?, ?, ?)",
                  (vehicle_name, vehicle_no, vehicle_info, fault, date, price))
        conn.commit()
        st.sidebar.success("Vehicle added successfully!")

    # Search and display vehicles
    st.header("Search and Display Vehicles")
    
    # Search input field with styling
    search_term = st.text_input("Search by Vehicle Name or Vehicle Number", help="Enter search term")
    
    if st.button("Search"):
        c.execute("SELECT * FROM vehicles WHERE vehicle_name LIKE ? OR vehicle_no LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        data = c.fetchall()
        if data:
            st.table(data)
        else:
            st.warning("No matching records found.")

    # Display the top 10 records
    st.header("Top 10 Vehicle Records")
    c.execute("SELECT * FROM vehicles LIMIT 10")
    top_records = c.fetchall()
    st.table(top_records)

    # Delete button with styling
    st.header("Delete Vehicle Record")
    delete_id = st.number_input("Enter ID of the record to delete", help="Enter ID")
    if st.button("Delete"):
        c.execute("DELETE FROM vehicles WHERE id=?", (delete_id,))
        conn.commit()
        st.success(f"Record with ID {delete_id} deleted successfully!")

    # Clear button to remove unnecessary data
    if st.button("Clear All Data"):
        c.execute("DELETE FROM vehicles")
        conn.commit()
        st.warning("All data cleared!")

if __name__ == '__main__':
    main()
