from playwright.sync_api import Page


def all_checkboxes_checked_successfully(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    initial_checked = len(page.locator("input[type='checkbox']:checked").all())

    for checkbox in page.locator("input[type='checkbox']").all():
        checkbox.scroll_into_view_if_needed()
        checkbox.check()

    final_checked = len(page.locator("input[type='checkbox']:checked").all())
    assert final_checked > initial_checked


def page_navigates_successfully(page: Page):
    response = page.goto("https://testautomationpractice.blogspot.com/")
    assert response.ok


def scrolls_checkboxes_into_view(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    checkboxes = page.locator("input[type='checkbox']").all()
    assert len(checkboxes) > 0

    for checkbox in checkboxes:
        checkbox.scroll_into_view_if_needed()
        assert checkbox.is_visible()


def handles_empty_checkbox_list(page: Page):
    page.goto("data:text/html,<html><body></body></html>")

    checkboxes = page.locator("input[type='checkbox']").all()
    assert len(checkboxes) == 0


def checks_visible_checkboxes_only(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    visible_checkboxes = page.locator("input[type='checkbox']:visible").all()

    for checkbox in visible_checkboxes:
        checkbox.scroll_into_view_if_needed()
        checkbox.check()
        assert checkbox.is_checked()


def multiple_checkbox_selections_idempotent(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    for checkbox in page.locator("input[type='checkbox']").all():
        checkbox.scroll_into_view_if_needed()
        checkbox.check()

    for checkbox in page.locator("input[type='checkbox']").all():
        assert checkbox.is_checked()
        checkbox.check()
        assert checkbox.is_checked()


def checkbox_remains_checked_after_scroll(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    checkboxes = page.locator("input[type='checkbox']").all()
    if len(checkboxes) > 0:
        first_checkbox = checkboxes[0]
        first_checkbox.check()
        first_checkbox.scroll_into_view_if_needed()
        assert first_checkbox.is_checked()

