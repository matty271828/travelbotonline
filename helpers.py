import os

from flask import redirect, render_template, request, session
from functools import wraps

# Thanks to CS50
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Thanks to CS50
def gbp(value):
    """Format value as GBP."""
    try:
        return f"£{value:,.2f}"
    except:
        return None