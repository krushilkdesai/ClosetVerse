from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def indian_price(value):
    """Format price in Indian Rupee format with commas"""
    try:
        # Convert to integer to remove decimals
        price = int(float(value))
        # Format with Indian number system (lakhs, crores)
        if price >= 10000000:  # 1 crore
            crores = price // 10000000
            remainder = price % 10000000
            if remainder >= 100000:
                lakhs = remainder // 100000
                return f"₹{crores},{lakhs:02d},000"
            else:
                return f"₹{crores} crore"
        elif price >= 100000:  # 1 lakh
            lakhs = price // 100000
            remainder = price % 100000
            if remainder >= 1000:
                thousands = remainder // 1000
                return f"₹{lakhs},{thousands:02d},000"
            else:
                return f"₹{lakhs} lakh"
        elif price >= 1000:
            # Format with comma for thousands
            return f"₹{price:,}"
        else:
            return f"₹{price}"
    except (ValueError, TypeError):
        return f"₹{value}"

@register.filter
def rupee_symbol(value):
    """Add rupee symbol to price"""
    try:
        price = int(float(value))
        return f"₹{price:,}"
    except (ValueError, TypeError):
        return f"₹{value}"
