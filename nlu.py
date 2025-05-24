import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Supported sites and actions for demo
SITES = ["amazon", "netflix", "youtube"]
ACTIONS = ["search", "add to cart", "play"]


def parse_command(command: str) -> dict:
    """
    Parse the user's natural language command into a structured plan using spaCy and rules.
    Enhanced to extract item, price, rating, and handle more phrasings.
    """
    doc = nlp(command.lower())
    site = None
    action = None
    item = None
    filters = {}

    # Find site
    for s in SITES:
        if s in command.lower():
            site = s.capitalize()
            break

    # Find action
    for a in ACTIONS:
        if a in command.lower():
            action = a
            break
    if not action:
        if site == "Amazon":
            if "add" in command and "cart" in command:
                action = "add to cart"
            elif "search" in command:
                action = "search"
        elif site in ["Netflix", "YouTube"]:
            if "play" in command:
                action = "play"

    # Extract item (object of search or play)
    # Try to extract quoted text, after 'search for', 'play', 'titled', etc.
    m = re.search(r'search for ([\w\s\-]+)', command.lower())
    if m:
        item = m.group(1).strip()
    else:
        m = re.search(r'play (movie|video)? ?([\w\s\-]+)', command.lower())
        if m:
            item = m.group(2).strip()
        else:
            m = re.search(r'titled ([\w\s\-]+)', command.lower())
            if m:
                item = m.group(1).strip()
            else:
                m = re.search(r'"([^"]+)"', command)
                if m:
                    item = m.group(1).strip()
                else:
                    # fallback: use noun chunks after action
                    for token in doc:
                        if token.lemma_ in ["search", "play"]:
                            np = next(doc.noun_chunks, None)
                            if np:
                                item = np.text.strip()
                                break
    # Price filter (e.g., under $80, below $50, max $100)
    m = re.search(r'(under|below|max) \$?(\d+)', command.lower())
    if m:
        filters["price_max"] = int(m.group(2))
    # Rating filter (e.g., at least 4 stars, 4+ stars)
    m = re.search(r'(at least|minimum|over|above|more than)? ?(\d(\.\d)?) ?\+? ?stars?', command.lower())
    if m:
        try:
            filters["rating_min"] = float(m.group(2))
        except Exception:
            pass
    plan = {
        "site": site or "Unknown",
        "action": action or "Unknown",
        "item": item or "Unknown",
        "filters": filters
    }
    print(f"[NLU] Parsed plan: {plan}")
    return plan 