class Terminal:
    def __init__(self, screen):
        self.screen = screen
        self.top_line = 0
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_line = self.max_y - 1
        self.centre_x = int(self.max_x / 2)

    def update(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.bottom_line = self.max_y - 1
        self.centre_x = int(self.max_x / 2)

