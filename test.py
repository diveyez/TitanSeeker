import bard

predicted_price = bard.finance_bard()
if predicted_price is not None:
    print(f"Predicted price: {predicted_price:.2f}")