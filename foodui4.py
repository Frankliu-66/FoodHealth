import streamlit as st
import requests

st.set_page_config("🍽️ Food Risk Detector", layout="wide")
st.title("🍽️ Open Food Facts UI")

# --- Sidebar ---
st.sidebar.header("Configure Query")
barcode = st.sidebar.text_input("Product Barcode", "")
fields = st.sidebar.multiselect(
    "Fields to retrieve",
    [
        "product_name",
        "nutrition_grades",
        "ingredients_text",
        "allergens_tags",
        "labels_tags",
        "misc_tags"
    ],
    default=["product_name", "nutrition_grades"]
)
operation = st.sidebar.radio("Operation", ["Fetch Product", "Search by Category", "Submit Missing Data"])

# Additional inputs
if operation == "Search by Category":
    st.sidebar.info("Please enter category in English, e.g. 'Orange Juice', 'Breakfast Cereals', 'Chocolate'.")
    category = st.sidebar.text_input("Category (e.g. Orange Juice)", "")
    grade = st.sidebar.selectbox("Nutrition Grade (optional)", ["", "a", "b", "c", "d", "e"])
elif operation == "Submit Missing Data":
    uid = st.sidebar.text_input("User ID", "")
    pwd = st.sidebar.text_input("Password", type="password")

# --- Helper function to display a product card ---
def display_product_card(p):
    product_name = p.get("product_name", "Unknown")
    code = p.get("code", "Unknown")
    brand = p.get("brands", "Unknown")
    quantity = p.get("quantity", "Unknown")
    nutrition_grade = p.get("nutrition_grades", "Unknown")
    categories = p.get("categories_tags", [])
    ecoscore = p.get("ecoscore_grade", "Unknown")
    image_url = p.get("image_small_url", "")
    ingredients = p.get("ingredients_text", "Not available")
    allergens = p.get("allergens_tags", [])
    labels = p.get("labels_tags", [])
    countries = p.get("countries_tags", [])
    nutriments = p.get("nutriments", {})
    nutriscore_data = p.get("nutriscore_data", {})

    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            if image_url:
                st.image(image_url, width=100)
            else:
                st.image("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg", width=100)
        with cols[1]:
            st.markdown(f"### 🥫 {product_name}")

            if brand and brand != "Unknown":
                brand_link = f"https://world.openfoodfacts.org/brand/{brand.replace(' ', '-')}"
                st.markdown(f"**Brand:** [{brand}]({brand_link})", unsafe_allow_html=True)
            else:
                st.write(f"**Brand:** {brand}")

            st.write(f"**Quantity:** {quantity}")
            st.write(f"**Barcode:** {code}")

            if nutrition_grade and nutrition_grade != "Unknown":
                grade_display = {
                    'a': '🟢 A 🥦', 'b': '🟡 B 🍊', 'c': '🟠 C 🍞', 'd': '🟠 D 🍟', 'e': '🔴 E 🍩'
                }.get(nutrition_grade.lower(), nutrition_grade.upper())
                st.write(f"**Nutrition Grade:** {grade_display}")

                # Show Nutrition Score
                score = nutriscore_data.get("score", None)
                if score is not None:
                    st.write(f"**Nutrition Score:** {score:+d}")

            if ecoscore and ecoscore != "Unknown":
                ecoscore_display = {
                    'a': '🟢 A 🌿', 'b': '🟡 B 🍂', 'c': '🟠 C 🍁', 'd': '🟠 D 🪵', 'e': '🔴 E 🔥'
                }.get(ecoscore.lower(), ecoscore.upper())
                st.write(f"**Eco-Score:** {ecoscore_display}")

            if nutriments:
                st.markdown("**🔬 Nutrition Facts (per 100g):**")
                cal = nutriments.get("energy-kcal_100g", None)
                fat = nutriments.get("fat_100g", None)
                sugars = nutriments.get("sugars_100g", None)
                salt = nutriments.get("salt_100g", None)
                proteins = nutriments.get("proteins_100g", None)
                sodium = nutriments.get("sodium_100g", None)
                potassium = nutriments.get("potassium_100g", None)
                calcium = nutriments.get("calcium_100g", None)

                if cal is not None:
                    st.write(f"**Calories:** {cal:.0f} kcal")
                if fat is not None:
                    st.write(f"**Fats:** {fat:.1f} g")
                if sugars is not None:
                    st.write(f"**Sugars:** {sugars:.1f} g")
                if salt is not None:
                    st.write(f"**Salt:** {salt:.1f} g")
                if proteins is not None:
                    st.write(f"**Proteins:** {proteins:.1f} g")
                if sodium is not None:
                    st.write(f"**Sodium:** {sodium:.3f} g")
                if potassium is not None:
                    st.write(f"**Potassium:** {potassium:.0f} mg")
                if calcium is not None:
                    st.write(f"**Calcium:** {calcium:.0f} mg")

            st.markdown("**🌿 Ingredients:**")
            st.write(ingredients if ingredients else "Not available")

            if allergens:
                st.markdown("**⚠️ Allergens:**")
                for a in allergens:
                    st.markdown(f"`{a.replace('en:', '').replace('-', ' ').title()}` ", unsafe_allow_html=True)

            if labels:
                st.markdown("**🔖 Labels:**")
                for l in labels:
                    st.markdown(f"`{l.replace('en:', '').replace('-', ' ').title()}` ", unsafe_allow_html=True)

            if countries:
                st.markdown("**🌍 Countries Available:**")
                for c in countries:
                    st.markdown(f"`{c.replace('en:', '').replace('-', ' ').title()}` ", unsafe_allow_html=True)

            if categories:
                st.markdown("**🏷️ Categories:**")
                for cat in categories:
                    st.markdown(f"`{cat.replace('en:', '').replace('-', ' ').title()}` ", unsafe_allow_html=True)

        st.markdown("---")

