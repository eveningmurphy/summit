#### SUMMIT APPLICATION MARKDOWN DOCUMENT ####

###  Metadata
##       Author name:
            Eve Murphy
##       School of education:
            University of the West of England, Department of Computer Science & Creative Technologies
##       Student ID:
            20049423
##       Module code:
            UFRCFR4-45-3
##       Date:
            19/07/2024
##       Project title:
            Summit: A Community-driven Decision-making Application for Cooperative Organisations
##       Project Repository:
            https://github.com/eveningmurphy/summit

###  Overview
This project is a web application called Summit, designed to handle proposals, voting, and comments within a community. It uses Flask for the web framework and MySQL for the database. This README provides instructions for setting up the development environment, installing dependencies, and configuring the database.

###  Setup Instructions
## Hosting Environment:
1. **Download and Install XAMPP**:
    - Visit the [Apache Friends website](https://www.apachefriends.org/index.html).
    - Download the latest version of XAMPP.
    - Follow the installation instructions for your operating system.

2. **Start XAMPP**:
    - Open the XAMPP Control Panel.
    - Start the Apache and MySQL services.

## Extracting Files:

1. **Extract the Application Zip**:
    - Locate the zip file of the application.
    - Extract the contents of the zip file to the `htdocs` directory within your XAMPP installation folder (usually located at `C:\xampp\htdocs` on Windows or `/Applications/XAMPP/htdocs` on macOS).

## Python Virtual Environment:

1. **Set Up a Python Virtual Environment**:
    - Open a terminal or command prompt.
    - Navigate to the root directory of the extracted application files.
    - Run the following commands to create and activate a virtual environment:
      ```sh
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
      ```

2. **Install Required Python Packages**:
    - With the virtual environment activated, install the required packages using `pip`:
      ```sh
      pip install -r requirements.txt
      ```

## Running the Application:

1. **Configure the Database**:
    - Open your web browser and go to `http://localhost/phpmyadmin`.
    - Create a new database named `summit`.
    - Import the SQL file provided with the application (`summit.sql`) to set up the necessary tables and data.

2. **Start the Flask Application**:
    - Ensure your virtual environment is activated.
    - Run the Flask application:
      ```sh
      python app.py
      ```
    - Open your web browser and navigate to `http://localhost:5000` to access the application.

###  Project Structure
##  Python Files
#       app.py:

        - Main executable script for the Summit application.
        - Defines routes for each page on the web app.
        - Handles session management and interaction with the database.

#       contracts.py:

        - Contains classes to simulate blockchain node interaction.
        - Includes methods for proposal voting and finalizing, and logging operations.

#       db.py:

        - Contains functions for database connection and queries.
        - Handles login, proposal management, comment insertion, and user information retrieval.

## HTML/CSS/JS Files
#       templates:

        - base.html: Base template for all other HTML templates. Includes common elements like the navbar and footer.
        - index.html: Home page displaying proposals.
        - dashboard.html: User dashboard showing member details, proposals, and votes.
        - log.html: Page displaying log entries.
        - login.html: Login page.
        - proposal.html: Page displaying a specific proposal and its comments.
        - submit_proposal.html: Page for submitting new proposals.

#       static:

        - css/style.css: Contains all custom CSS styles for the application.
        - img/: Directory for storing image files used in the application.
        - js/: Directory for storing JavaScript files (if any).
        