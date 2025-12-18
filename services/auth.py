"""
Authentication Service for Kerala Smart Farmer
Mobile number-based signup and login with OTP verification.
"""

import random
import time
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# ============================================================================
# IN-MEMORY DATABASE (In production, use a real database like SQLite/PostgreSQL)
# ============================================================================

# Registered users database: {mobile_number: user_data}
REGISTERED_USERS: Dict[str, dict] = {}

# Pending OTP verifications: {mobile_number: {"otp": str, "expires": float, "attempts": int}}
PENDING_OTPS: Dict[str, dict] = {}

# OTP Configuration
OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 300  # 5 minutes
MAX_OTP_ATTEMPTS = 3
OTP_RESEND_COOLDOWN = 60  # 1 minute before resend


@dataclass
class AuthResult:
    success: bool
    message: str
    otp_sent: bool = False
    is_registered: bool = False
    requires_otp: bool = False
    user_data: Optional[dict] = None


def validate_mobile_number(mobile: str) -> Tuple[bool, str]:
    """
    Validate Indian mobile number format.
    Rules:
    - Must be exactly 10 digits
    - Must start with 6, 7, 8, or 9
    - Must contain only digits
    """
    if not mobile:
        return False, "Mobile number is required."
    
    # Remove any spaces or dashes
    mobile = mobile.replace(" ", "").replace("-", "")
    
    if not mobile.isdigit():
        return False, "Mobile number must contain only digits."
    
    if len(mobile) != 10:
        return False, "Mobile number must be exactly 10 digits."
    
    if mobile[0] not in ['6', '7', '8', '9']:
        return False, "Mobile number must start with 6, 7, 8, or 9."
    
    return True, "Valid mobile number."


def generate_otp() -> str:
    """Generate a random 6-digit OTP."""
    return ''.join([str(random.randint(0, 9)) for _ in range(OTP_LENGTH)])


def is_user_registered(mobile: str) -> bool:
    """Check if a mobile number is already registered."""
    return mobile in REGISTERED_USERS


def get_user_data(mobile: str) -> Optional[dict]:
    """Get user data for a registered mobile number."""
    return REGISTERED_USERS.get(mobile)


def send_otp(mobile: str) -> Tuple[bool, str, str]:
    """
    Generate and send OTP to the mobile number.
    In production, integrate with SMS gateway (MSG91, Twilio, etc.)
    
    Returns: (success, message, otp_for_demo)
    """
    # Check cooldown
    if mobile in PENDING_OTPS:
        pending = PENDING_OTPS[mobile]
        time_since_sent = time.time() - (pending.get("sent_at", 0))
        if time_since_sent < OTP_RESEND_COOLDOWN:
            remaining = int(OTP_RESEND_COOLDOWN - time_since_sent)
            return False, f"Please wait {remaining} seconds before requesting a new OTP.", ""
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP with expiry
    PENDING_OTPS[mobile] = {
        "otp": otp,
        "expires": time.time() + OTP_EXPIRY_SECONDS,
        "attempts": 0,
        "sent_at": time.time()
    }
    
    # In production, send SMS here using API
    # Example: send_sms_via_gateway(mobile, f"Your AgriVision OTP is: {otp}")
    
    # For demo purposes, we return the OTP to display on screen
    return True, f"OTP sent successfully to ******{mobile[-4:]}.", otp


def verify_otp(mobile: str, entered_otp: str) -> Tuple[bool, str]:
    """
    Verify the OTP entered by user.
    
    Returns: (success, message)
    """
    if mobile not in PENDING_OTPS:
        return False, "No OTP was sent to this number. Please request a new OTP."
    
    pending = PENDING_OTPS[mobile]
    
    # Check expiry
    if time.time() > pending["expires"]:
        del PENDING_OTPS[mobile]
        return False, "OTP has expired. Please request a new OTP."
    
    # Check attempts
    if pending["attempts"] >= MAX_OTP_ATTEMPTS:
        del PENDING_OTPS[mobile]
        return False, "Too many failed attempts. Please request a new OTP."
    
    # Verify OTP
    if entered_otp != pending["otp"]:
        pending["attempts"] += 1
        remaining = MAX_OTP_ATTEMPTS - pending["attempts"]
        if remaining > 0:
            return False, f"Invalid OTP. {remaining} attempts remaining."
        else:
            del PENDING_OTPS[mobile]
            return False, "Invalid OTP. Maximum attempts exceeded. Please request a new OTP."
    
    # OTP verified successfully
    del PENDING_OTPS[mobile]
    return True, "OTP verified successfully."


