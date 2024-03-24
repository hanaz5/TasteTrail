#RecipeClass.py
import streamlit as st
import google.generativeai as genai
import PIL
import requests
import time
from ConstantClass import ConstantClass as cc

class RecipeClass:

    #image recognition using gemini
    def recognize_ingredients(image):
        st.secrets.GOOGLE_API_KEY
        image = PIL.Image.open(image)

        #generate content using the vision model
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        response = vision_model.generate_content(["List all the item separated by comma. Just item, no need sentences such as 'There are various...'.", image])
        
        #extract the recognized text from the response
        recognized_text = response.text
        
        identified_ingredients = [ingredient.strip() for ingredient in recognized_text.split(",")]
        st.toast('Analyzing...')
        time.sleep(1.5)
        st.toast('Listed!', icon="🥣")
        return identified_ingredients

    #generate recipe based on ingredients using Edamam API
    def generate_recipe_suggestions(ingredients, allergies, halal_check, diet_pref="", max_prep_time=60):
        params = {
            "q": ",".join(ingredients),
            "app_id": st.secrets.EDAMAM_API_ID,
            "app_key": st.secrets.EDAMAM_API_KEY,
            "to": 15,
            "time": f"0-{max_prep_time}"
        }

        #filter recipes
        if diet_pref != "Any":
            params["health"] = diet_pref.lower()

        response = requests.get(cc.EDAMAM_RECIPE_SEARCH_API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            recipes = data.get('hits', [])
            
            recipe_details = []
            for hit in recipes:
                recipe = hit['recipe']
                prep_time = recipe.get('totalTime', 0)
                if prep_time == 0.0:
                    prep_time = 30.0
                #check prep time
                if prep_time <= max_prep_time:
                    #check allergies
                    if allergies:
                        allergic_ingredients = allergies.split(",")
                        contains_allergen = False
                        for ingredient in allergic_ingredients:
                            if ingredient.strip().lower() in recipe['label'].lower():
                                contains_allergen = True
                                break
                        if contains_allergen:
                            continue
                        for ingredient_line in recipe['ingredientLines']:
                            for ingredient in allergic_ingredients:
                                if ingredient.strip().lower() in ingredient_line.lower():
                                    contains_allergen = True
                                    break
                            if contains_allergen:
                                break
                        if contains_allergen:
                            continue
                    #check halal
                    if halal_check:
                        non_halal_ingredients = ["pork", "bacon", "ham", "alcohol", "wine", "beer", "liquor", "lard"]
                        contains_non_halal = False
                        for ingredient in non_halal_ingredients:
                            if ingredient in recipe['label'].lower() or any(ingredient in ingredient_line.lower() for ingredient_line in recipe['ingredientLines']):
                                contains_non_halal = True
                                break
                        if contains_non_halal:
                            continue
                    
                    #fetch meal image
                    image = recipe.get('image')
                    if image:
                        image_url = image.replace("_medium", "_lg")
                    else:
                        image_url = None

                    recipe_info = {
                        "label": recipe['label'],
                        "ingredients": recipe['ingredientLines'],
                        "url": recipe['url'],
                        "image_url": image_url,
                        "prep_time": prep_time
                    }
                    recipe_details.append(recipe_info)
            
            return recipe_details
        else:
            st.error("Failed to fetch recipes from Edamam API.")
            return []

    #display recipe suggestions
    def display_recipe_suggestions(recipe_suggestions):
        st.subheader("Recipe Suggestions:")
        for recipe in recipe_suggestions:
            with st.expander(recipe['label']):
                col1, col2 = st.columns([2, 3])
                with col1:
                    image_url = recipe.get('image_url')
                    if image_url:
                        st.image(image_url, width=200)
                        st.markdown("URL: " + f"[Recipe Link]({recipe['url']})")
                        st.write(f"Preparation Time: {recipe.get('prep_time', 'N/A')} minutes")
                with col2:
                    st.markdown("<h3 style='font-size: 1.2em;'>Ingredients</h3>", unsafe_allow_html=True)
                    ingredients_html = "<ul style='list-style-type: square; padding-left: 1.5em; line-height: 1.5;'>"
                    ingredients_html += "".join([f"<li>{ingredient}</li>" for ingredient in recipe['ingredients']])
                    ingredients_html += "</ul>"
                    st.markdown(ingredients_html, unsafe_allow_html=True)
#hanaz, cohort4