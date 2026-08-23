import urllib.parse
import webbrowser


def bhejo(phone: str, message: str) -> None:
    """
    Opens WhatsApp Web and pre-fills the message to the specified number.
    Usage: whatsapp.bhejo("+919876543210", "Namaste Duniya!")
    """
    print(f"📱 Opening WhatsApp to send message to {phone}...")
    encoded_message = urllib.parse.quote(message)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
    webbrowser.open(url)
    print("✅ WhatsApp Web opened. Please press 'Send' manually when it loads.")


def spam(phone: str, message: str, count: int) -> None:
    """
    Spam function simulated for JugaadLang.
    """
    print(f"⚠️ SPAM WARNING: Preparing to send {count} messages to {phone}.")
    print(
        "In true Jugaad style, this will just open one pre-filled tab, you'll have to spam it manually to avoid getting banned!"
    )
    bhejo(phone, message)
