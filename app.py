import streamlit as st
import datetime
import pandas as pd

from logic import add_expense, get_all_expenses, add_income, get_all_incomes
from models import Budget, Income
from db import Session

st.title("💰 Personal Finance Tracker")

# ➕ Add New Expense
st.header("➕ Add New Expense")
amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="expense_amount")
category = st.selectbox("Category", ["Food", "Transport", "Health", "Shopping", "Others"], key="expense_category")
date = st.date_input("Date", value=datetime.date.today(), key="expense_date")

if st.button("Add Expense"):
    add_expense(amount, category, date)
    st.success("✅ Expense added!")

# 📋 Expense History
st.header("📋 Expense History")
expenses = get_all_expenses()

# For tracking current month/year
today = datetime.datetime.today()
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

    # 🧾 Spending by Category
    st.subheader("🧾 Spending by Category")
    category_summary = df.groupby("category")["amount"].sum().reset_index()
    st.bar_chart(category_summary.set_index("category"))

    # 📅 Monthly Spending
    df["month_str"] = pd.to_datetime(df["date"]).dt.strftime("%B")
    monthly_summary = df.groupby("month_str")["amount"].sum().reset_index()
    st.subheader("📅 Monthly Spending")
    st.line_chart(monthly_summary.set_index("month_str"))

else:
    st.info("No expenses recorded yet.")
    total_spent = 0.0

# 💸 Budget Section (Always Visible)
st.subheader("💸 Set Your Monthly Budget")

budget_input = st.number_input("Enter Monthly Budget ($)", min_value=0.0, step=50.0, key="budget_input")

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

# Query Budget for current month/year
session = Session()
budget = session.query(Budget).filter_by(month=month, year=year).first()
session.close()

budget_amount = budget.amount if budget else 0.0

if budget:
    remaining_budget = budget_amount - total_spent
    st.subheader("📊 Budget Overview")
    st.metric("Monthly Budget", f"${budget_amount:.2f}")
    st.metric("Remaining Budget", f"${remaining_budget:.2f}", delta=f"${-remaining_budget:.2f}" if remaining_budget < 0 else f"${remaining_budget:.2f}")
else:
    st.warning("⚠️ No budget set for this month yet.")

# ➕ Add New Income
st.header("➕ Add New Income")
income_amount = st.number_input("Income Amount ($)", min_value=0.0, step=50.0, key="income_amount")
income_source = st.text_input("Income Source (e.g., Salary, Freelance)", value="Salary", key="income_source")
income_month = st.selectbox("Income Month", [datetime.date(1900, i, 1).strftime('%B') for i in range(1, 13)], index=today.month - 1, key="income_month")
income_year = st.number_input("Income Year", min_value=2000, max_value=2100, value=today.year, step=1, key="income_year")

if st.button("Add Income"):
    add_income(income_amount, income_source, income_month, income_year)
    st.success("✅ Income added!")

# 📋 Income History
st.header("📋 Income History")
incomes = get_all_incomes()

if incomes:
    income_df = pd.DataFrame([i.__dict__ for i in incomes])
    income_df = income_df.drop(columns=["_sa_instance_state"])

    st.dataframe(income_df)

    # Total Income for current month and year
    current_income = income_df[(income_df['month'] == month) & (income_df['year'] == year)]
    if not current_income.empty:
        total_income = current_income["amount"].sum()
        st.subheader("📈 Income Summary")
        st.metric("Total Income", f"${total_income:.2f}")

        # Money Left = Income - Expenses (current month)
        money_left = total_income - total_spent
        st.subheader("💰 Money Left After Expenses")
        st.metric("Remaining Amount", f"${money_left:.2f}", delta=f"${-money_left:.2f}" if money_left < 0 else f"${money_left:.2f}")

        # Alerts
        if budget_amount > 0 and total_spent > budget_amount:
            st.error("🚨 You have exceeded your budget!")
        if money_left < 0:
            st.warning("⚠️ You are spending more than your income!")
    else:
        st.info("No income recorded for current month and year.")
else:
    st.info("No income records found yet.")
