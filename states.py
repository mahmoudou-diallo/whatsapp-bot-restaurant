user_states = {}
user_data = {}

def get_state(phone):
    return user_states.get(phone, "start")

def set_state(phone, state):
    user_states[phone] = state

def get_data(phone):
    if phone not in user_data:
        user_data[phone] = {}
    return user_data[phone]

def set_data(phone, key, value):
    if phone not in user_data:
        user_data[phone] = {}
    user_data[phone][key] = value

def reset(phone):
    user_states[phone] = "start"
    user_data[phone] = {}
