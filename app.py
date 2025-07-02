import streamlit as st
from logic import add_expense, get_all_expenses
import datetime
import pandas as pd
from models import Budget
from db import Session

st.title("💰 Personal Finance Tracker")

# ➕ Add New Expense
st.header("➕ Add New Expense")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox("Category", ["Food", "Transport", "Health", "Shopping", "Others"])
date = st.date_input("Date", value=datetime.date.today())

if st.button("Add Expense"):
    add_expense(amount, category, date)
    st.success("✅ Expense added!")

# 📋 Expense History
st.header("📋 Expense History")
expenses = get_all_expenses()

# For tracking current month/year
from datetime import datetime
today = datetime.today()
month = today.strftime("%B")
year = today.year

if expenses:
    df = pd.DataFrame([e.__dict__ for e in expenses])
    df = df.drop(columns=["_sa_instance_state"])
    st.dataframe(df)

    # 📈 Expense Summary
    st.subheader("📈 Expense Summary")
    total_spent = df["amount"].sum()
    st.metric("Total Spent", f"${total_spent:.2f}")

    # ✅ Compare with Budget
    session = Session()
    budget = session.query(Budget).filter_by(month=month, year=year).first()
    session.close()

    if budget:
        remaining = budget.amount - total_spent
        st.subheader("📊 Budget Overview")
        st.metric("Monthly Budget", f"${budget.amount:.2f}")
        st.metric("Remaining Budget", f"${remaining:.2f}", delta=f"${-remaining:.2f}" if remaining < 0 else f"${remaining:.2f}")
    else:
        st.warning("⚠️ No budget set for this month yet.")

    # 🧾 Category Summary
    st.subheader("🧾 Spending by Category")
    category_summary = df.groupby("category")["amount"].sum().reset_index()
    st.bar_chart(category_summary.set_index("category"))

    # 📅 Monthly Summary
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    monthly_summary = df.groupby("month")["amount"].sum().reset_index()
    st.subheader("📅 Monthly Spending")
    st.line_chart(monthly_summary.set_index("month"))

else:
    st.info("No expenses recorded yet.")

# 💸 Set Budget (ALWAYS visible)
st.subheader("💸 Set Your Monthly Budget")

budget_input = st.number_input("Enter Monthly Budget ($)", min_value=0.0, step=50.0)

if st.button("Save Budget"):
    session = Session()
    existing = session.query(Budget).filter_by(month=month, year=year).first()
    if existing:
        existing.amount = budget_input
    else:
        session.add(Budget(month=month, year=year, amount=budget_input))
    session.commit()
    session.close()
    st.success("✅ Budget Saved!")
