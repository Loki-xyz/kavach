"""Database of Indian Laws and Legal Knowledge"""

INDIAN_ACTS = {
    "indian_contract_act": {
        "name": "Indian Contract Act, 1872",
        "key_sections": {
            "2": "Communication of proposals",
            "10": "What agreements are contracts",
            "23": "Lawful consideration and object",
            "73": "Compensation for breach",
            "108": "Rights of lessor and lessee",
        }
    },
    "consumer_protection_act": {
        "name": "Consumer Protection Act, 2019",
        "key_sections": {
            "2(7)": "Definition of consumer",
            "2(11)": "Deficiency in service",
            "2(47)": "Unfair trade practice",
            "35": "Filing of complaint",
            "38": "Mediation",
        }
    },
    "specific_reliefs_act": {
        "name": "Specific Relief Act, 1963",
        "key_sections": {
            "10": "Contracts not specifically enforceable",
            "14": "Specific performance of contract",
            "34": "Declaratory decrees",
        }
    },
    "transfer_of_property_act": {
        "name": "Transfer of Property Act, 1882",
        "key_sections": {
            "52": "Doctrine of Lis Pendens",
            "58": "Mortgage defined",
            "105": "Lease defined",
            "108": "Rights and liabilities of lessor and lessee",
        }
    },
    "consumer_protection_rules": {
        "name": "Consumer Protection Rules, 2020",
        "key_sections": {
            "3": "Jurisdiction of District Commission",
            "4": "Jurisdiction of State Commission",
            "5": "Jurisdiction of National Commission",
        }
    },
}

# Limitation periods in days
LIMITATION_PERIODS = {
    "simple_contract": 3 * 365,  # 3 years
    "written_instrument": 3 * 365,
    "negotiable_instrument": 3 * 365,
    "promissory_note": 3 * 365,
    "suit_for_accounts": 3 * 365,
    "suit_for_foreclosure": 12 * 365,  # 12 years
    "suit_for_redemption": 30,  # 30 days
    "consumer_complaint": 2 * 365,  # 2 years
    "rent_recovery": 3 * 365,
    "eviction_suit": 3 * 365,
    "specific_performance": 3 * 365,
    "declaration_suit": 3 * 365,
    "injunction_suit": 3 * 365,
    "tort_claim": 1 * 365,  # 1 year
    "motor_accident": 180,  # 6 months
    "workmen_compensation": 2 * 365,
}

# State-specific rent control acts
RENT_CONTROL_ACTS = {
    "Maharashtra": "Maharashtra Rent Control Act, 1999",
    "Delhi": "Delhi Rent Control Act, 1958",
    "Karnataka": "Karnataka Rent Control Act, 1999",
    "Tamil Nadu": "Tamil Nadu Buildings (Lease and Rent Control) Act, 1960",
    "West Bengal": "West Bengal Premises Tenancy Act, 1956",
    "Gujarat": "Gujarat Rent Control Act, 1999",
    "Uttar Pradesh": "Uttar Pradesh Urban Buildings (Regulation of Letting, Rent and Eviction) Act, 1972",
}

# Consumer Forum jurisdiction amounts
CONSUMER_JURISDICTION = {
    "district": {"upto": 1000000, "name": "District Consumer Disputes Redressal Commission"},
    "state": {"from": 1000001, "upto": 10000000, "name": "State Consumer Disputes Redressal Commission"},
    "national": {"above": 10000000, "name": "National Consumer Disputes Redressal Commission"},
}
