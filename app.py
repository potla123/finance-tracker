import streamlit as st
from logic import add_expense, get_all_expenses
import datetime
import pandas as pd

st.title("💰 Personal Finance Tracker")

# Form to add expense
st.header("➕ Add New Expense")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox("Category", ["Food", "Transport", "Health", "Shopping", "Others"])
date = st.date_input("Date", value=datetime.date.today())

if st.button("Add Expense"):
    add_expense(amount, category, date)
    st.success("Expense added!")

# View past expenses
st.header("📋 Expense History")
expenses = get_all_expenses()

if expenses:
    df = pd.DataFrame([e.__dict__ for e in expenses])
    df = df.drop(columns=["_sa_instance_state"])
    st.dataframe(df)

    # ✅ Move this inside the IF block (indented correctly)
    st.subheader("📈 Expense Summary")

    total_spent = df["amount"].sum()
    st.metric("Total Spent", f"${total_spent:.2f}")

    # Category-wise summary
    st.subheader("🧾 Spending by Category")
    category_summary = df.groupby("category")["amount"].sum().reset_index()
    st.bar_chart(category_summary.set_index("category"))

    # Monthly summary
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    monthly_summary = df.groupby("month")["amount"].sum().reset_index()
    st.subheader("📅 Monthly Spending")
    st.line_chart(monthly_summary.set_index("month"))

else:
    st.info("No expenses recorded yet.")
