import random

def recognize_face(live_input_id):
    """
    Simulates facial recognition by checking if a provided face (customer ID or input ID)
    matches the actual user ID. 
    There's a 90% chance of successful recognition, and 10% chance it fails.

    Parameters:
        live_input_id (str): The simulated input, like a customer ID

    Returns:
        str or None: The recognized customer ID if successful, or None if recognition fails
    """
    print("🔍 Simulating face recognition...")

    # Simulate recognition success or failure
    success_chance = 0.9  # 90% chance to recognize the face
    if random.random() < success_chance:
        print("✅ Face recognized.")
        return live_input_id
    else:
        print("❌ Face recognition failed.")
        return None
