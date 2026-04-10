import streamlit as st
from tax_engine import TaxCalculator
from deduction import DeductionCalculator
from agent import chat_agent
from report import generate_pdf

st.set_page_config(page_title="Tax Guide Agent", layout="centered")

st.title("💬 Tax Guide Agent ")

# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}

# STEP 1 - Salary
if st.session_state.step == 0:
    with st.form("salary_form"):
        st.subheader("💰 Step 1: Enter Salary")
        salary = st.number_input("Annual Salary (₹)", min_value=0)
        submit = st.form_submit_button("Next")

        if submit:
            st.session_state.data["income"] = salary
            st.session_state.step = 1
            st.rerun()

# STEP 2 - 80C
elif st.session_state.step == 1:
    with st.form("80c_form"):
        st.subheader("📉 Step 2: 80C Investment")
        invest_80C = st.number_input("80C Amount (₹)", min_value=0)
        submit = st.form_submit_button("Next")

        if submit:
            st.session_state.data["80C"] = invest_80C
            st.session_state.step = 2
            st.rerun()

# STEP 3 - 80D
elif st.session_state.step == 2:
    with st.form("80d_form"):
        st.subheader("🏥 Step 3: Health Insurance")
        invest_80D = st.number_input("80D Amount (₹)", min_value=0)
        submit = st.form_submit_button("Next")

        if submit:
            st.session_state.data["80D"] = invest_80D
            st.session_state.step = 3
            st.rerun()

# STEP 4 - Regime
elif st.session_state.step == 3:
    with st.form("regime_form"):
        st.subheader("⚙️ Step 4: Choose Regime")
        regime = st.selectbox("Tax Regime", ["new", "old"])
        submit = st.form_submit_button("Calculate")

        if submit:
            st.session_state.data["regime"] = regime
            st.session_state.step = 4
            st.rerun()

# STEP 5 - Results
elif st.session_state.step == 4:

    data = st.session_state.data
    investments = {"80C": data["80C"], "80D": data["80D"]}
    deduction_calc = DeductionCalculator(investments)

    if data["regime"] == "old":
        total_deduction = deduction_calc.total_deductions()
    else:
        total_deduction = 0

    tax = TaxCalculator(data["income"], total_deduction, data["regime"]).calculate_tax()

    old_tax = TaxCalculator(data["income"], deduction_calc.total_deductions(), "old").calculate_tax()
    new_tax = TaxCalculator(data["income"], 0, "new").calculate_tax()

    st.success("✅ Calculation Complete!")

    st.subheader("📊 Results")
    st.write(f"💰 Income: ₹{data['income']}")
    st.write(f"🧾 Tax: ₹{tax}")

    st.subheader("⚖️ Comparison")
    st.write(f"Old: ₹{old_tax}")
    st.write(f"New: ₹{new_tax}")

    if old_tax < new_tax:
        st.success("Old regime is better")
    else:
        st.success("New regime is better")

    st.subheader("🤖 Assistant")
    st.write(chat_agent(data, tax, data["regime"]))

    # ✅ PDF button (FIXED POSITION)
    # Generate PDF
if st.button("📄 Generate Tax Report"):
    file_path = generate_pdf(
        data,
        tax,
        data["regime"],
        old_tax,
        new_tax
    )
    st.session_state.file_path = file_path

# Download button (safe)
if "file_path" in st.session_state:
    with open(st.session_state.file_path, "rb") as f:
        st.download_button(
            label="⬇️ Download PDF",
            data=f,
            file_name="Tax_Report.pdf",
            mime="application/pdf"
        )

    # ✅ Restart button (FIXED POSITION)
    if st.button("🔄 Restart"):
        st.session_state.step = 0
        st.session_state.data = {}
        st.rerun()
