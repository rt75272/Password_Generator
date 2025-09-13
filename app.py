import random
import string
from flask import Flask, render_template, request # type: ignore
# -------------------------------------------------------------------------------------
# Random Password Generator Web Application using Flask.

# The Flask application is created via an application factory (`create_app`) so
# the module can be imported in tests or by WSGI servers without starting the
# development server automatically.

# Usage (development):
#     $ python app.py
# -------------------------------------------------------------------------------------
def create_app():
    """Create and configure the Flask application.

    Routes are registered inside the factory so the returned `app` is ready
    to be served by a WSGI server or used in tests.
    """
    app = Flask(__name__)
    app.secret_key = 'secure_random_secret_key'
    @app.route('/', methods=['GET', 'POST'])
    def index():
        """Render the main page and handle password generation.

        On POST the selected `length` is validated and a new password is
        generated using `generate_password`. The template receives `password`
        and `length` for rendering.
        """
        password = ''
        length = 12
        if request.method == 'POST':
            try:
                # Read the requested length and clamp to allowed range.
                length = int(request.form.get('length', 12))
                length = max(6, min(length, 32))
            except ValueError:
                length = 12
            # Generate the password using the helper below.
            password = generate_password(length)
        return render_template('index.html', password=password, length=length)
    return app

def generate_password(length):
    """Return a random password containing letters, digits and a small set of symbols.

    The allowed symbol set is intentionally narrow to avoid problematic shell
    characters when copying or pasting on some platforms.
    """
    # Only allow letters, digits, and the characters: ! # $ &.
    chars = string.ascii_letters + string.digits + '!# $&'.replace(' ', '')
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    """Main driver function.

    Creates the Flask app and starts the built-in development server. For
    production use, invoke a WSGI server (gunicorn/uWSGI) and call
    ``create_app()`` to obtain the application instance.
    """
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    # The big red activation button.
    main()