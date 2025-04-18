import streamlit as st

st.set_page_config(page_title="🍽️ Food Risk Detection", layout="centered")

st.title("🍽️ Food Risk Detection System")

# User input for food information
food_name = st.text_input("Enter food name (e.g., milk, sausage, salad)")
ingredients = st.text_area("Enter ingredient list (optional)")

# Risk type selector
risk_type = st.selectbox(
    "Select type of risk to detect",
    ["Allergy Risk", "Health Risk", "Expiration Risk", "Food Poisoning Risk"]
)

# Simulate analysis
if st.button("Analyze"):
    if not food_name:
        st.warning("Please enter a food name.")
    else:
        # Simulated result (you can connect your model later)
        st.subheader("✅ Analysis Result")
        st.write(f"**Food Name:** {food_name}")
        st.write(f"**Risk Type:** {risk_type}")
        st.write("**Risk Level:** ⚠️ Moderate Risk")
        st.write("**Explanation:** This food may contain allergens such as lactose or peanuts.")
        st.write("**Suggestion:** Avoid if you have food allergies.")

        # Simulated risk score bar
        st.progress(60)  # Example: risk score of 60%
