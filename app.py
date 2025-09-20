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

        The form posts back to this route to request a new password length.
        """
        passwords = []
        length = 12 # Standrd default length
        if request.method == 'POST':
            try:
                length = int(request.form.get('length', 12))
                length = max(6, min(length, 32))
            except ValueError:
                length = 12
            passwords = generate_multiple_passwords(length)
        return render_template('index.html', passwords=passwords, length=length)
    return app

def generate_password(length):
    """Return a random password containing letters, digits and a small set of symbols.

    The allowed symbol set is intentionally narrow to avoid problematic shell
    characters when copying or pasting on some platforms.
    """
    # Only allow letters, digits, and the characters: ! # $ &.
    chars = string.ascii_letters + string.digits + '!# $&'.replace(' ', '')
    return ''.join(random.choice(chars) for _ in range(length))

def check_password_strength(password):
    """Evaluate password strength and return rating with details.
    
    Returns a dictionary with:
    - strength: 'weak', 'medium', or 'strong'
    - score: numeric score (0-100)
    - details: list of criteria met/not met
    """
    score = 0
    details = []
    # Length criteria
    if len(password) >= 12:
        score += 25
        details.append("✓ Good length (12+ characters)")
    elif len(password) >= 8:
        score += 15
        details.append("○ Adequate length (8+ characters)")
    else:
        details.append("✗ Too short (less than 8 characters)")
    # Character type criteria
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in '!#$&' for c in password)
    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    if char_types >= 4:
        score += 30
        details.append("✓ All character types (upper, lower, digits, symbols)")
    elif char_types >= 3:
        score += 20
        details.append("○ Multiple character types")
    elif char_types >= 2:
        score += 10
        details.append("○ Some character variety")
    else:
        details.append("✗ Limited character types")
    # Complexity bonuses
    if len(password) >= 16:
        score += 15
        details.append("✓ Very long password")
    if has_symbol and char_types >= 3:
        score += 10
        details.append("✓ Good symbol usage")
    # Determine strength level
    if score >= 70:
        strength = 'strong'
    elif score >= 40:
        strength = 'medium'
    else:
        strength = 'weak'
    return {
        'strength': strength,
        'score': score,
        'details': details
    }

def generate_multiple_passwords(length):
    """Generate multiple password options with different strategies.
    
    Returns a list of dictionaries, each containing:
    - password: the generated password
    - strategy: description of generation strategy
    - strength_info: result from check_password_strength()
    """
    passwords = []
    # Strategy 1: Balanced mix (original algorithm)
    chars = string.ascii_letters + string.digits + '!#$&'
    password1 = ''.join(random.choice(chars) for _ in range(length))
    passwords.append({
        'password': password1,
        'strategy': 'Balanced Mix',
        'strength_info': check_password_strength(password1)
    })
    # Strategy 2: Pronounceable with syllables
    password2 = generate_pronounceable_password(length)
    passwords.append({
        'password': password2,
        'strategy': 'Pronounceable',
        'strength_info': check_password_strength(password2)
    })
    # Strategy 3: Word-based pronounceable
    if length >= 8:
        password3 = generate_word_based_password(length)
        passwords.append({
            'password': password3,
            'strategy': 'Word-Based',
            'strength_info': check_password_strength(password3)
        })
    # Strategy 4: Symbol-rich for maximum security
    if length >= 8:  # Only for longer passwords
        symbol_rich_chars = string.ascii_letters + string.digits + '!#$&' * 2
        password4 = ''.join(random.choice(symbol_rich_chars) for _ in range(length))
        passwords.append({
            'password': password4,
            'strategy': 'Symbol Rich',
            'strength_info': check_password_strength(password4)
        })
    # Strategy 5: Easy to type (fewer special characters)
    easy_chars = string.ascii_letters + string.digits + '!#'
    password5 = ''.join(random.choice(easy_chars) for _ in range(length))
    passwords.append({
        'password': password5,
        'strategy': 'Easy to Type',
        'strength_info': check_password_strength(password5)
    })
    return passwords

def generate_pronounceable_password(length):
    """Generate a highly pronounceable password using realistic syllable patterns."""
    # More natural consonants (avoiding hard-to-pronounce combinations)
    consonants = 'bdfghjklmnprstvwz'  # Removed c, q, x, y for better flow
    vowels = 'aeiou'
    # Common consonant clusters that are easy to pronounce
    clusters = [
        'br', 
        'cr', 
        'dr', 
        'fr', 
        'gr', 
        'pr', 
        'tr', 
        'bl', 
        'cl', 
        'fl', 
        'gl', 
        'pl', 
        'sl', 
        'st', 
        'sp', 
        'sc', 
        'sk', 
        'sm', 
        'sn', 
        'sw'
    ]
    digits = '23456789'  # Avoid 0, 1 which can be confused with letters
    symbols = '!#$&'
    password = []
    i = 0
    # Reserve space for required security elements
    required_extras = []
    if length >= 10:
        required_extras.extend([random.choice(digits), random.choice(symbols)])
    elif length >= 8:
        required_extras.append(random.choice(digits))
    syllable_count = 0
    target_syllables = max(2, (length - len(required_extras)) // 3)
    # Generate syllables (consonant-vowel or cluster-vowel patterns)
    while syllable_count < target_syllables and i < length - len(required_extras):
        # Start syllable - use consonant cluster occasionally for variety
        if random.random() < 0.3 and i < length - len(required_extras) - 2:
            # Use consonant cluster
            cluster = random.choice(clusters)
            password.extend(list(cluster))
            i += len(cluster)
        else:
            # Single consonant
            consonant = random.choice(consonants)
            password.append(consonant)
            i += 1
        # Add vowel if there's space
        if i < length - len(required_extras):
            vowel = random.choice(vowels)
            password.append(vowel)
            i += 1
        # Occasionally add another vowel for diphthongs (like 'ai', 'ou')
        if random.random() < 0.2 and i < length - len(required_extras):
            vowel2 = random.choice(vowels)
            if vowel2 != password[-1]:  # Don't repeat the same vowel
                password.append(vowel2)
                i += 1
        syllable_count += 1
    # Fill remaining space with simple consonant-vowel if needed
    while i < length - len(required_extras):
        if i % 2 == 0:
            password.append(random.choice(consonants))
        else:
            password.append(random.choice(vowels))
        i += 1
    # Capitalize the first letter and randomly capitalize other syllable starts
    if password:
        password[0] = password[0].upper()
        # Find syllable boundaries and randomly capitalize
        for idx in range(2, len(password), 3):
            if idx < len(password) and random.random() < 0.4:
                password[idx] = password[idx].upper()
    # Add security elements at natural break points
    if required_extras:
        # Insert at syllable boundaries when possible
        for extra in required_extras:
            if len(password) >= 3:
                # Insert at position that doesn't break syllable flow too much
                insert_pos = len(password) - random.randint(0, 2)
                password.insert(insert_pos, extra)
            else:
                password.append(extra)
    result = ''.join(password)
    return result[:length]  # Ensure we don't exceed length

def generate_word_based_password(length):
    """Generate a password using realistic words and natural patterns."""
    # More pronounceable and common word components
    common_words = [
        'blue', 'fire', 'moon', 'star', 'tree', 'rock', 'wave', 'wind', 
        'bird', 'fish', 'bear', 'wolf', 'lion', 'tiger', 'eagle', 'shark',
        'gold', 'iron', 'ruby', 'jade', 'rose', 'lily', 'sage', 'mint',
        'swift', 'brave', 'calm', 'wise', 'kind', 'bold', 'free', 'pure'
    ]
    syllable_words = [
        'ama-zing', 'beau-ti-ful', 'won-der-ful', 'fan-tas-tic', 'magi-cal',
        'dyna-mic', 'crea-tive', 'ele-gant', 'bril-liant', 'glo-ri-ous',
        'har-mo-ny', 'melo-dy', 'sym-pho-ny', 'rhap-so-dy', 'sere-nade',
        'cas-cade', 'mira-cle', 'para-dise', 'trea-sure', 'adven-ture'
    ]
    # Easy to pronounce prefixes and suffixes
    prefixes = ['sun', 'moon', 'star', 'sea', 'sky', 'fire', 'ice', 'wind']
    suffixes = ['song', 'dance', 'wave', 'light', 'dream', 'magic', 'power', 'force']
    password_parts = []
    current_length = 0
    # Choose base word strategy based on length
    if length <= 8:
        # Use simple common words
        word = random.choice(common_words)
        word = word.capitalize()
        password_parts.append(word)
        current_length += len(word)
    elif length <= 12:
        # Use compound words
        word1 = random.choice(prefixes)
        word2 = random.choice(suffixes)
        compound = word1.capitalize() + word2
        password_parts.append(compound)
        current_length += len(compound)
    else:
        # Use longer syllable-based words (remove hyphens)
        word = random.choice(syllable_words).replace('-', '')
        word = word.capitalize()
        password_parts.append(word)
        current_length += len(word)
    # Add meaningful numbers (years, ages, etc.)
    remaining_space = length - current_length
    if remaining_space >= 2:
        # Use years, ages, or other meaningful numbers
        meaningful_nums = [
            str(random.randint(20, 99)),  # Age-like numbers
            str(random.randint(2020, 2030)),  # Recent years
            str(random.randint(100, 999)),  # Round numbers
        ]
        if remaining_space >= 4:
            num = random.choice(meaningful_nums[1:])  # Use longer numbers
        else:
            num = meaningful_nums[0]  # Use 2-digit numbers
        password_parts.append(num)
        current_length += len(num)
    elif remaining_space >= 1:
        # Single digit
        password_parts.append(str(random.randint(2, 9)))
        current_length += 1
    # Add symbol at the end if there's space
    if current_length < length:
        symbol = random.choice('!#&')  # Removed $ as it's less common
        password_parts.append(symbol)
        current_length += 1
    # Fill any remaining space with vowels (easy to pronounce)
    while current_length < length:
        filler = random.choice('aeiou')
        password_parts.append(filler)
        current_length += 1
    # Join and ensure correct length
    password = ''.join(password_parts)
    return password[:length]

def main():
    """Main driver function.

    Creates the Flask app and starts the built-in development server. For
    production use, invoke a WSGI server (gunicorn/uWSGI) and call
    ``create_app()`` to obtain the application instance.
    """
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    """The big red activation button."""
    main()

# Expose the WSGI application at module level for servers like gunicorn.
# This allows a command like `gunicorn app:app` in Render to work.
app = create_app()