from datetime import datetime
import pandas as pd

def format_date(date_str):
    """Convert date string to consistent format"""
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

def get_condition_options():
    """Return list of common dermatologic conditions"""
    return [
        "Eczema", "Psoriasis", "Acne", "Rosacea",
        "Contact Dermatitis", "Seborrheic Dermatitis",
        "Hives", "Other"
    ]

def get_symptom_options():
    """Return list of common dermatologic symptoms"""
    return [
        "Itching", "Redness", "Swelling", "Burning",
        "Dryness", "Scaling", "Blisters", "Pain",
        "Discoloration", "Warmth", "Rash"
    ]

def get_trigger_options():
    """Return list of common triggers"""
    return [
        "Stress", "Weather", "Food", "Medication",
        "Exercise", "Allergens", "Skincare Products",
        "Clothing", "Heat", "Cold", "Unknown"
    ]

def get_treatment_options():
    """Return list of common treatments"""
    return [
        "Topical Steroids", "Moisturizer", "Antihistamines",
        "Oral Medication", "Phototherapy", "Cold Compress",
        "Prescription Cream", "Other"
    ]