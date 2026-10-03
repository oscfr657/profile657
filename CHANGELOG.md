# Changelog #

## tags ##

## commits ##

### 03 Okt 2026 ###

    docs: updated CHANGELOG
    build: version 0.5.0a0
    chore: Black
    chore: improved template code and design
    feat: added cancel button to action forms
    feat: added profile link to managed_users template
    feat: added the logged_out template to the logout url
    feat: created a profile page


### 20 Sep 2026 ###

    docs: updated CHANGELOG and README
    build: version 0.4.0a0
    chore: Black
    test: added view tests for managed_users_view and reset_delegated_password_view
    feat: added managed_users_view and reset_delegated_password_view and related urls and templates
    feat: updated CustomUserCreationForm with a trusted_manager_email
    feat: added a PasswordDelegation model and admin

### 02 Sep 2026 ###

    docs: updated CHANGELOG
    build: version 0.3.0a0
    chore: Black
    test: added view tests
    feat: added email requirement at signup
    bug: custom templates not used
    feat: added the possibility to update the email

### 27 Aug 2026 ###

    docs: updated CHANGELOG
    build: version 0.2.0a0
    chore: Black
    docs: added email settings example to README.md
    test: Changed from testing Lock model to testing Key model
    feat: Lock model is now a Key model to unlock PROFILE657_SIGNUP_LOCKED

### 12 Aug 2026 ###

    docs: updated CHANGELOG
    build: version 0.1.0a0
    chore: Black
    chore: small improvements of README
    chore: increased required python version to 12
    feat: made the views and utils Site aware
    test: created model tests
    feat: added ForeignKey Site to Lock model

### 08 Aug 2026 ###

    docs: created a CHANGELOG
    build: version 0.0.1a0
    chore: Black
    doc: created a README.md and pyproject.toml
    fix: PROFILE657_SIGNUP_LOCKED is default true
    feature: created urls.py
    feature: created login and signup views and templates
    feature: crated a utils.py with a get_current_lock function
    feature: created a Lock model and ModelAdmin
    feature: created a Django app with password_reset templates and empty tests
    ci: first commit: license, .gitignore and requirements.
