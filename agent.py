def chat_agent(user_data, tax, regime):
    income = user_data.get("income", 0)
    invest_80C = user_data.get("80C", 0)
    invest_80D = user_data.get("80D", 0)

    response = "🤖 Tax Guide Agent (FY 2025-26)\n\n"
    response += f"💰 Income: ₹{income}\n"
    response += f"🧾 Estimated Tax: ₹{tax}\n"
    response += f"⚙️ Regime: {regime.upper()}\n\n"

    # Slabs
    if regime == "new":
        response += """📊 New Regime Slabs:
0-4L: 0%
4-8L: 5%
8-12L: 10%
12-16L: 15%
16-20L: 20%
20-24L: 25%
Above 24L: 30%
"""
    else:
        response += """📊 Old Regime Slabs:
0-2.5L: 0%
2.5-5L: 5%
5-10L: 20%
Above 10L: 30%
"""

    # Deduction logic
    if regime == "old":
        response += "\n📉 Deduction Analysis:\n"
        response += f"• 80C used: ₹{invest_80C}/150000\n"
        response += f"• 80D used: ₹{invest_80D}\n"

        if invest_80C < 150000:
            response += f"⚠️ Invest ₹{150000 - invest_80C} more in 80C\n"
        else:
            response += "✅ 80C fully utilized\n"

        if invest_80D == 0:
            response += "⚠️ Consider health insurance under 80D\n"
        else:
            response += "✅ 80D benefit applied\n"

    else:
        response += """
📉 Deduction Note (New Regime):
⚠️ 80C and 80D deductions are NOT applicable
✔️ Only standard deduction ₹50,000 is considered
"""

    # ITR steps
    response += """
🗣️ ITR Filing Steps:
1. Go to Income Tax Portal
2. Login with PAN
3. Select ITR-1
4. Enter salary details
5. Add deductions
6. Verify using Aadhaar OTP
7. Submit return

✅ ITR Filed Successfully!
"""

    return response