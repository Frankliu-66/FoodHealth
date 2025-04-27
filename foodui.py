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
    grade = st.sidebar.selectbox("Nutrition Grade", ["a", "b", "c", "d", "e"])
elif operation == "Submit Missing Data":
    uid = st.sidebar.text_input("User ID", "")
    pwd = st.sidebar.text_input("Password", type="password")

# --- Action ---
if st.sidebar.button("Go"):
    if operation == "Fetch Product":
        if not barcode.strip():
            st.error("Please enter a barcode.")
        else:
            url = f"https://world.openfoodfacts.org/api/v2/product/{barcode.strip()}"  # 注意.org
            params = {"fields": ",".join(fields)}
            res = requests.get(url, params=params)
            if res.ok and res.json().get("status") == 1:
                st.success("✅ Product found!")
                data = res.json()["product"]

                # --- Improved Output ---
                st.subheader(f"📦 Product: {data.get('product_name', 'Unknown')}")
                info = {}

                for key in fields:
                    value = data.get(key)
                    if isinstance(value, (dict, list)):
                        # 复杂结构展开查看
                        with st.expander(f"🔍 {key.replace('_', ' ').title()} (Click to Expand)"):
                            st.json(value)
                    else:
                        # 简单结构收集
                        info[key.replace("_", " ").title()] = value

                # 展示简单信息
                if info:
                    st.markdown("---")
                    st.markdown("### 📋 Product Info")
                    for k, v in info.items():
                        st.write(f"**{k}:** {v if v is not None else 'N/A'}")

            else:
                st.error("❌ Product not found or error.")

    elif operation == "Search by Category":
        if not category.strip():
            st.error("Please enter a category.")
        else:
            url = "https://world.openfoodfacts.org/api/v2/search"
            params = {
                "categories_tags_en": category.strip(),
                "nutrition_grades_tags": grade,
                "fields": "code,product_name,nutrition_grades"
            }
            res = requests.get(url, params=params)
            if res.ok:
                obj = res.json()
                st.success(f"✅ Found {obj['count']} products")
                st.json(obj["products"])
            else:
                st.error("❌ Search failed.")

    elif operation == "Submit Missing Data":
        if not (barcode.strip() and uid and pwd):
            st.error("Provide barcode, user ID, and password.")
        else:
            url = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"  # 注意.org
            payload = {
                "user_id": uid,
                "password": pwd,
                "code": barcode.strip(),
                # Example: posting sodium
                "nutriment_sodium": 0.015,
                "nutriment_sodium_unit": "g"
            }
            res = requests.post(url, data=payload)
            if res.ok:
                st.success("✅ Data submitted!")
                st.json(res.json())
            else:
                st.error("❌ Submission failed.")
