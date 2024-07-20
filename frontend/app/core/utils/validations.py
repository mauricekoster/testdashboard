def confirm_password_rules(get_values, value):
    values = get_values()
    return values["new_password"] == values["confirm_password"]
