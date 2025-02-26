# Window Dimensions
# Provides a flexible, scalable screen layout that can adapt
# to different display sizes while maintaining proportional design

# Main view takes up 70% of the screen width
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Calculate component widths proportionally
MAIN_VIEW_WIDTH = int(WINDOW_WIDTH * 0.7)
SIDE_PANEL_WIDTH = int(WINDOW_WIDTH * 0.3)

# UI Component Sizing
# Carefully sized to provide balanced information display
LOG_HEIGHT = 300
MINIMAP_SIZE = 250
STATS_HEIGHT = 150

# Color Palette
# A carefully curated set of colors that provide:
# - Readability
# - Visual hierarchy
# - Consistent aesthetic

BLACK = (0, 0, 0)        # Primary background color
WHITE = (255, 255, 255)  # Primary text and highlight color
GRAY = (128, 128, 128)   # Neutral UI elements
RED = (255, 0, 0)        # Danger or critical state indicator
DARK_GRAY = (32, 32, 32) # Secondary background, subtle elements