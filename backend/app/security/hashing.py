"""
Password Hashing Utilities.

This module provides password hashing functions.
Note: The main hashing logic is in user_service.py.
This file exists for backwards compatibility.
"""

from backend.app.services.user_service import hash_password, verify_password

# Re-export for backwards compatibility
__all__ = ["hash_password", "verify_password"]

