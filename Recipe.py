import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
import os

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'recipe_user',
    'password': 'SharRecipeBook',
    'database': 'recipe_app'
}

UPLOAD_DIR = "image_uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ==============================================================================
# Custom CSS for Styling
# ==============================================================================
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

page_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');

    /* --- Main App Styling --- */
    .stApp {
        background-color: #FDF5E6; /* Soft, warm off-white (Old Lace) */
    }

    /* --- Font Styling --- */
    body, p, ol, ul, li, label {
        font-family: 'Poppins', sans-serif;
        color: #333333 !important; /* Near-black for high contrast */
    }

    h1, h2, h3 {
        font-family: 'Lora', serif; /* Elegant font for headers */
        color: #BF6000 !important; /* Your chosen accent color */
    }
    
    /* Ensure all text inside streamlit elements is readable */
    .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1v0mbdj, .st-emotion-cache-1r6slb0, .st-emotion-cache-10trblm, .st-emotion-cache-qbe2hs, .st-emotion-cache-7006d, .st-emotion-cache-1q8dd3e {
        color: #333333 !important;
    }

    /* --- Main Content Block --- */
    [data-testid="stVerticalBlock"] .st-emotion-cache-16txtl3 {
        background-color: rgba(255, 255, 255, 0.8); /* Slightly more opaque white */
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* --- Sidebar Styling --- */
    [data-testid="stSidebar"] {
        background-color: #FFF8E1 !important; /* Light cream color */
        border-right: 1px solid #E0E0E0;
    }

    /* --- Button Styling --- */
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #BF6000;
        background-color: white; /* Your chosen accent color */
        color: black;
        transition: all 0.2s;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    .stButton>button:hover {
        border: 1px solid #A55300;
        background-color: black; /* Darker shade for hover */
        color: white;
    }

    /* --- FIX for Black Input Bars and Elements --- */
    [data-testid="stTextInput"] input, 
    [data-testid="stTextArea"] textarea,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1px solid #BDBDBD !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] button {
        border: 1px solid #BF6000 !important;
        background-color: #BF6000 !important;
        color: white !important;
    }
    .st-emotion-cache-1fttcpj { /* Expander header */
        background-color: #F0EAD6 !important;
        border-radius: 8px;
    }

    /* --- Table Outline Styling --- */
    .stTable, .stDataFrame {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        overflow: hidden; /* Ensures border radius is applied to the table */
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #E0E0E0;
    }
    thead th {
        background-color: #FFF8E1; /* Light cream header to match sidebar */
        color: #BF6000; /* Your chosen accent color for header text */
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    tbody tr:nth-of-type(even) {
        background-color: #F9F9F9; /* Zebra striping for rows */
    }
    tbody tr:hover {
        background-color: #F1F1F1;
    }
    
    </style>
"""

# ==============================================================================
# Database Interaction Functions
# ==============================================================================
def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        st.error("Please ensure your MySQL server is running and the password in `app.py` is correct.")
        return None

@st.cache_data(ttl=60)
def fetch_all_recipes():
    """Fetches a list of all recipe IDs and names for the sidebar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM recipes ORDER BY name ASC")
            return cursor.fetchall()
        finally:
            conn.close()
    return []

@st.cache_data(ttl=60)
def fetch_recipe_details(recipe_id):
    """Fetches all details for a single recipe, including ingredients and instructions."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
            recipe_data = cursor.fetchone()
            if not recipe_data: return None
            cursor.execute("SELECT i.name, ri.quantity, ri.unit FROM recipe_ingredients ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE ri.recipe_id = %s", (recipe_id,))
            recipe_data['ingredients'] = cursor.fetchall()
            cursor.execute("SELECT step_number, description FROM instructions WHERE recipe_id = %s ORDER BY step_number", (recipe_id,))
            recipe_data['instructions'] = cursor.fetchall()
            return recipe_data
        finally:
            conn.close()
    return None

@st.cache_data(ttl=30)
def fetch_comments(recipe_id):
    """Fetches all comments for a single recipe."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT author, comment_text, created_at FROM comments WHERE recipe_id = %s ORDER BY created_at DESC", (recipe_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    return []

def add_comment(recipe_id, author, comment_text):
    """Inserts a new comment into the database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO comments (recipe_id, author, comment_text) VALUES (%s, %s, %s)"
            cursor.execute(sql, (recipe_id, author, comment_text))
            conn.commit()
            st.cache_data.clear()
            return True
        finally:
            conn.close()
    return False

def add_recipe(recipe_data, uploaded_image):
    """Inserts a new recipe, its ingredients, instructions, and handles the image upload."""
    image_path = None
    if uploaded_image is not None:
        image_filename = f"recipe_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_image.name}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as f: f.write(uploaded_image.getbuffer())
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            conn.start_transaction()
            recipe_sql = "INSERT INTO recipes (name, description, cuisine, course, diet_type, prep_time_minutes, cook_time_minutes, image_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(recipe_sql, (recipe_data['name'], recipe_data['description'], recipe_data['cuisine'], recipe_data['course'], recipe_data['diet_type'], recipe_data['prep_time_minutes'], recipe_data['cook_time_minutes'], image_path))
            new_recipe_id = cursor.lastrowid
            for ing in recipe_data['ingredients']:
                cursor.execute("INSERT IGNORE INTO ingredients (name) VALUES (%s)", (ing['name'],))
                cursor.execute("SELECT id FROM ingredients WHERE name = %s", (ing['name'],));
                ingredient_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit) VALUES (%s, %s, %s, %s)", (new_recipe_id, ingredient_id, ing['quantity'], ing['unit']))
            for i, instruction in enumerate(recipe_data['instructions']):
                cursor.execute("INSERT INTO instructions (recipe_id, step_number, description) VALUES (%s, %s, %s)", (new_recipe_id, i + 1, instruction['description']))
            conn.commit()
            st.cache_data.clear()
            return True
        except mysql.connector.Error as err:
            conn.rollback()
            st.error(f"Database Error: Failed to add recipe. {err}")
        finally:
            conn.close()
    return False

# ==============================================================================
# Streamlit User Interface
# ==============================================================================

st.set_page_config(page_title="रसोई रूची", layout="wide", initial_sidebar_state="expanded")

# --- Inject Custom CSS ---
st.markdown(page_style, unsafe_allow_html=True)

st.title("रसोई रूची")
st.markdown("From your kitchen to the world, share the recipes you love. Discover flavors, explore stories, and let taste bring us together.")

# --- Sidebar for Navigation and Search ---
st.sidebar.title("Navigation")
all_recipes = fetch_all_recipes()
if all_recipes:
    recipe_names = [recipe['name'] for recipe in all_recipes]
    search_term = st.sidebar.text_input("Search Recipes", "")
    filtered_names = [name for name in recipe_names if search_term.lower() in name.lower()] if search_term else recipe_names
    
    if not filtered_names:
        st.sidebar.warning("No recipes found for your search.")
        selected_recipe_name = None
    else:
        selected_recipe_name = st.sidebar.radio("Select a Recipe", filtered_names)
else:
    st.sidebar.info("Your recipe book is empty. Add your first recipe below!"); 
    selected_recipe_name = None

# --- Main Content Area: Display Selected Recipe ---
if selected_recipe_name:
    recipe_id = next((r['id'] for r in all_recipes if r['name'] == selected_recipe_name), None)
    
    if recipe_id:
        recipe_details = fetch_recipe_details(recipe_id)
        if recipe_details:
            st.header(recipe_details['name'])
            
            if recipe_details.get('image_path') and os.path.exists(recipe_details['image_path']):
                st.image(recipe_details['image_path'], use_column_width=True)

            st.markdown(f"**Cuisine:** {recipe_details['cuisine']} | **Course:** {recipe_details['course']} | **Diet:** {recipe_details.get('diet_type', 'N/A')}")
            st.markdown(f"_{recipe_details['description']}_")
            c1, c2 = st.columns(2)
            c1.info(f"**Prep Time:** {recipe_details['prep_time_minutes']} minutes")
            c2.success(f"**Cook Time:** {recipe_details['cook_time_minutes']} minutes")
            st.markdown("---")

            col_ing, col_ins = st.columns([1, 2])
            with col_ing:
                st.subheader("Ingredients")
                df_ingredients = pd.DataFrame(recipe_details['ingredients'])[['quantity', 'unit', 'name']].rename(columns={'name': 'Ingredient'})
                st.table(df_ingredients)
            with col_ins:
                st.subheader("Instructions")
                for instruction in recipe_details['instructions']:
                    st.markdown(f"**{instruction['step_number']}.** {instruction['description']}")
            st.markdown("---")

            st.subheader("Comments & Tips")
            comments = fetch_comments(recipe_id)
            if comments:
                for comment in comments:
                    ts = comment['created_at'].strftime('%b %d, %Y at %I:%M %p')
                    st.info(f"**{comment['author']}** (_{ts}_):\n\n>{comment['comment_text']}")
            else:
                st.write("Be the first to leave a comment or tip!")
            
            with st.form(f"comment_form_{recipe_id}", clear_on_submit=True):
                author = st.text_input("Your Name", value="Anonymous")
                comment_text = st.text_area("Share your tip or comment")
                if st.form_submit_button("Submit Comment"):
                    if comment_text:
                        if add_comment(recipe_id, author, comment_text):
                            st.success("Comment submitted!")
                            st.rerun()
                    else:
                        st.warning("Comment cannot be empty.")

# --- Sidebar: Add New Recipe Section ---
with st.sidebar.expander("Add Your Own Recipe", expanded=True):
    with st.form("new_recipe_form", clear_on_submit=True):
        st.subheader("Enter New Recipe Details")
        name = st.text_input("Recipe Name*")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        description = st.text_area("Description*")
        
        c1, c2, c3 = st.columns(3)
        cuisine = c1.text_input("Cuisine*")
        course = c2.text_input("Course*")
        diet_type = c3.selectbox("Diet*", ["Vegetarian", "Non-Vegetarian"])
        
        c4, c5 = st.columns(2)
        prep_time = c4.number_input("Prep Time (min)*", min_value=0, step=5)
        cook_time = c5.number_input("Cook Time (min)*", min_value=0, step=5)
        
        ingredients_text = st.text_area("Ingredients*", help="One per line, format: `quantity unit, name` (e.g., `2 cups, Basmati Rice`)")
        instructions_text = st.text_area("Instructions*", help="One step per line.")

        if st.form_submit_button("Save New Recipe"):
            if not all([name, description, cuisine, course, ingredients_text, instructions_text]):
                st.warning("Please fill out all required fields marked with *.")
            else:
                ingredients = []
                for line in ingredients_text.strip().split('\n'):
                    parts = line.split(',')
                    if len(parts) == 2:
                        qty_unit, ing_name = parts
                        qty_parts = qty_unit.strip().split()
                        quantity = qty_parts[0] if qty_parts else ""
                        unit = " ".join(qty_parts[1:])
                        ingredients.append({"name": ing_name.strip(), "quantity": quantity, "unit": unit})
                
                instructions = [{"description": line.strip()} for line in instructions_text.strip().split('\n')]
                
                new_recipe_data = {
                    "name": name, "description": description, "cuisine": cuisine, "course": course, 
                    "diet_type": diet_type, "prep_time_minutes": prep_time, "cook_time_minutes": cook_time, 
                    "ingredients": ingredients, "instructions": instructions
                }
                
                if add_recipe(new_recipe_data, uploaded_image):
                    st.success(f"Recipe '{name}' added successfully!")
                    st.rerun()


