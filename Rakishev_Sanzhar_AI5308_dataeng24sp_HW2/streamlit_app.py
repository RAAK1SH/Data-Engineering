import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import streamlit as st
from cachetools import TTLCache

# Load data from Excel
data = pd.read_excel("MLB2023_Regular.xlsx")

# Function to create features (replace with your column names if different)
def create_features(data):
    data['wOBA'] = data['OBP'] + data['SLG']
    data['ISO'] = data['SLG'] - data['AVG']
    data['PA'] = data['H'] + data['BB'] + data['AB']
    data['K%'] = (data['SO'] / data['PA']) * 100
    data['BB%'] = (data['BB'] / data['PA']) * 100
    return data

# Preprocess data (create features)
data = create_features(data.copy())  # Avoid modifying original data

# Feature selection
features = ["wOBA", "ISO", "K%", "BB%", "PA"]
target = ["HR"]  # Assuming HR is the target variable for prediction

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2)

# Standardize features (assuming model requires it)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest model
model = RandomForestRegressor()
model.fit(X_train_scaled, y_train)

# Function to predict HR with data scaling
def predict_hr(data):
    df = pd.DataFrame([data])
    scaled_data = scaler.transform(df[features])
    return model.predict(scaled_data)[0]

# Cache for storing predictions (optional)
cache = TTLCache(maxsize=100, ttl=600)  # Cache at most 100 predictions for 10 minutes

# Authentication state (replace with your authentication logic)
authenticated = st.session_state.get("authenticated", False)
username = st.session_state.get("username", None)
user_data = st.session_state.get("user_data", {})  # Store user data

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
        # Replace with your authentication logic (e.g., database check)
        if username == "Sanzhar" and password == "Rakish159753":
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            user_data["name"] = username  # Example user data
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
    
            
if authenticated:
    # Navigation sidebar
    with st.sidebar:
        st.title(f"Welcome, {username}")
        if st.button("Home"):
            st.session_state["page"] = "Home"
        if st.button("Select Player's Name"):
            st.session_state["page"] = "prediction"
        if st.button("Enter Player's Name By Hand"):
            st.session_state["page"] = "prediction2"
        if st.button("MLB 2023 Stats"):
            st.session_state["page"] = "MLB2023"
        if st.button("MLB 2024 Stats"):
            st.session_state["page"] = "MLB2024"
        
        # Add buttons for other functionalities here (optional)

# Navigation options with conditional hiding of prediction section
if not authenticated:
    st.markdown("""
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png" 
    alt="MLB Logo" style="display:block; margin-left: auto; margin-right: auto; width: 300px">            
    <h1 style="color:black; text-align: left; font-size: 40px; font-family: Arial"> Hello, Welcome! </h1>
    <t style="color:black; text-align: center; font-size: 32px; font-family: Arial"> Login </t>
    """, unsafe_allow_html=True)
    login()
