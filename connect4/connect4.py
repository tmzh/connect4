import bisect
import pygame

from board import Board


pygame.init()
YELLOW = pygame.color.THECOLORS['yellow']
WHITE = pygame.color.THECOLORS['white']
BLUE = pygame.color.THECOLORS['blue']
RED = pygame.color.THECOLORS['red']
COLOR_MAP = {
    0: WHITE,
    1: RED,
    2: YELLOW
}
clock = pygame.time.Clock()


class Space:
    def __init__(self, x, y):
        self.color = WHITE
        self._rect = [x, y, 40, 40]

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self._rect)


class VisualBoard:
    DISC_SIZE = 40
    GAP = 5

    def __init__(self, b: Board):
        self.board = b
        self.n_rows = b.n_rows
        self.n_cols = b.n_cols

    def __call__(self):
        while not self.board.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    board.game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (pos_x, pos_y) = pygame.mouse.get_pos()
                    column_num = bisect.bisect(self.x_list, pos_x) - 1
                    board.make_move(column_num)
            self.draw_board()
            clock.tick(60)

    @property
    def x_list(self):
        return [x * (self.DISC_SIZE + self.GAP) + self.GAP for x in range(self.n_cols)]

    @property
    def y_list(self):
        return [x * (self.DISC_SIZE + self.GAP) + self.GAP for x in range(self.n_rows)]

    @property
    def size(self):
        return self.GAP + (self.DISC_SIZE + self.GAP) * self.n_cols, \
               self.GAP + (self.DISC_SIZE + self.GAP) * self.n_rows

    def draw_board(self):
        screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Connect 4 but Worse")
        screen.fill(BLUE)
        for i, r in enumerate(self.board.state[::-1]):
            for j, c in enumerate(r):
                space = Space(self.x_list[j], self.y_list[i])
                space.color = COLOR_MAP[c]
                space.draw(screen)
        pygame.display.flip()


board = Board()
connect4board = VisualBoard(board)
connect4board()

pygame.quit()
