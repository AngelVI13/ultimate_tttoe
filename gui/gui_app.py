import time
from functools import partial
from itertools import cycle, chain

from engine.uct import uct_multi
from gui.gui_board import *


class Gui(GuiBoard):
    def __init__(self):
        super(Gui, self).__init__()
        self.board = UltimateBoard()
        self.allowed_cells = set()
        self.grids_with_result = set()  # all grids that have a result on them

    def reset_game(self):
        self.board = UltimateBoard()
        self.allowed_cells = set()
        self.grids_with_result = set()
        self.clicked_cells = set()

    def subcell_clicked(self, cell):
        # do not provide player just yet, only do so when we are sure we can click the cell
        if cell in self.clicked_cells:  # if cell already clicked -> do nothing
            return

        if cell not in self.allowed_cells:
            return

        cell.player = self.board.playerJustMoved * -1
        self.clicked_cells.add(cell)

        move, board = cell.cell_idx, cell.board_idx
        self.board.make_move(move, board)
        self.allowed_cells = self.find_allowed_cells()

        result = self.board.pos[board].get_result()
        if result is not None:
            for grid in self.all_grids:
                if grid.board_idx == board:
                    grid.player = result  # add the player who won to the grid that he won
                    self.grids_with_result.add(grid)

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
            pygame.draw.rect(self.gameDisplay, color, (cell.pos_x, cell.pos_y, cell.width, cell.height))

    def click_cell_under_mouse(self, pos):
        mouse_x, mouse_y = pos
        for cell in self.all_cells:
            if cell.pos_x < mouse_x < cell.pos_x + cell.width and cell.pos_y < mouse_y < cell.pos_y + cell.height:
                self.subcell_clicked(cell)
                break  # don't bother finishing up the loop -> break on match

    def draw_results(self):  # todo this is the same as draw_all moves? parameterize
        for grid in self.grids_with_result:
            pygame.draw.rect(self.gameDisplay, GRID_RESULT_COLORS[grid.player],
                             (grid.pos_x, grid.pos_y, grid.width, grid.height))

    def check_for_game_over(self):
        result = self.board.get_result(player_jm=PLAYER_X)
        if result is not None:
            self.message_display(text=RESULT_TEXT[result])
            self.message_display(text='Click anywhere to continue...',
                                 pos=(DISPLAY_WIDTH / 2, (BOARD_HEIGHT + OFFSET_Y + 30)), font='comicsansms', size=20)

            # Wait until a mouse click before going back to main menu
            clicked = False
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        clicked = True
            return True  # game is over
        return False  # game not over

    def click_random_cell(self):
        random_cell = random.choice(list(self.allowed_cells))
        self.subcell_clicked(random_cell)
        time.sleep(0.2)  # sleep 1s so output can be checked

    def get_best_engine_move(self):
        print(uct_multi(self.board, itermax=10000, verbose=False))

    def do_nothing(self):
        pass  # todo remove this later

    def get_game_input(self, game_type, mouse_pos):
        if game_type == GameType.SINGLE_PLAYER:
            if self.board.playerJustMoved == PLAYER_O:  # X's turn  todo allow user to select side to play
                if mouse_pos is not None:
                    self.click_cell_under_mouse(mouse_pos)
            else:
                self.click_random_cell()  # todo replace with AI

        elif game_type == GameType.MULTI_PLAYER:
            if mouse_pos is not None:
                self.click_cell_under_mouse(mouse_pos)

    def game_loop(self, game_type):
        pygame.event.clear(pygame.MOUSEBUTTONUP)  # clear all mouse clicks
        self.reset_game()

        # set up an endless cycle of B values (rgB) for highlighting moves
        highlight_range = [i for i in range(HIGHLIGHT_LOW, HIGHLIGHT_HIGH+1, HIGHLIGHT_STEP)]
        brightness_iter = cycle(chain(highlight_range, reversed(highlight_range)))

        start = time.time()
        while not self.check_for_game_over():
            pos = None  # default mouse pos is None -> update on MOUSE_UP

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

            brightness = next(brightness_iter)
            highlight = (255, 255, brightness)  # yellow highlight used to accent available moves

            self.gameDisplay.fill(WHITE)
            self.draw_main_grid()

            if not self.allowed_cells:
                self.allowed_cells = self.find_allowed_cells()

            # Need to wait a bit before allowing user input otherwise the menu click gets detected
            # as game click
            if time.time() - start > PAUSE_BEFORE_USER_INPUT:
                self.get_game_input(game_type, pos)

            self.draw_clicked_cells()
            self.draw_results()
            self.draw_allowed_moves(highlight)
            self.draw_side_to_move(-self.board.playerJustMoved)

            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)

    def menu_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

            self.gameDisplay.fill(WHITE)
            self.message_display("Ultimate Tic Tac Toe", pos=(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 3),
                                 font='comicsansms', size=40, update=False)

            self.button("Single Player", **MENU_BUTTON_POSITIONS[0],
                        action=partial(self.game_loop, GameType.SINGLE_PLAYER))
            self.button("Two Player",    **MENU_BUTTON_POSITIONS[1],
                        action=partial(self.game_loop, GameType.MULTI_PLAYER))
            self.button("Settings",      **MENU_BUTTON_POSITIONS[2], action=self.do_nothing)
            self.button("Quit",          **MENU_BUTTON_POSITIONS[3], action=self.quit_game)

            pygame.display.update()
            self.clock.tick(15)


if __name__ == '__main__':
    g = Gui()
    g.menu_loop()
