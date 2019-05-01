from itertools import cycle, chain

from gui.gui_board import *


class Gui(GuiBoard):
    def __init__(self):
        super(Gui, self).__init__()
        self.board = UltimateBoard()
        self.on_cell_clicked = self.subcell_clicked
        self.allowed_cells = set()

    def subcell_clicked(self, x, y, w, h, board, move):
        # do not provide player just yet, only do so when we are sure we can click the cell
        cell = Cell(x, y, w, h, player=None, board_idx=board, cell_idx=move)

        if cell in self.clicked_cells:  # if cell already clicked -> do nothing
            return

        if cell not in self.allowed_cells:
            return  # todo raise warning or display text

        cell.player = self.board.playerJustMoved * -1
        self.clicked_cells.add(cell)
        self.board.make_move(move, board)
        print(board, move)
        print(self.board)
        self.allowed_cells = self.find_allowed_cells()

    def find_allowed_cells(self):
        allowed_cells = set()  # clear currently allowed moves

        moves = self.board.get_moves()
        for board, move in moves:
            for cell in self.all_cells:
                if cell.board_idx == board and cell.cell_idx == move:
                    allowed_cells.add(cell)

        return allowed_cells

    def draw_allowed_moves(self, color):
        for cell in self.allowed_cells:
            pygame.draw.rect(self.gameDisplay, color,
                             (cell.pos_x, cell.pos_y, cell.width, cell.height))

    def game_loop(self):
        # set up an endless cycle of B values (rgB) for highlighting moves
        highlight_range = [i for i in range(140, 201, 2)]
        brightness_iter = cycle(chain(highlight_range, reversed(highlight_range)))

        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.quit_game()

            brightness = next(brightness_iter)
            highlight = (255, 255, brightness)  # yellow highlight used to accent available moves

            self.gameDisplay.fill(WHITE)
            self.draw_main_grid()

            # todo check for game end here as well. Mind not have allowed cells because game is over
            if not self.allowed_cells:
                self.allowed_cells = self.find_allowed_cells()

            self.draw_clicked_cells()
            self.draw_allowed_moves(highlight)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    g = Gui()
    g.game_loop()
