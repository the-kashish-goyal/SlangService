import re


class Response:
    @classmethod
    def validate_response(cls,name, monthly_income, monthly_savings, phone_no, email):
        errors = []
        # Rule 1: income vs savings
        if monthly_savings > monthly_income:
            errors.append("Monthly savings cannot be less than Monthly income")

        # Rule 2: email validity
        if not email:
            errors.append("Email is required")
        else:
            email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')  # Stricter email validation
            if not email_pattern.match(email):
                errors.append("Invalid email format. Please enter a valid email address.")

        # Rule 3: phone number validity
        if not phone_no:
            errors.append("Phone number is required")
        else:
            phone_pattern = re.compile(r'^\d{10}$')  # Phone number must be exactly 10 digits
            if not phone_pattern.match(phone_no):
                errors.append("Invalid phone number format. It must be exactly 10 digits and contain only digits.")
        # Rule 4:
        if not name:
            errors.append("Name is required")
        return errors
