from aqt import mw
from aqt.qt import QShortcut, QKeySequence
from aqt.gui_hooks import browser_menus_did_init
from aqt.utils import tooltip

# =================================================
# SHARED HELPER FUNCTIONS
# =================================================

def apply_actions_to_cids(cids):
    """
    Takes a list of Card IDs, Flags them Green (3), and Suspends them.
    """
    if not cids:
        return

    mw.progress.start()
    try:
        # 1. Suspend all provided cards
        mw.col.sched.suspend_cards(cids)
        
        # 2. Flag all provided cards Green (3)
        # UPDATED FOR ANKI 24/25+: Use set_user_flag_for_cards(flag_index, list_of_ids)
        mw.col.set_user_flag_for_cards(3, cids)
        
    finally:
        mw.progress.finish()

def get_note_sibling_cids(card):
    """
    Given a card, returns a list of IDs for ALL cards belonging to that note.
    """
    note = card.note()
    # Return all card IDs linked to this note ID
    return mw.col.find_cards(f"nid:{note.id}")

# =================================================
# 1. REVIEWER LOGIC
# =================================================

def reviewer_suspend_card():
    # Shift+C: Acts on the current CARD only
    if mw.state != "review": return
    card = mw.reviewer.card
    if not card: return

    # Checkpoint for Undo
    mw.checkpoint("Flag/Suspend Card")
    
    # Apply actions just to this one card
    apply_actions_to_cids([card.id])
    
    # Refresh/Move to next card
    mw.reviewer.nextCard()
    tooltip("Card Suspended & Green")

def reviewer_suspend_note():
    # Shift+N: Acts on the NOTE (all sibling cards)
    if mw.state != "review": return
    card = mw.reviewer.card
    if not card: return

    mw.checkpoint("Flag/Suspend Note")

    # Get all sibling cards (including the current one)
    target_cids = get_note_sibling_cids(card)
    
    # Apply actions to all of them
    apply_actions_to_cids(target_cids)
    
    # Move to next card
    mw.reviewer.nextCard()
    tooltip(f"Note Suspended ({len(target_cids)} cards)")

# =================================================
# 2. BROWSER LOGIC
# =================================================

def browser_suspend_card(browser):
    # Shift+C: Acts on selected cards only
    cids = browser.selected_cards()
    if not cids: return

    mw.checkpoint("Flag/Suspend Selected Cards")
    apply_actions_to_cids(cids)
    
    browser.model.reset()
    tooltip(f"Updated {len(cids)} Cards")

def browser_suspend_note(browser):
    # Shift+N: Acts on Notes of selected cards
    selected_cids = browser.selected_cards()
    if not selected_cids: return

    mw.checkpoint("Flag/Suspend Selected Notes")
    
    # Find all unique Notes from the selected cards
    target_cids = set()
    for cid in selected_cids:
        # We need to be careful fetching cards in a loop, but IDs are safe
        try:
            card = mw.col.get_card(cid)
            siblings = get_note_sibling_cids(card)
            target_cids.update(siblings) # Add siblings to the set
        except:
            continue
    
    apply_actions_to_cids(list(target_cids))
    
    browser.model.reset()
    tooltip(f"Updated Notes ({len(target_cids)} related cards)")

# =================================================
# 3. REGISTER SHORTCUTS
# =================================================

# Reviewer Shortcuts
# We create these without a parent initially, then attach to Main Window
shortcut_rev_c = QShortcut(QKeySequence("Shift+C"), mw)
shortcut_rev_c.activated.connect(reviewer_suspend_card)

shortcut_rev_n = QShortcut(QKeySequence("Shift+N"), mw)
shortcut_rev_n.activated.connect(reviewer_suspend_note)

# Browser Shortcuts
def setup_browser_shortcuts(browser):
    s_c = QShortcut(QKeySequence("Shift+C"), browser)
    s_c.activated.connect(lambda: browser_suspend_card(browser))
    
    s_n = QShortcut(QKeySequence("Shift+N"), browser)
    s_n.activated.connect(lambda: browser_suspend_note(browser))

browser_menus_did_init.append(setup_browser_shortcuts)
