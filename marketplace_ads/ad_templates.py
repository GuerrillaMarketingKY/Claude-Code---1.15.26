"""
Facebook Marketplace ad templates for portable storage units.
Multiple title and description variations to avoid repetitive listings.
"""

import random

# --- Ad Titles (with {city} and {state} placeholders) ---

TITLES = [
    "Portable Storage Units in {city} - Code Inspected & Ready",
    "Rent or Buy Portable Storage in {city}, {state}",
    "{city} Portable Storage Containers - Inspected & Delivered",
    "Code Inspected Storage Units - {city}, {state}",
    "Portable Storage for {city} - Up to Code, Delivered to You",
    "Storage Containers Available in {city} - Fully Inspected",
    "{city} Storage Units - Portable, Inspected, Affordable",
    "Need Storage in {city}? Portable Units Available Now",
    "Inspected Portable Storage - Serving {city}, {state}",
    "Portable Storage Delivered to {city} - Code Compliant",
    "{city} Portable Storage - Buy or Rent, Inspected Units",
    "Up-to-Code Storage Containers in {city}, {state}",
    "Secure Portable Storage for {city} Residents",
    "On-Site Storage Units in {city} - Inspected & Delivered",
    "Portable Storage Solutions in {city} - Fully Inspected",
    "{city}, {state} - Portable Storage Units Available Now",
    "Code Inspected Portable Storage Near {city}",
    "Quality Storage Units Delivered to {city}, {state}",
    "Affordable Portable Storage in {city} - Inspected & Ready",
    "Storage Made Simple in {city} - Portable & Inspected",
]

# --- Description Templates ---

DESCRIPTIONS = [
    """Looking for reliable portable storage in {city}, {state}? We've got you covered!

Our storage units are fully up-to-code inspected and ready for delivery straight to your location in the {city} area.

What we offer:
- Fully inspected, code-compliant portable storage units
- Multiple sizes available to fit your needs
- Delivery and pickup in {city} and surrounding areas
- Ideal for home renovation, moving, job sites, or extra space
- Weather-resistant and secure

Whether you're a homeowner, contractor, or business in {city} - we have the right storage solution for you.

Contact us today for pricing and availability in {city}, {state}!""",

    """Portable storage units now available in {city}, {state}!

Every single one of our units has been professionally inspected and is up to code. No surprises, no hassles - just clean, secure storage delivered right to your door in {city}.

Why choose us?
- Up-to-code inspected units you can trust
- Convenient delivery anywhere in {city}
- Flexible rental and purchase options
- Perfect for moving, remodeling, business storage, or seasonal needs
- Durable construction built to handle {state} weather

Serving {city} and all surrounding communities. Reach out today to reserve your unit!""",

    """Are you in {city} and need extra storage space? Our portable storage units are the answer.

All units are fully inspected and meet code requirements - guaranteed. We deliver directly to your property in {city}, {state}, so you can start storing right away.

Great for:
- Home renovations and remodeling projects
- Moving and staging
- Construction and job sites in the {city} area
- Business inventory and equipment
- Seasonal storage

Sizes available to match any project. We proudly serve {city} and the greater {state} area.

Message us for a free quote!""",

    """Portable storage units for {city}, {state} - inspected, delivered, and ready to use.

Stop paying for off-site storage across town. We bring the storage TO YOU in {city}. All of our units have passed code inspection, so you get peace of mind with every rental or purchase.

Our storage units are:
- Code inspected and certified
- Available for rent or purchase
- Delivered and picked up on your schedule
- Built tough for any {state} weather conditions
- Secure with heavy-duty locking systems

Homes, businesses, and contractors in {city} trust us for their portable storage needs. You should too.

Get in touch for availability!""",

    """Need storage in {city}? We deliver up-to-code inspected portable storage units directly to your location in {city}, {state}.

No storage facility runs. No monthly locker fees. Just convenient, on-site storage that comes to you.

Perfect for {city} residents who need:
- Extra space during a move
- Secure job site storage
- Room during a home renovation
- Business or inventory overflow
- Seasonal and long-term storage

Every unit is professionally inspected and code compliant. Multiple sizes available.

{city}, {state} and surrounding areas - contact us today!""",

    """Attention {city} homeowners, contractors, and businesses: portable storage is here.

We supply up-to-code inspected portable storage units with delivery throughout {city}, {state} and surrounding communities.

Here's what sets us apart:
- Every unit is inspected and meets local code standards
- Fast delivery to any address in {city}
- Flexible terms - rent weekly, monthly, or buy outright
- Range of sizes from compact to extra-large
- Weatherproof and secure construction

Whether you need short-term storage for a project or a long-term solution in {city}, we have you covered.

Message us now for pricing!""",

    """Portable storage containers available NOW in {city}, {state}.

Our units aren't just convenient - they're inspected and up to code. That means you're getting safe, compliant storage delivered right to your {city} property.

Use cases:
- Decluttering your home in {city}
- Storing equipment and materials on a job site
- Holding inventory for your {city}-area business
- Keeping things safe during renovations
- Temporary or permanent storage solutions

We make storage easy for everyone in {city}. No hidden fees, no fine print.

Call or message for your free estimate!""",

    """Storage doesn't have to be complicated. In {city}, {state}, we deliver portable storage units straight to your door.

Every unit has been professionally inspected and certified up to code. You get secure, reliable storage without ever leaving {city}.

Available for:
- Residential storage in {city} neighborhoods
- Commercial and business use
- Construction and contractor projects
- Event and seasonal storage
- Long-term and short-term rentals

Multiple unit sizes to choose from. Fast delivery across the {city} metro area.

Reach out today - we're ready to serve {city}!""",
]

# --- Category and Tags ---

CATEGORY = "Storage & Organization"

TAGS = [
    "portable storage",
    "storage unit",
    "storage container",
    "code inspected",
    "delivered storage",
    "moving storage",
    "job site storage",
    "storage rental",
    "storage for sale",
    "on-site storage",
]

# --- Condition and Availability ---

CONDITIONS = ["New", "Like New", "Good"]

# --- Helper Functions ---


def generate_ad(city, state, seed=None):
    """Generate a single ad for a given city/state combo."""
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random(f"{city}-{state}")

    title = rng.choice(TITLES).format(city=city, state=state)
    description = rng.choice(DESCRIPTIONS).format(city=city, state=state)
    condition = rng.choice(CONDITIONS)
    tags = rng.sample(TAGS, min(5, len(TAGS)))

    return {
        "title": title,
        "description": description,
        "city": city,
        "state": state,
        "category": CATEGORY,
        "condition": condition,
        "tags": tags,
        "location": f"{city}, {state}",
    }


def generate_multiple_ads(city, state, count=1):
    """Generate multiple unique ad variations for a single city."""
    ads = []
    for i in range(count):
        seed = f"{city}-{state}-{i}"
        ads.append(generate_ad(city, state, seed=seed))
    return ads
