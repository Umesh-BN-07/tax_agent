from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from tax_engine import TaxCalculator
from deduction import DeductionCalculator
from agent import chat_agent

# Store user states
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data_store[user_id] = {"step": 0}
    await update.message.reply_text("👋 Welcome to Tax Guide Bot!\nEnter your salary:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data_store:
        user_data_store[user_id] = {"step": 0}

    data = user_data_store[user_id]

    # STEP 0 → Salary
    if data["step"] == 0:
        data["income"] = int(text)
        data["step"] = 1
        await update.message.reply_text("📉 Enter 80C investment:")
    
    # STEP 1 → 80C
    elif data["step"] == 1:
        data["80C"] = int(text)
        data["step"] = 2
        await update.message.reply_text("🏥 Enter 80D insurance:")
    
    # STEP 2 → 80D
    elif data["step"] == 2:
        data["80D"] = int(text)
        data["step"] = 3
        await update.message.reply_text("⚙️ Enter regime (old/new):")
    
    # STEP 3 → Calculate
    elif data["step"] == 3:
        regime = text.lower()
        data["regime"] = regime

        investments = {"80C": data["80C"], "80D": data["80D"]}
        deduction_calc = DeductionCalculator(investments)

        if regime == "old":
            total_deduction = deduction_calc.total_deductions()
        else:
            total_deduction = 0

        tax = TaxCalculator(data["income"], total_deduction, regime).calculate_tax()

        response = chat_agent(data, tax, regime)

        await update.message.reply_text(f"🧾 Tax: ₹{tax}\n\n{response}")

        data["step"] = 0  # reset

# Run bot
def main():
    TOKEN = "8645796955:AAHzrYL5SlA7KP-Ecoj_Xthy7dAI5mKSQws"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()