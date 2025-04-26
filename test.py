import streamlit as st
import requests
from typing import List

st.markdown("""
    <style>
        @keyframes jump {
            0%   { transform: translateY(0); }
            50%  { transform: translateY(-8px); }
            100% { transform: translateY(0); }
        }

        .stSidebar button {
            animation: jump 1.5s infinite;
            background-color: #F5F5DC !important;
            border: none !important;
            font-weight: bold;
        }

        .stSidebar button:hover {
            animation: none;
            color: #D2691E !important;
            transform: scale(1.05);
        }
       .stApp,
section[data-testid="stSidebar"] {
  background: linear-gradient(
    180deg,
    #A8D8E6   0%, 
    #F0E5D8  40%,
    #F6C6A7 80%,
    #B5E3D8 100%
  );
  background-attachment: fixed;
}
        .headerE3C6A8 { visibility: hidden; }

        .recipe-card:hover {
            transform: translateZ(10px);
        }
    </style>
""", unsafe_allow_html=True)
class Recipe:
    def __init__(self, name: str, image_url: str, instructions: str, ingredients: List[str]):
        self.name = name
        self.image_url = image_url
        self.instructions = instructions
        self.ingredients = ingredients

    def display(self):
        st.markdown(f"""
            <style>
                .vintage-title {{
                    font-family: 'Playfair Display', serif;
                    font-size: 48px;
                    text-align: center;
                    color: #4B2E2B;
                    text-shadow:
                        1px 1px 0 #000,
                        2px 2px 0 #555,
                        3px 3px 5px rgba(0,0,0,0.2);
                    margin-bottom: 20px;
                }}

                .bordered-img {{
                display: block;
                margin-left: auto;
                margin-right: auto;
                border: 8px solid #3E3E3E;
                box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
                border-radius: 10px;
                 max-width: 500px;  /* Max width */
                 max-height: 350px;
                 max-width: 100%;
               height: auto; 
                }}

                .ingredients-list {{
                    font-family: Arial, sans-serif;
                    font-size: 18px;
                    color: #333;
                    list-style-type: disc;
                    margin-left: 40px;
                }}
            </style>

            <h1 class="vintage-title">{self.name}</h1>
            <img src="{self.image_url}" class="bordered-img" alt="Recipe Image"/>
        """, unsafe_allow_html=True)

        st.markdown("### Ingredients")
        st.markdown(f"<ul class='ingredients-list'>{''.join(f'<li>{ingredient}</li>' for ingredient in self.ingredients)}</ul>", unsafe_allow_html=True)
        st.markdown("### Instructions")
        st.markdown(self.instructions)

class RecipeAPI:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def fetch_recipes(self) -> List[dict]:
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            return data['meals'] if data['meals'] else []
        except Exception as e:
            st.error(f"Failed to fetch recipes: {e}")
            return []

    def fetch_recipe_details(self, meal_id: str) -> Recipe:
        details_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        try:
            response = requests.get(details_url)
            response.raise_for_status()
            data = response.json()
            meal = data['meals'][0]

            ingredients = []
            for i in range(1, 21):
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ingredient and ingredient.strip():  # Check if ingredient exists
                    # If measure exists, append ingredient and measure together
                    if measure and measure.strip():
                        ingredients.append(f"{ingredient.strip()} - {measure.strip()}")
                    else:
                        ingredients.append(f"{ingredient.strip()}")
            return Recipe(
                name=meal['strMeal'],
                image_url=meal['strMealThumb'],
                instructions=meal['strInstructions'],
                ingredients=ingredients
            )
        except Exception as e:
            st.error(f"Failed to fetch recipe details: {e}")
            return Recipe("Unknown", "", "No instructions available.")
class RecipeApp:
    def __init__(self):
        self.api = RecipeAPI("https://www.themealdb.com/api/json/v1/1/filter.php?a=American")
        self.recipe_list = []

    def load_recipes(self):
        self.recipe_list = self.api.fetch_recipes()

    def show_sidebar(self):
        st.sidebar.title("🍲 Recipes")

        if st.sidebar.button("🏠 Home"):
            if "recipe_id" in st.query_params:
                del st.query_params["recipe_id"]
        
        for recipe in self.recipe_list:
            if st.sidebar.button(recipe['strMeal']):
                st.query_params["recipe_id"] = recipe['idMeal']

    def show_home_page(self):
        st.markdown("""
            <style>
                .centered-title {
                    text-align: center;
                    font-family: 'Playfair Display', serif;
                    font-size: 48px;
                    color: #4B2E2B;
                    text-shadow: 1px 1px 0 #000,
                                 2px 2px 0 #555,
                                 3px 3px 5px rgba(0,0,0,0.2);
                    margin-top: 40px;
                }

                .centered-paragraph {
                    text-align: center;
                    font-size: 22px;
                    color: #333;
                    font-family: Arial, sans-serif;
                    font-weight: 300;
                    text-shadow: 1px 1px 0 #000,
                                 2px 2px 0 #555,
                                 3px 3px 3px rgba(0,0,0,0.1);
                    margin-top: 150px;
                    padding: 30px;
                    max-width: 80%;
                    margin-left: auto;
                    margin-right: auto;
                    background-color: #F5F5DC;
                    border-radius: 15px;
                    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                    animation: fadeIn 1s ease-in-out, glow 1.5s infinite alternate;
                }

                /* Animation for fade-in effect */
                @keyframes fadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }

                /* Animation for glow effect */
                @keyframes glow {
                    0% {
                        box-shadow: 0 0 5px #f7b500, 0 0 10px #f7b500, 0 0 15px #f7b500;
                    }
                    50% {
                        box-shadow: 0 0 10px #f7b500, 0 0 20px #f7b500, 0 0 30px #f7b500;
                    }
                    100% {
                        box-shadow: 0 0 5px #f7b500, 0 0 10px #f7b500, 0 0 15px #f7b500;
                    }
                }
            </style>
            <h1 class="centered-title">🍽️ Welcome to My Recipe Book</h1>
            <div class="centered-paragraph">
                Join us on a flavorful journey where we explore delicious dishes from around the world.😋🍝🥗 Click on the side bar button on top left to open the menu!
            </div>
        """, unsafe_allow_html=True)

    def run(self):
        self.load_recipes()
        self.show_sidebar()

        recipe_id = st.query_params.get("recipe_id")
        if recipe_id:
            recipe_obj = self.api.fetch_recipe_details(recipe_id)
            recipe_obj.display()
        else:
            self.show_home_page()

if __name__ == "__main__":
    app = RecipeApp()
    app.run()  