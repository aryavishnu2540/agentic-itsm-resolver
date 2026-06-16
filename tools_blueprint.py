import json

def load_db():
    with open("database.json", "r") as f:
        return json.load(f)

def save_db(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)

def reset_user_password(employee_id):
    """Real backend function to unlock a user account in the JSON database."""
    db = load_db()
    for user in db["users"]:
        if user["employee_id"] == employee_id:
            user["account_locked"] = False
            save_db(db)
            return f"SUCCESS: Account for {employee_id} has been unlocked."
    return "ERROR: Employee ID not found."

def provision_cloud_db(employee_id):
    """Real backend function to provision a database for a user."""
    db = load_db()
    for user in db["users"]:
        if user["employee_id"] == employee_id:
            user["has_database"] = True
            save_db(db)
            return f"SUCCESS: Database successfully provisioned for {employee_id}."
    return "ERROR: Employee ID not found."