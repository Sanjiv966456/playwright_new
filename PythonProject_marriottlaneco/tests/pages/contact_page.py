from .base_page import BasePage

class ContactPage(BasePage):
    FORM_SELECTORS = [
        ("input[type=\"text\"]", "name"),
        ("input[type=\"email\"]", "email"),
        ("textarea", "message"),
    ]

    def goto_contact(self):
        return self.goto("/contact/")

    def submit_contact_form(self, name: str, email: str, message: str) -> bool:
        # Try to fill common form fields if present
        try:
            # name
            name_input = self.page.query_selector("input[name*='name'], input[id*='name']")
            email_input = self.page.query_selector("input[type='email'], input[name*='email']")
            message_input = self.page.query_selector("textarea[name*='message'], textarea[id*='message']")

            if name_input:
                name_input.fill(name)
            if email_input:
                email_input.fill(email)
            if message_input:
                message_input.fill(message)

            # try to submit via button
            submit = self.page.query_selector("button[type='submit'], input[type='submit'], button:has-text('Send'), button:has-text('Submit')")
            if submit:
                submit.click()
                # wait for navigation or success message
                self.page.wait_for_timeout(1500)
                return True
        except Exception:
            return False
        return False

