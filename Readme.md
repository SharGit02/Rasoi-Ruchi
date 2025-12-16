# Rasoi Ruchi (रसोई रूची)👩🏻‍🍳

Rasoi Ruchi is a digital recipe management application developed as part of my academic learning, inspired by college laboratory sessions where I was introduced to connecting Python applications with relational databases. The project was built to practically apply these concepts by creating a simple yet functional system that combines Python logic, database connectivity, and an interactive user interface using the Streamlit library. Rasoi Ruchi functions as a personal digital recipe book, allowing users to store, organize, and explore recipes in a structured manner, including ingredients, preparation steps, cooking time, image uploads, and basic comments for notes or tips.
This platform aims to digitally preserve traditional and personal recipes, removing the limitations of handwritten notes while allowing users to document cooking secrets, add personal insights, and gradually evolve dishes into improved versions over time. The application supports searching recipes by name and presents detailed instructions in a clear format, with all data securely managed using a MySQL database. While this project is not intended to be a professional or production-level platform, it represents my first complete hands-on project and reflects my focus on understanding core concepts such as data handling, system structure, and UI development.

---

## Features

- Recipe management with ingredients, instructions, and cooking time
- Image upload support for each recipe
- Smart search and filtering
- Step-by-step recipe details
- Commenting system for notes and feedback
- MySQL-backed structured data storage

## Tech Stack

- Frontend & Logic: Streamlit (Python)
- Database: MySQL
- Data Handling: Pandas
- Database Connector: mysql-connector-python

## Installation & Setup

### 1. Prerequisites

- Python 3.8+
- MySQL Server

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rasoi-ruchi.git
cd rasoi-ruchi
```
### 3. Install Dependencies

- Install required Python packages:

```bash
pip install -r requirements.txt
```

- If requirements.txt is not available, install manually:
```bash
pip install streamlit mysql-connector-python pandas
```
### 4. Database Configuration

- This project includes an automated SQL setup script.

**Steps:**

- Open MySQL Command Line Client or MySQL Workbench

- Run the Database_setup.sql file included in the repository

**This script will:**

- Create a database named recipe_app

- Create a user recipe_user

- Set the default password as SharRecipeBook

### 5. Verify Configuration

- Open Recipe.py and ensure the database configuration matches the following:
```bash
DB_CONFIG = {
    'host': 'localhost',
    'user': 'recipe_user',
    'password': 'SharRecipeBook',
    'database': 'recipe_app'
}
```
(This is already configured by default.)

### 6. Running the Application

- From the project directory, run:
```bash
streamlit run Recipe.py
```

- The application will open automatically in your browser at:
```bash
http://localhost:8501
```

### Project Structure

- **Recipe.py** – Main Streamlit application and logic

- **Database_setup.sql** – Database initialization script

- **image_uploads/** – Directory for uploaded recipe images

##### Contributions are welcome! If you have suggestions or improvements, please feel free to fork the repository and submit a pull request.