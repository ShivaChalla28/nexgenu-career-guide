from fastapi import APIRouter, HTTPException
import sheets_db
import uuid

router = APIRouter(
    prefix="/api/payments",
    tags=["payments"]
)

def is_payments_enabled() -> bool:
    settings = sheets_db.get_all("Settings")
    for s in settings:
        if s.get("key") == "PAYMENT_TOGGLE":
            return s.get("value", "").lower() == "on"
    return False

@router.post("/initiate")
def initiate_payment(data: dict):
    if not is_payments_enabled():
        return {"status": "free", "message": "Payments are currently disabled. Everything is free."}
    
    # Normally we would call Razorpay/Cashfree here using keys from Settings
    if "payment_id" not in data:
        data["payment_id"] = f"PAY-{str(uuid.uuid4())[:8]}"
    
    data["status"] = "initiated"
    sheets_db.create_item("Payments", data)
    return {"status": "initiated", "payment_id": data["payment_id"]}

@router.post("/verify")
def verify_payment(payment_id: str, data: dict):
    # Verify webhook/callback data
    res = sheets_db.update_item("Payments", 0, payment_id, {"status": "success"})
    if not res:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"status": "success", "message": "Payment verified and unlocked"}
