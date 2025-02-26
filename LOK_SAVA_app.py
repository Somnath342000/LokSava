import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas

# Function to generate the PDF with better table formatting and adjusted margins
def generate_pdf(dataframe, selected_Year, selected_State, selected_PC_Name, selected_Party, selected_Position):
    buffer = BytesIO()

    # Adjust margins (left, right, top, bottom) to reduce space
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10)

    # Create the canvas object for custom header (state, year, etc.)
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add a header with filter info (Year, State, Constituency, Party, Position)
    c.setFont("Helvetica", 12)
    c.drawString(30, 770, f"Election Report for Year: {selected_Year}")
    c.drawString(30, 755, f"State: {selected_State}")
    c.drawString(30, 740, f"Constituency: {selected_PC_Name}")
    c.drawString(30, 725, f"Party: {selected_Party}")
    c.drawString(30, 710, f"Position: {selected_Position}")
    c.setFont("Helvetica", 10)
    c.line(30, 705, 580, 705)  # Horizontal line after the header

    # Table Header
    data = [['Year', 'Candidate Name', 'Party', 'Position', 'Votes Polled', 'Vote %']]  # Table Header

    # Add rows from the dataframe
    for index, row in dataframe.iterrows():
        data.append([row['Year'], row['Candidate'], row['Party'], row['Position'], row['Votes_Polled'], row['Vote %']])

    # Create the table
    table = Table(data)
    
    # Apply table styles (background colors, borders, etc.)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines around all cells
    ]))

    # Build the document with the table
    doc.build([table])

    buffer.seek(0)  # Move to the beginning of the BytesIO buffer
    return buffer

# Header for the Streamlit app
st.header("Lok Sava Election Result Analysis")
st.image('election1.jpg', caption='Welcome to sales dashboard & forcating', use_container_width=True)

# Link to other project
st.write('''My other project link: https://movieexplorationsuggestion-somnath.streamlit.app/''')
st.write('''My Other Projects : Retail Techstore Sales Analysis (Please Go through the link) : https://salesanalytics-somnath-techstore.streamlit.app/''')
st.write('''My other project link  (Bengali Audio Story Dictionary) :  https://bengaliaudiostorysomnathbanerjee.streamlit.app/''')

# Correct Raw URL for the Excel file
LOKSEATS_url = "https://raw.githubusercontent.com/Somnath342000/LokSava/main/ELECT.xlsx"

try:
    # Request the file from GitHub
    response_LOKSEATS = requests.get(LOKSEATS_url)

    if response_LOKSEATS.status_code == 200:
        st.success("File loaded successfully from GitHub")

        # Load the Excel file into a pandas DataFrame
        df_LOKSEATS = pd.read_excel(BytesIO(response_LOKSEATS.content), engine='openpyxl')

        # Ensure the Year column is treated consistently as string
        df_LOKSEATS['Year'] = df_LOKSEATS['Year'].astype(str)

        # Create columns for layout to display filters
        col1, col2, col3 = st.columns([1, 2, 1])  # 2 is the middle column width

        with col2:
            st.header("🔍Search here")
            
            # Create filters
            selected_Year = st.selectbox("Select Year", ["All"] + df_LOKSEATS["Year"].unique().tolist())
            if selected_Year != "All":
                df_filtered = df_LOKSEATS[df_LOKSEATS["Year"] == selected_Year]
            else:
                df_filtered = df_LOKSEATS.copy()  # Include all years if "All" is selected

            selected_State = st.selectbox("Select State", ["All"] + df_filtered["State"].unique().tolist())
            if selected_State != "All":
                df_filtered = df_filtered[df_filtered["State"] == selected_State]
            
            selected_Party = st.selectbox("Select Party", ["All"] + df_filtered["Party"].unique().tolist())
            if selected_Party != "All":
                df_filtered = df_filtered[df_filtered["Party"] == selected_Party]

            selected_PC_Name = st.selectbox("Select Constituency", ["All"] + df_filtered["PC_Name"].unique().tolist())
            if selected_PC_Name != "All":
                df_filtered = df_filtered[df_filtered["PC_Name"] == selected_PC_Name]

            selected_Position = st.selectbox("Select Position", ["All"] + df_filtered["Position"].unique().tolist())
            if selected_Position != "All":
                df_filtered = df_filtered[df_filtered["Position"] == selected_Position]

            selected_Candidate = st.selectbox("Select Candidate", ["All"] + df_filtered["Candidate"].unique().tolist())
            if selected_Candidate != "All":
                df_filtered = df_filtered[df_filtered["Candidate"] == selected_Candidate]

        # Data Overview: Render HTML table with clickable links
        st.subheader("📌 Your Election Data Overview")
        st.markdown(df_filtered.head(100).to_html(escape=False), unsafe_allow_html=True)

        # Generate PDF and download link
        if st.button("Download PDF Report"):
            pdf_buffer = generate_pdf(df_filtered, selected_Year, selected_State, selected_PC_Name, selected_Party, selected_Position)
            
            # Constructing dynamic file name based on filters
            filename = f"Election_Report_{selected_Year}_{selected_State}_{selected_PC_Name}_{selected_Party}_{selected_Position}.pdf".replace(" ", "_")
            
            st.download_button(
                label=f"Click here to download the PDF ({filename})",
                data=pdf_buffer,
                file_name=filename,
                mime="application/pdf"
            )

    else:
        st.error(f"Failed to retrieve file. HTTP Status code: {response_LOKSEATS.status_code}")

except Exception as e:
    st.error(f"An error occurred while processing the file: {e}")
    st.image('election2.jpg', caption='Welcome to sales dashboard & forcating', use_container_width=True)
