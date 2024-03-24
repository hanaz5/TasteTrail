#main.py
import streamlit as st
import time
from RecipeClass import RecipeClass as rc

def main():
    if 'edited_ingredients' not in st.session_state:
        st.session_state.edited_ingredients = ""

    st.set_page_config(page_title='TasteTrail', page_icon="https://github.com/hanaz5/TasteTrail/blob/main/images/icon.png?raw=true")
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    LOGO_IMAGE_URL = "https://github.com/hanaz5/TasteTrail/blob/main/images/logo.png?raw=true"
    st.image(LOGO_IMAGE_URL, caption='', use_column_width=True)
    st.markdown("""
    <div class="logo-container">
        <p>Turn your kitchen chaos into culinary creativity – snap, identify, and savor!</p>
    </div>
    """, unsafe_allow_html=True)

    #user select input method
    input_method = st.sidebar.radio("Select input method:", ("Upload Picture", "Manually Enter Ingredients"))

    if input_method == "Upload Picture": #upload image
        uploaded_file = st.sidebar.file_uploader("Upload an image of ingredients", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            #display image
            st.toast('Loading...')
            time.sleep(2.5)
            st.sidebar.image(uploaded_file, width=100)
            try:
                #image recognition using gemini
                identified_ingredients = rc.recognize_ingredients(uploaded_file)

                if identified_ingredients:
                    #identified ingredients in text area so that user can still edit
                    st.session_state.edited_ingredients = st.sidebar.text_area("Edit Ingredients (separated by commas):", value=", ".join(identified_ingredients))

                    #advanced search
                    with st.sidebar.expander("Advanced Search"):
                        diet_pref = st.selectbox("Diet preference:", ["Any", "Dairy-free", "Gluten-free", "Keto", "Vegan", "Vegetarian"], index=0)
                        allergies = st.text_input("Allergies:", "", placeholder="Enter allergies separated by commas")
                        halal_check = st.checkbox("Halal Meal")
                        max_prep_time = st.slider("Prep Time (mins)", min_value=5, max_value=180, value=60, step=5)

                    #generate recipes button
                    if st.sidebar.button("Generate Recipes"):
                        st.toast('Loading...')
                        time.sleep(1.7)
                        ingredient_list = [ingredient.strip() for ingredient in st.session_state.edited_ingredients.split(",")]
                        if ingredient_list:
                            recipe_suggestions = rc.generate_recipe_suggestions(ingredient_list, allergies, halal_check, diet_pref, max_prep_time=max_prep_time)
                            if recipe_suggestions:
                                st.toast('Gathering ingredients...')
                                time.sleep(1.5)
                                st.toast('Cooking...')
                                time.sleep(1.5)
                                st.toast('Ready!', icon="🍽️")
                                rc.display_recipe_suggestions(recipe_suggestions)
                            else:
                                st.write("No recipe suggestions found.")
                        else:
                            st.sidebar.warning("Please enter at least one ingredient.")
            except Exception as e:
                #error for when image cannot be recognized
                st.toast('Cannot be recognized.', icon="😔")
                st.sidebar.error("Ingredients cannot be recognized. Please input the ingredients manually.")

                #manual method will be display due to error above
                ingredients = st.sidebar.text_area("Enter the ingredients (separated by commas):", "")

                #advanced search
                with st.sidebar.expander("Advanced Search"):
                    diet_pref = st.selectbox("Diet preference:", ["Any", "Dairy-free", "Gluten-free", "Keto", "Vegan", "Vegetarian"], index=0)
                    allergies = st.text_input("Allergies:", "", placeholder="Enter allergies separated by commas")
                    halal_check = st.checkbox("Halal Meal")
                    max_prep_time = st.slider("Prep Time (mins)", min_value=5, max_value=180, value=60, step=5)

                #generate recipes button
                if st.sidebar.button("Generate Recipes"):
                    st.toast('Loading...')
                    time.sleep(1.7)
                    if ingredients:
                        ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]
                        recipe_suggestions = rc.generate_recipe_suggestions(ingredient_list, allergies, halal_check, diet_pref, max_prep_time=max_prep_time)
                        if recipe_suggestions:
                            st.toast('Gathering ingredients...')
                            time.sleep(1.5)
                            st.toast('Cooking...')
                            time.sleep(1.5)
                            st.toast('Ready!', icon="🍽️")
                            rc.display_recipe_suggestions(recipe_suggestions)
                        else:
                            st.write("No recipe suggestions found.")
                    else:
                        st.sidebar.warning("Please enter at least one ingredient.")

    else:  #manually input
        ingredients = st.sidebar.text_area("Enter the ingredients (separated by commas):", "")

        #advanced search
        with st.sidebar.expander("Advanced Search"):
            diet_pref = st.selectbox("Diet preference:", ["Any", "Alcohol-free", "Dairy-free", "Gluten-free", "Keto", "Paleo", "Vegan", "Vegetarian"], index=0)
            allergies = st.text_input("Allergies:", "", placeholder="Enter allergies separated by commas")
            halal_check = st.checkbox("Halal Meal")
            max_prep_time = st.slider("Prep Time (mins)", min_value=5, max_value=180, value=60, step=5)

        #generate recipes button
        if st.sidebar.button("Generate Recipes"):
            st.toast('Loading...')
            time.sleep(1.7)
            if ingredients:
                ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]
                recipe_suggestions = rc.generate_recipe_suggestions(ingredient_list, allergies, halal_check, diet_pref, max_prep_time=max_prep_time)
                if recipe_suggestions:
                    st.toast('Gathering ingredients...')
                    time.sleep(1.5)
                    st.toast('Cooking...')
                    time.sleep(1.5)
                    st.toast('Ready!', icon="🍽️")
                    rc.display_recipe_suggestions(recipe_suggestions)
                else:
                    st.write("No recipe suggestions found.")
            else:
                st.sidebar.warning("Please enter at least one ingredient.")


if __name__ == "__main__":
    main()
#hanaz, cohort4