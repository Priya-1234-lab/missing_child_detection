# backend/notifications/utils.py
import os
import logging
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Parent
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # load TWILIO credentials

logger = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Example: +1415xxxxxxx


def normalize_phone(phone):
    """Normalize phone number to +91XXXXXXXXXX if Indian format."""
    if not phone:
        return None
    p = str(phone).strip().replace(" ", "").replace("-", "")
    if p.startswith("+"):
        return p
    if len(p) == 10 and p.isdigit():
        return "+91" + p
    return p


def send_alert(parent_id, location="Unknown Location", lat=None, lon=None, uploader_ip=None):
    """
    Send both Email and SMS alerts with optional map link.
    """
    try:
        parent = Parent.objects.get(id=parent_id)
    except Parent.DoesNotExist:
        logger.error("Parent id %s not found", parent_id)
        return False

    ok = False
    maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else None

    # ---------- EMAIL ----------
    email_msg = f"Dear {parent.username},\n\nYour child may have been found at: {location}.\n"
    if maps_link:
        email_msg += f"Google Maps link: {maps_link}\n"
    if uploader_ip:
        email_msg += f"Uploader IP: {uploader_ip}\n"
    email_msg += "\nPlease check immediately.\n\n— Missing Child Detection System"

    try:
        send_mail(
            subject="🚨 Missing Child Alert",
            message=email_msg,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[parent.email],
            fail_silently=False,
        )
        ok = True
        logger.info("✅ Email sent to %s", parent.email)
    except Exception as e:
        logger.exception("❌ Failed to send email: %s", e)

    # ---------- SMS ----------
        # ---------- SMS ----------
    try:
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            to_phone = normalize_phone(parent.phone)
            if not to_phone:
                logger.warning("⚠️ No valid phone number for parent %s", parent.id)
                return ok

            sms_msg = f"🚨 Your child may have been found at {location}."
            if maps_link:
                sms_msg += f" Map: {maps_link}"
            if uploader_ip:
                sms_msg += f" (Uploaded from IP: {uploader_ip})"

            # 🔍 Debug print — this helps us see what's happening
            print("📤 Sending SMS via Twilio...")
            print(f"TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID}")
            print(f"From: {TWILIO_PHONE_NUMBER}")
            print(f"To: {to_phone}")
            print(f"Message: {sms_msg}")

            msg = client.messages.create(
                body=sms_msg,
                from_=TWILIO_PHONE_NUMBER,
                to=to_phone,
            )

            print(f"✅ SMS sent successfully. Message SID: {msg.sid}")
            ok = True
            logger.info("✅ SMS sent to %s", to_phone)

        else:
            logger.warning("⚠️ Twilio credentials missing — SMS skipped.")
            print("⚠️ Twilio credentials missing — SMS skipped.")

    except Exception as e:
        print("❌ SMS sending failed:", e)
        logger.exception("❌ Failed to send SMS: %s", e)

    return ok
