from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Accepts common formats: local (e.g. 01xxxxxxxxx), +20…, spaces/dashes.
    Requires 8–15 digits (ITU-T E.164 max is 15 digits).
    """
    if value is None:
        return
    stripped = value.strip()
    if not stripped:
        raise ValidationError('Phone number is required.')

    allowed_chars = set('0123456789 +-.()')
    if not all(c in allowed_chars for c in stripped):
        raise ValidationError(
            'Use only digits, spaces, and these symbols: + - ( ) .',
        )

    digits = ''.join(c for c in stripped if c.isdigit())
    if len(digits) < 8:
        raise ValidationError('Enter at least 8 digits.')
    if len(digits) > 15:
        raise ValidationError('Phone number cannot have more than 15 digits.')