# --- Main Action ---
if st.sidebar.button("Go"):
    with st.spinner('Loading, please wait... 🌀'):
        # Common requested fields
        requested_fields = fields + [
            "brands", "quantity", "categories_tags", "ecoscore_grade",
            "image_small_url", "countries_tags", "code", "nutriments", "nutriscore_data"
        ]

        if operation == "Fetch Product":
            if not barcode.strip():
                st.error("Please enter a barcode.")
            else:
                params = {"fields": ",".join(set(requested_fields))}
                url = f"https://world.openfoodfacts.org/api/v2/product/{barcode.strip()}"
                res = requests.get(url, params=params)
                if res.ok and res.json().get("status") == 1:
                    st.success("✅ Product found!")
                    p = res.json()["product"]
                    display_product_card(p)
                else:
                    st.error("❌ Product not found or error.")

        elif operation == "Search by Category":
            if not category.strip():
                st.error("Please enter a category.")
            else:
                category_tag = category.lower().replace(" ", "-").strip()
                params = {
                    "categories_tags_en": category_tag,
                    "fields": ",".join(set(requested_fields))
                }
                if grade:
                    params["nutrition_grades_tags"] = grade

                url = "https://world.openfoodfacts.org/api/v2/search"
                res = requests.get(url, params=params)
                if res.ok:
                    obj = res.json()
                    products = obj.get("products", [])
                    st.success(f"✅ Found {obj['count']} products")

                    if not products:
                        st.warning("⚠️ No products found. Check spelling or try a different category.")
                    else:
                        page_size = 20
                        page_number = st.number_input("Page Number", min_value=1, max_value=max(1, (len(products) - 1) // page_size + 1), step=1)
                        start_idx = (page_number - 1) * page_size
                        end_idx = start_idx + page_size

                        for p in products[start_idx:end_idx]:
                            display_product_card(p)

                else:
                    st.error("❌ Search failed.")

        elif operation == "Submit Missing Data":
            if not (barcode.strip() and uid and pwd):
                st.error("Provide barcode, user ID, and password.")
            else:
                url = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
                payload = {
                    "user_id": uid,
                    "password": pwd,
                    "code": barcode.strip(),
                    "nutriment_sodium": 0.015,
                    "nutriment_sodium_unit": "g"
                }
                res = requests.post(url, data=payload)
                if res.ok:
                    st.success("✅ Data submitted!")
                    st.json(res.json())
                else:
                    st.error("❌ Submission failed.")
