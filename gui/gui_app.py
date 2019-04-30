from gui.gui_board import *


class Gui(GuiBoard):
    def __init__(self):
        super(Gui, self).__init__()
        self.board = UltimateBoard()
        self.on_cell_clicked = self.subcell_clicked

    def subcell_clicked(self, x, y, w, h, board, move):
        # todo check if the cell that is clicked is also allowed to be clicked else display warning!!!!
        # do not provide player just yet, only do so when we are sure we can click the cell
        cell = Cell(x, y, w, h, None, board_idx=board, cell_idx=move)  # todo fix this *-1

        if cell in self.clicked_cells:  # if cell already clicked -> do nothing
            return

        cell.player = self.board.playerJustMoved * -1
        self.clicked_cells.add(cell)
        self.board.make_move(move, board)
        print(board, move)
        print(self.board)

    def draw_allowed_moves(self, color):
        moves = self.board.get_moves()
        for board, move in moves:
            for cell in self.all_cells:
                if cell.board_idx == board and cell.cell_idx == move:
                    pygame.draw.rect(self.gameDisplay, color,
                                     (cell.pos_x, cell.pos_y, cell.width, cell.height))

    def game_loop(self):
        highlight = AVAILABLE_MOVE_1
        frames = 0

        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.quit_game()

            if frames == 30:
                highlight = AVAILABLE_MOVE_1 if highlight == AVAILABLE_MOVE_2 else AVAILABLE_MOVE_2
                frames = 0

            self.gameDisplay.fill(WHITE)
            self.draw_main_grid()
            self.draw_clicked_cells()
            self.draw_allowed_moves(highlight)
            pygame.display.update()
            self.clock.tick(60)
            frames += 1


if __name__ == '__main__':
    g = Gui()
    g.game_loop()
