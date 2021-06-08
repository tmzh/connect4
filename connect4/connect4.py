import bisect
import pygame

from board import Board

pygame.init()
YELLOW = pygame.color.THECOLORS['yellow']
WHITE = pygame.color.THECOLORS['white']
BLUE = pygame.color.THECOLORS['blue']
BLACK = pygame.color.THECOLORS['black']
RED = pygame.color.THECOLORS['red']
COLOR_MAP = {
    0: WHITE,
    1: RED,
    2: YELLOW
}
clock = pygame.time.Clock()


class Space:
    def __init__(self, x, y, coin_size):
        self.color = WHITE
        self._rect = [x, y, coin_size, coin_size]

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self._rect)


class VisualBoard:
    COIN_SIZE = 100
    GAP = 10

    def __init__(self, b: Board):
        self.board = b
        self.n_rows = b.n_rows
        self.n_cols = b.n_cols
        self.mouse_x = None

    def __call__(self):
        while not self.board.game_over:
            for event in pygame.event.get():
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    board.game_over = True
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_x = pos_x
                if event.type == pygame.MOUSEBUTTONUP:
                    column_num = bisect.bisect(self.x_list, pos_x) - 1
                    board.make_move(column_num)
            self.draw_board()
        if self.board.game_over:
            pygame.time.wait(3000)

    @property
    def x_list(self):
        return [x * (self.COIN_SIZE + self.GAP) + self.GAP for x in range(self.n_cols)]

    @property
    def y_list(self):
        return [x * (self.COIN_SIZE + self.GAP) + self.GAP for x in range(self.n_rows)]

    @property
    def space_size(self):
        return self.COIN_SIZE + self.GAP

    @property
    def screen_size(self):
        label_row_height = self.GAP + self.space_size
        drop_row_height = self.GAP + self.space_size
        return self.GAP + self.space_size * self.n_cols, \
               self.GAP + self.space_size * self.n_rows + label_row_height + drop_row_height

    def draw_board(self):
        screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Connect 4")
        screen.fill(BLUE)
        pygame.draw.rect(screen, BLACK, (0, 0, self.screen_size[0], 2*self.COIN_SIZE))
        if self.mouse_x:
            self.draw_space(self.board.current_player, self.mouse_x - self.COIN_SIZE // 2,
                            self.COIN_SIZE - self.GAP, screen)
        if self.board.game_over:
            self.display_text(screen, f"Player {self.board.current_player} won the game")
        else:
            self.display_text(screen, f"{self.board.current_player}'s turn")
        for i, r in enumerate(self.board.state[::-1]):
            for j, c in enumerate(r):
                self.draw_space(c, self.x_list[j], self.space_size * 2 + self.y_list[i], screen)
        pygame.display.flip()

    def display_text(self, screen, text):
        my_font = pygame.font.SysFont("Arial", 48)
        label = my_font.render(text, 1, (255, 255, 0))
        screen.blit(label, (self.GAP, self.GAP))

    def draw_space(self, c, i, j, screen):
        space = Space(i, j, self.COIN_SIZE)
        space.color = COLOR_MAP[c]
        space.draw(screen)


board = Board()
connect4board = VisualBoard(board)
connect4board()

pygame.quit()