else:
    with st.sidebar:
        # Navigation options (consider a sidebar or horizontal menu)
        if st.button("Log Out"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = None
                st.session_state["user_data"] = {}
                st.success("Logged out!")

# Display content based on selected page (using session state)
page = st.session_state.get("page", "Home")  # Set default to None

if not authenticated:
    st.stop()  # Halt Streamlit rendering


if page == "MLB2023":
    st.markdown(f"<h1 style='font-family: Arial, sans-serif; font-size: 30px; line-height: 1;'>MLB 2023</h1>", unsafe_allow_html=True)
    st.markdown("""
    <text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 1.5">            
Here is the MLB data from the year 2023. Dive into the numbers, explore player performances, and gain insights into the dynamic world of baseball. With this data as our foundation, we embark on a journey to forecast future home runs and unravel the mysteries of player statistics.</text>
    """, unsafe_allow_html=True)
    st.write("---")
    st.dataframe(data)
    # data1 = pd.read_excel("MLB2024_Regular.xlsx")
    # st.dataframe(data1)

if page == "MLB2024":
    st.markdown(f"<h1 style='font-family: Arial, sans-serif; font-size: 30px; line-height: 1;'>MLB 2024</h1>", unsafe_allow_html=True)
    st.markdown("""
    <text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 1.5">            
Here is the relevant MLB data from the year 2024. Delve into the latest statistics, analyze player performances, and uncover the trends shaping the current baseball landscape. With this fresh dataset at our disposal, we're equipped to make informed predictions and anticipate the home run hitters of the upcoming season. """, unsafe_allow_html=True)
    data1 = pd.read_excel("MLB2024_Regular.xlsx")
    st.write("---")
    st.dataframe(data1)

if page == "Home":
    st.markdown("""
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png" 
    alt="MLB Logo" style="display:block; margin-left: auto; margin-right: auto; width: 300px">            
    """, unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family: Arial, sans-serif; font-size: 30px; line-height:0;'>Hi {username},</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family: Arial, sans-serif; font-size: 20px; line-height: 1;'>Welcome to my Streamlit Application!</h1>", unsafe_allow_html=True)
    # Add content for the Home page here    
    st.markdown("""
    <text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 0.5">            
    You can redict a player's home runs for the 2024 season based on their estimated 2023 statistics!
    This app utilizes a Random Forest model trained on historical MLB data to forecast home runs. Simply select or enter a player's name, and let's explore their potential performance for the upcoming season. 
    Select a player and let's embark on this predictive journey together!</text>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.markdown("""
    <h3 style="font-weight: bold; font-size: 20px; font-family: Arial;">Objective:</h3>
    """, unsafe_allow_html=True)

    st.markdown("""<text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 0.5">  
    - My goal for this project is to create a toy application and host it. The frontend of our application will allow users to input queries, while the backend will utilize this information to make predictions using a model. These predicted values will then be displayed on the frontend. My focus for this assignment lies in model development and the integration of various system components, rather than on web development itself.
    </text>""", unsafe_allow_html=True)

    st.write("---")
    st.markdown("""
    <h3 style="font-weight: bold; font-size: 20px; font-family: Arial;">Hosting Options:</h3>
    """, unsafe_allow_html=True)    

    st.markdown("""<text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 0.5">  
    - I use Streamlit for hosting my application, as it offers a user-friendly interface.
     </text>""", unsafe_allow_html=True)

    st.write("---")
    st.markdown("""
    <h3 style="font-weight: bold; font-size: 20px; font-family: Arial;">Datasets:</h3>
    """, unsafe_allow_html=True)

    st.markdown("""<text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 1.5">  
    - I use the MLB dataset from HW1.
     </text>""", unsafe_allow_html=True)

    # Navigation buttons to other pages (replace with actual page names)
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("Select Player"):
    #         st.session_state["page"] = "prediction"
    # with col2:
    #     if st.button("Enter Player"):
    #         st.session_state["page"] = "Page3"
    # with col3:
    #     if st.button("More Pages..."):
    #         # Dropdown menu or other navigation options for additional pages
            # pass


if page == "prediction2":
    # Informative text with explanation and player selection
    st.markdown("""
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png" 
    alt="MLB Logo" style="display:block; margin-left: auto; margin-right: auto; width: 300px">            
    <h1 style="color:black; text-align: left; font-size: 32px; font-family: Arial"> MLB Home Run Prediction (2023 Data) </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 1.5">            
    Predict a player's home runs for the 2024 season based on their estimated 2023 statistics!<br>
    This app uses a Random Forest model trained on historical MLB data to predict home runs. Just enter a player's name:
    </text>
    """, unsafe_allow_html=True)

    # player_name = st.selectbox("Select Player", data["PLAYER"].unique())  # Assuming 'Player' is the player name column

    player_name = st.text_input("Enter Player Name")

    # Find player data (using session state)
    if player_name:
        player_data = data[data["PLAYER"] == player_name]
        # Check if same player and update data if needed
            
        if len(player_data) > 0 and player_name == st.session_state.get('player_data', {}).get('name'):
            # Update existing data (assuming same player)
            player_data = player_data.iloc[0]
            player_data = player_data.to_dict()
            st.session_state['player_data'].update(player_data)
            st.info("Player information updated.")
        else:
            # New player, process data
            if len(player_data) > 0:
                player_data = player_data.iloc[0]
                player_data = player_data.to_dict()
                st.session_state['player_data'] = player_data  # Save new player data
            else:
                st.error("Player not found in the data!")

            # Check cache for prediction (optional)
        if player_name in cache:
            predicted_hr = cache[player_name]
        else:
            # Process data for prediction if not cached
            try:
                predicted_hr = predict_hr(player_data)
                cache[player_name] = predicted_hr  # Add prediction to cache
            except Exception as e:  # Handle potential errors during prediction
                st.error(f"An error occurred: {e}")

        actual_hr = player_data["HR"]

        if actual_hr > 0:
            percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
        # Display prediction, data visualization, and progress bar
        st.success(f"Predicted Home Runs for 2024: {predicted_hr:.2f} \n\n"
                    f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")
            
        actual_hr = player_data["HR"]

        if actual_hr > 0:
            percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
            # st.success(f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")


        # # Create labels for the bars
        # labels = ["Actual HR", "Predicted HR"]

        # # Create the bar chart
        # plt.figure(figsize=(10, 5))  # Adjust figure size as needed
        # plt.bar(labels, [actual_hr, predicted_hr], width=0.4, color=['blue', 'red'])
        # plt.xlabel("HR Category")
        # plt.ylabel("HR Value")
        # plt.title("Actual vs. Predicted HR")
        # plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
        # plt.tight_layout()

        # Display the chart as a Streamlit element
        # st.pyplot(plt)

        # Create pie chart data (assuming these are percentages)
        pie_data = [actual_hr, predicted_hr]
        pie_labels = ["Actual HR", "Predicted HR"]

        # Create the pie chart
        plt.figure(figsize=(7, 7))  # Adjust figure size as needed
        plt.pie(pie_data, labels=pie_labels, autopct="%1.1f%%", startangle=140, colors=['blue', 'red'])  # Customize labels, percentages, and colors
        plt.axis("equal")  # Equal aspect ratio ensures a circular pie chart
        plt.title("Actual vs. Predicted HR")

        # Display the chart as a Streamlit element
        st.pyplot(plt)

        # Calculate difference
        hr_difference = predicted_hr - actual_hr

        # Create labels
        labels = ["2023 (Actual)", "2024 (Predicted)"]

        # Create line chart with design elements
        fig, ax = plt.subplots(figsize=(8, 5))  # Set chart size

        # Minimum y-axis value for starting line at actual_hr
        min_y = min(actual_hr, predicted_hr) - hr_difference * 0.1  # Buffer for visual clarity

        # Plot actual and predicted HRs with markers and labels
        lines = ax.plot([2023, 2024], [actual_hr, predicted_hr], marker='o', label=labels, linewidth=2)

        # Customize x-axis labels (assuming 'Year' is numeric)
        ax.set_xticks([2023, 2024])
        ax.set_xticklabels(labels, rotation=0, ha='center')  # Rotate and center tick labels

        # Set y-axis limits (ensures line starts from actual_hr)
        ax.set_ylim(bottom=min_y)

        # Add horizontal line at y=0 (optional)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)  # Adjust alpha for transparency

        # Customize labels, title, and grid lines
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Home Runs", fontsize=12)
        ax.set_title(f"{player_name} HR Difference", fontsize=14)
        ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

        # # Customize legend
        # legend = ax.legend(loc='upper left', title="HR Type", title_fontsize=12)
        # for label in legend.get_texts():
        #     label.set_text(str(label).split(" - ")[1])  # Extract label text without year

        # Format y-axis ticks (optional)
        ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))  # Format as one decimal

        # Color customization (optional)
        colors = ['blue', 'green']  # Adjust colors as desired
        for line, color in zip(lines, colors):
            line.set_color(color)

        # Display chart in Streamlit
        st.pyplot(fig)

        # with st.spinner("Generating Visualization..."):  # Show spinner while plotting
            # fig, ax = plt.subplots()
                # Process data for prediction (assuming predict_hr function is defined)

            # Display prediction
            # Assuming "HR" is the column containing actual home runs

            # Access features directly for labels (recommended)
            # feature_labels = [str(val) for val in player_data[features]]

            # Create bar plot with customization options
            # bars = ax.bar(feature_labels, [actual_hr, predicted_hr], label=["Actual HR", "Predicted HR"], width=0.6, color=['blue', 'green'])  # Adjust bar width and color

            # Customize labels and title
            # ax.set_xlabel("Features", fontsize=14)
            # ax.set_ylabel("Home Runs", fontsize=14)
            # ax.set_title(f"{player_name} Statistics (2023 Actual vs. Predicted 2024)", fontsize=16)

            # Add legend, customize appearance
            # ax.legend(loc='upper left')  # Adjust legend position
            # legend = ax.get_legend()
            # legend.set_title('Home Run Comparison', prop={'size': 12})  # Set legend title

            # Calculate and display percentage difference (optional)
            # actual_hr = player_data["HR"]
            # if actual_hr > 0:
            #     percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
            #     st.success(f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")

            # Customize x-axis tick labels for readability (optional)
            # if len(feature_labels) > 10:  # Adjust threshold for rotation
            #     plt.xticks(rotation=45, ha='right')  # Rotate long labels for better display

            # st.pyplot(fig)

        # Display player image (optional) - replace with image URL if available
        # if 'IMG_URL' in player_data:  # Assuming 'IMG_URL' is the image column
        #     st.image(player_data['IMG_URL'], width=200)

    else:
        st.write("Please enter a player's name.")


    # Save user prediction data (optional)
    if player_name and authenticated:
        prediction_data = {
            "username": username,
            "player_name": player_name,
            "predicted_hr": predicted_hr,  # Assuming 'predicted_hr' is available
            # Add other relevant data if needed (e.g., actual HR if available)
        }
        # Replace with your preferred data storage method (e.g., database)
        # For example: save_prediction_data(prediction_data)
        st.success("Prediction data saved successfully!")

elif page == "user_data":  # Placeholder for user data access (optional)
    if authenticated:
        st.subheader("User Data")
        # Display relevant user data stored in session state (e.g., username, past predictions)
        st.write(f"Username: {user_data.get('name')}")
        # ... (display other user data as needed)
    else:
        st.error("Please log in to access user data.")



if page == "prediction":
    # Informative text with explanation and player selection
    st.markdown("""
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/1200px-Major_League_Baseball_logo.svg.png" 
    alt="MLB Logo" style="display:block; margin-left: auto; margin-right: auto; width: 300px">            
    <h1 style="color:black; text-align: left; font-size: 32px; font-family: Arial"> MLB Home Run Prediction (2023 Data) </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <text style="font-family: Arial, sans-serif; font-size: 18 px; line-height: 1.5">            
    Predict a player's home runs for the 2024 season based on their estimated 2023 statistics!<br>
    This app uses a Random Forest model trained on historical MLB data to predict home runs. Just select a player's name from the list below:
    </text>
    """, unsafe_allow_html=True)

    player_name = st.selectbox("Select Player", data["PLAYER"].unique())  # Assuming 'Player' is the player name column

    # player_name = st.text_input("Enter Player Name")

    # Find player data (using session state)
    if player_name:
        player_data = data[data["PLAYER"] == player_name]
        # Check if same player and update data if needed
            
        if len(player_data) > 0 and player_name == st.session_state.get('player_data', {}).get('name'):
            # Update existing data (assuming same player)
            player_data = player_data.iloc[0]
            player_data = player_data.to_dict()
            st.session_state['player_data'].update(player_data)
            st.info("Player information updated.")
        else:
            # New player, process data
            if len(player_data) > 0:
                player_data = player_data.iloc[0]
                player_data = player_data.to_dict()
                st.session_state['player_data'] = player_data  # Save new player data
            else:
                st.error("Player not found in the data!")

            # Check cache for prediction (optional)
        if player_name in cache:
            predicted_hr = cache[player_name]
        else:
            # Process data for prediction if not cached
            try:
                predicted_hr = predict_hr(player_data)
                cache[player_name] = predicted_hr  # Add prediction to cache
            except Exception as e:  # Handle potential errors during prediction
                st.error(f"An error occurred: {e}")

        actual_hr = player_data["HR"]

        if actual_hr > 0:
            percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
        # Display prediction, data visualization, and progress bar
        st.success(f"Predicted Home Runs for 2024: {predicted_hr:.2f} \n\n"
                    f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")
            
        actual_hr = player_data["HR"]

        if actual_hr > 0:
            percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
            # st.success(f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")

        # Create labels for the bars
        labels = ["Actual HR", "Predicted HR"]

        # Create the bar chart
        plt.figure(figsize=(10, 5))  # Adjust figure size as needed
        plt.bar(labels, [actual_hr, predicted_hr], width=0.4, color=['blue', 'red'])
        plt.xlabel("HR Category")
        plt.ylabel("HR Value")
        plt.title("Actual vs. Predicted HR")
        plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
        plt.tight_layout()

        # Display the chart as a Streamlit element
        st.pyplot(plt)
        
        # Calculate difference
        hr_difference = predicted_hr - actual_hr

        # Create labels
        labels = ["2023 (Actual)", "2024 (Predicted)"]

        # Create line chart with design elements
        fig, ax = plt.subplots(figsize=(8, 5))  # Set chart size

        # Minimum y-axis value for starting line at actual_hr
        min_y = min(actual_hr, predicted_hr) - hr_difference * 0.1  # Buffer for visual clarity

        # Plot actual and predicted HRs with markers and labels
        lines = ax.plot([2023, 2024], [actual_hr, predicted_hr], marker='o', label=labels, linewidth=2)

        # Customize x-axis labels (assuming 'Year' is numeric)
        ax.set_xticks([2023, 2024])
        ax.set_xticklabels(labels, rotation=0, ha='center')  # Rotate and center tick labels

        # Set y-axis limits (ensures line starts from actual_hr)
        ax.set_ylim(bottom=min_y)

        # Add horizontal line at y=0 (optional)
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)  # Adjust alpha for transparency

        # Customize labels, title, and grid lines
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Home Runs", fontsize=12)
        ax.set_title(f"{player_name} HR Difference", fontsize=14)
        ax.grid(color='lightgray', linestyle='--', linewidth=0.5)

        # # Customize legend
        # legend = ax.legend(loc='upper left', title="HR Type", title_fontsize=12)
        # for label in legend.get_texts():
        #     label.set_text(str(label).split(" - ")[1])  # Extract label text without year

        # Format y-axis ticks (optional)
        ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))  # Format as one decimal

        # Color customization (optional)
        colors = ['blue', 'green']  # Adjust colors as desired
        for line, color in zip(lines, colors):
            line.set_color(color)

        # Display chart in Streamlit
        st.pyplot(fig)

        # with st.spinner("Generating Visualization..."):  # Show spinner while plotting
            # fig, ax = plt.subplots()
                # Process data for prediction (assuming predict_hr function is defined)

            # Display prediction
            # Assuming "HR" is the column containing actual home runs

            # Access features directly for labels (recommended)
            # feature_labels = [str(val) for val in player_data[features]]

            # Create bar plot with customization options
            # bars = ax.bar(feature_labels, [actual_hr, predicted_hr], label=["Actual HR", "Predicted HR"], width=0.6, color=['blue', 'green'])  # Adjust bar width and color

            # Customize labels and title
            # ax.set_xlabel("Features", fontsize=14)
            # ax.set_ylabel("Home Runs", fontsize=14)
            # ax.set_title(f"{player_name} Statistics (2023 Actual vs. Predicted 2024)", fontsize=16)

            # Add legend, customize appearance
            # ax.legend(loc='upper left')  # Adjust legend position
            # legend = ax.get_legend()
            # legend.set_title('Home Run Comparison', prop={'size': 12})  # Set legend title

            # Calculate and display percentage difference (optional)
            # actual_hr = player_data["HR"]
            # if actual_hr > 0:
            #     percentage_diff = ((predicted_hr - actual_hr) / actual_hr) * 100
            #     st.success(f"Percentage Difference: {percentage_diff:.2f}% , HR: {actual_hr}")

            # Customize x-axis tick labels for readability (optional)
            # if len(feature_labels) > 10:  # Adjust threshold for rotation
            #     plt.xticks(rotation=45, ha='right')  # Rotate long labels for better display

            # st.pyplot(fig)

        # Display player image (optional) - replace with image URL if available
        # if 'IMG_URL' in player_data:  # Assuming 'IMG_URL' is the image column
        #     st.image(player_data['IMG_URL'], width=200)

    else:
        st.write("Please select a player from the list or enter a name.")


    # Save user prediction data (optional)
    if player_name and authenticated:
        prediction_data = {
            "username": username,
            "player_name": player_name,
            "predicted_hr": predicted_hr,  # Assuming 'predicted_hr' is available
            # Add other relevant data if needed (e.g., actual HR if available)
        }
        # Replace with your preferred data storage method (e.g., database)
        # For example: save_prediction_data(prediction_data)
        st.success("Prediction data saved successfully!")

elif page == "user_data":  # Placeholder for user data access (optional)
    if authenticated:
        st.subheader("User Data")
        # Display relevant user data stored in session state (e.g., username, past predictions)
        st.write(f"Username: {user_data.get('name')}")
        # ... (display other user data as needed)
    else:
        st.error("Please log in to access user data.")