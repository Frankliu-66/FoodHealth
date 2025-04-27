import streamlit as st
import requests

st.set_page_config("🍽️ Food Risk Detector", layout="wide")
st.title("🍽️ Open Food Facts UI")

# --- Sidebar ---
st.sidebar.header("Configure Query")
barcode = st.sidebar.text_input("Product Barcode", "")
fields = st.sidebar.multiselect(
    "Fields to retrieve",
    ["product_name", "nutrition_grades", "nutriments", "nutriscore_data", "misc_tags"],
    default=["product_name", "nutrition_grades"]
)
operation = st.sidebar.radio("Operation", ["Fetch Product", "Search by Category", "Submit Missing Data"])

# Additional inputs
if operation == "Search by Category":
    category = st.sidebar.text_input("Category (e.g. Orange Juice)", "")
    grade = st.sidebar.selectbox("Nutrition Grade", ["a","b","c","d","e"])
elif operation == "Submit Missing Data":
    uid = st.sidebar.text_input("User ID", "")
    pwd = st.sidebar.text_input("Password", type="password")

# --- Action ---
if st.sidebar.button("Go"):
    if operation == "Fetch Product":
        if not barcode:
        st.error("Please enter a barcode.")
    else:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"  # 注意.org
        params = {"fields": ",".join(fields)}
        res = requests.get(url, params=params)
        if res.ok and res.json().get("status") == 1:
            st.success("Product found!")
            data = res.json()["product"]
            for key in fields:
                st.subheader(key.replace("_"," ").title())
                st.json(data.get(key))
        else:
            st.error("Product not found or error.")


    elif operation == "Search by Category":
        if not category:
            st.error("Please enter a category.")
        else:
            url = "https://world.openfoodfacts.org/api/v2/search"
            params = {
                "categories_tags_en": category,
                "nutrition_grades_tags": grade,
                "fields": "code,product_name,nutrition_grades"
            }
            res = requests.get(url, params=params)
            obj = res.json()
            st.write(f"Found {obj['count']} products")
            st.json(obj["products"])

    elif operation == "Submit Missing Data":
        if not (barcode and uid and pwd):
            st.error("Provide barcode, user ID, and password.")
        else:
            url = "https://world.openfoodfacts.net/cgi/product_jqm2.pl"
            payload = {
                "user_id": uid, "password": pwd, "code": barcode,
                # example: posting sodium
                "nutriment_sodium": 0.015,
                "nutriment_sodium_unit": "g"
            }
            res = requests.post(url, data=payload)
            if res.ok:
                st.success("Data submitted!")
                st.json(res.json())
            else:
                st.error("Submission failed.")
