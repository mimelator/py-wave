class ColorPalettes:
    @staticmethod
    def get_palette(name):
        palettes = {
            "default": [
                (255, 0, 0),    # Red
                (0, 255, 0),    # Green
                (0, 0, 255),    # Blue
                (255, 255, 0),  # Yellow
                (255, 0, 255)   # Magenta
            ],
            "pastel": [
                (255, 182, 193),  # Light Pink
                (135, 206, 250),  # Light Sky Blue
                (240, 230, 140),  # Khaki
                (144, 238, 144),  # Light Green
                (221, 160, 221)   # Plum
            ],
            "neon": [
                (57, 255, 20),    # Neon Green
                (255, 20, 147),   # Deep Pink
                (0, 255, 255),    # Cyan
                (255, 255, 0),    # Yellow
                (255, 0, 255)     # Magenta
            ]
        }
        return palettes.get(name, palettes["default"])