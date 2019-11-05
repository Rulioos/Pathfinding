class Color:
    """
    Object that defines a color by RGB and alpha layer.
    Method get_color returns the tuple RGB.
    Method get_alpha returns alpha value of the color.
    """

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        self.r, self.g, self.b, self.a = r, g, b, a

    def get_color(self):
        return int(self.r), int(self.g), int(self.b)

    def set_color(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def get_alpha(self):
        return self.a

    def __copy__(self, other):
        other.r, other.g, other.b, other.a = self.r, self.g, self.b, self.a