def register_user(mobile: str, name: str = "") -> Tuple[bool, str]:
    """
    Register a new user after OTP verification.
    
    Returns: (success, message)
    """
    if is_user_registered(mobile):
        return False, "This mobile number is already registered."
    
    # Create user record
    REGISTERED_USERS[mobile] = {
        "mobile": mobile,
        "name": name if name else f"Farmer_{mobile[-4:]}",
        "registered_at": datetime.now().isoformat(),
        "verified": True,
        "last_login": datetime.now().isoformat()
    }
    
    return True, "Registration successful! Welcome to AgriVision."


def login_user(mobile: str) -> Tuple[bool, str]:
    """
    Login an existing user (after OTP verification).
    
    Returns: (success, message)
    """
    if not is_user_registered(mobile):
        return False, "This mobile number is not registered. Please sign up first."
    
    # Update last login
    REGISTERED_USERS[mobile]["last_login"] = datetime.now().isoformat()
    
    return True, "Login successful! Welcome back."


def initiate_auth(mobile: str) -> AuthResult:
    """
    Main authentication flow entry point.
    Determines if user needs to signup or login, and sends OTP.
    
    Returns: AuthResult with appropriate flags and messages
    """
    # Validate mobile number
    is_valid, validation_msg = validate_mobile_number(mobile)
    if not is_valid:
        return AuthResult(
            success=False,
            message=validation_msg,
            otp_sent=False,
            is_registered=False,
            requires_otp=False
        )
    
    # Check if user is registered
    is_registered = is_user_registered(mobile)
    
    # Send OTP
    otp_success, otp_msg, otp_value = send_otp(mobile)
    
    if not otp_success:
        return AuthResult(
            success=False,
            message=otp_msg,
            otp_sent=False,
            is_registered=is_registered,
            requires_otp=False
        )
    
    action = "login" if is_registered else "signup"
    message = f"OTP sent to ******{mobile[-4:]}. {'Welcome back!' if is_registered else 'Complete registration by verifying OTP.'}"
    
    return AuthResult(
        success=True,
        message=message,
        otp_sent=True,
        is_registered=is_registered,
        requires_otp=True,
        user_data={"otp_for_demo": otp_value, "action": action}  # For demo only
    )


def complete_auth(mobile: str, otp: str, name: str = "") -> AuthResult:
    """
    Complete authentication after OTP verification.
    Handles both signup and login flows.
    
    Returns: AuthResult with final status
    """
    # Verify OTP
    otp_valid, otp_msg = verify_otp(mobile, otp)
    
    if not otp_valid:
        return AuthResult(
            success=False,
            message=otp_msg,
            otp_sent=False,
            is_registered=is_user_registered(mobile),
            requires_otp=True
        )
    
    # OTP verified - now register or login
    if is_user_registered(mobile):
        # Login existing user
        login_success, login_msg = login_user(mobile)
        user_data = get_user_data(mobile) if login_success else None
        return AuthResult(
            success=login_success,
            message=login_msg,
            otp_sent=False,
            is_registered=True,
            requires_otp=False,
            user_data=user_data
        )
    else:
        # Register new user
        reg_success, reg_msg = register_user(mobile, name)
        user_data = get_user_data(mobile) if reg_success else None
        return AuthResult(
            success=reg_success,
            message=reg_msg,
            otp_sent=False,
            is_registered=reg_success,
            requires_otp=False,
            user_data=user_data
        )


def get_all_users() -> Dict[str, dict]:
    """Get all registered users (for admin purposes)."""
    return REGISTERED_USERS.copy()


def delete_user(mobile: str) -> Tuple[bool, str]:
    """Delete a user account."""
    if mobile in REGISTERED_USERS:
        del REGISTERED_USERS[mobile]
        return True, "User account deleted successfully."
    return False, "User not found."
