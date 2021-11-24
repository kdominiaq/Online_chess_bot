from chessboard import ChessBoard
from exceptions import IndexOutOfChessBoard
import logging
import numpy as np

class LogicGame(ChessBoard):
    def __init__(self, chessboard: ChessBoard) -> None:
        # assign chessboard to private varaible to get infomration about board
        self._cb = chessboard
        
        # white - 0, black - 1
        self._opponent_color = 0
        self._player_color = 0
        
        # Assign colors to variables (_opponent_color and _player_color).
        self._which_color_have_players()



    @property
    def get_player_color(self):
        """ Return color of the pieces (Player). """
        return self._player_color 

    @property
    def get_opponent_color(self):
        """ Return color of the pieces (Oponent). """
        return self._opponent_color

    def _which_color_have_players(self):
        """
        Working on the given chessboard image, check the color of the rocks on the left side of the board - compare to each other, 
        if the sum of RGB representation of color is smaller then second, it's black (because it is darker than it.)        
        If the color of the rock is black, it means the player has white color, and "we" start the game. Otherwise, the opponent starts 
        the game (has white in color).
        
        Assign colors to variables (_opponent_color and _player_color).
        """       
        # Looking fot the center of the field where towers are.
        # T - tower on  the top of board, B - on the bot.
        #   T . . . . . . .       
        #   . . . . . . . .       
        #   . . . . . . . .       
        #   . . . . . . . .       
        #   . . . . . . . .       
        #   . . . . . . . .        
        #   . . . . . . . .      
        #   B . . . . . . .       

        # counte center of the fileds
        tower_T_coordinates_y = int(self._cb.get_f_size[0] / 2)
        tower_T_coordinates_x = int(self._cb.get_f_size[1] / 2)

        tower_B_coordinates_y = self._cb.get_cb_size[0]  - int(self._cb.get_f_size[0] / 2)
        tower_B_coordinates_x = int(self._cb.get_f_size[1] / 2)

        # save color color of the fields
        tower_T_color = self._cb.get_cb_image[tower_T_coordinates_y,tower_T_coordinates_x]

        tower_B_color = self._cb.get_cb_image[tower_B_coordinates_y,tower_B_coordinates_x]
        
        # first three arguments of the list contains RGB, so nao assume the values
        tower_T_color = np.sum(tower_T_color[:-1])
        
        tower_B_color = np.sum(tower_B_color[:-1])
        
        # compare values, gretter value means in this field is brighter piece then second.
        # white pieces - 0
        # black pieces - 1
        if tower_T_color > tower_B_color:
            # assign colot to class values
            self._player_color = 1
            self._opponent_color = 0 

            # send log to file
            logging.info("Player color: Black, Opponent color: White.")
        else:
            self._player_color = 0
            self._opponent_color = 1
            
            logging.info("Player color: White, Opponent color: Black.")

    
    def is_chessboard_ready_to_start(self):
        """
        Method prevent the bot to start the game when the hame hsa benn already started. For each color of the pieces are two different methods:
        - Black (lowercase letters): if all pawns (p) and also knights (k) are in start position everything is fine. Chessboard must look like this:
        . k . . . . . k . 
        p p p p p p p p p
        
        - White (uppercase letters): One of the pawns (P) or knights (K) could be moved because the opppenet player has already start the game.
        Correct examples:
        . K . . . . . K .
        P P P P P P P P P

        . K . . . . . . .
        P P P P P P P P P
                    K

        . K . . . . . K .
        P P P P P P P P .
                        P

        :return is_ready_to_start: return True if all pieces are is started position, otherwise return False
        """

        is_ready_to_start = True
        # method depends on colors, so now code must check on which side are the white and black pieces. These infrmation are saved in classes vairables 
        # (_opponent_color and _player_color). If player color is 0 it means it has white color and pieces will be on the bottom  spaces of the chessboard

        
        # player has black pieces
        # . . . . . . . .
        # | | | | | | | |  <- skip rows
        # . . . . . . . .
        # p p p p p p p p
        # . k . . . . k .
        
        
        # all pieces must have same color so, the color form the first piece will be saved, and checked with others. If the color will be diffrent, return Fasle
        try:
            black_color_first = np.array([])
            black_color = np.array([])

                # check pawns
            center_of_field_y = int(self._cb.get_cb_size[0] - 9 / 8 *self._cb.get_f_size[0])
            for itr, center_of_field_x in enumerate(range(int(self._cb.get_f_size[1] / 2), # center of the first field
                                                        int(self._cb.get_cb_size[1] - self._cb.get_f_size[1] / 2 + self._cb.get_f_size[1]), # center of the last field
                                                        int(self._cb.get_f_size[1]))): # step by width of field
                    # colorof the first pawn
                if itr == 0:
                    black_color_first = self._cb.get_cb_image[center_of_field_y, center_of_field_x]
                else:
                    black_color = self._cb.get_cb_image[center_of_field_y, center_of_field_x]

                    # if the color is diffrent chessboard is not ready to play (game has already started) the np.array_equal(black_color_first, black_color)
                    # return True if arrays are the same
                    if not np.array_equal(black_color_first, black_color):
                        is_ready_to_start = False
                        return is_ready_to_start

            # check knights
            center_of_field_y = int(self._cb.get_cb_size[0] - (3 / 8 *self._cb.get_f_size[0])) # 7/8 ensure to find knight
            centers_of_knights_x = np.array([int(self._cb.get_f_size[1] / 2 + self._cb.get_f_size[1]), 
                                            int(self._cb.get_cb_size[1] - (self._cb.get_f_size[1] / 2 + self._cb.get_f_size[1]))])
            for center_of_field_x in centers_of_knights_x:
                black_color = self._cb.get_cb_image[center_of_field_y, center_of_field_x]

                # if the color is the same like colors of the fields, chessboard is not ready to play (game has already started) the np.array_equal(black_color_first, black_color)
                # return True if arrays are the same. This time code checks "is the color of found pixel is diffrent than fields color."
                bright, dark = self._cb.get_f_colors
                if np.array_equal(bright, black_color) and np.array_equal(dark, black_color):
                        is_ready_to_start = False
                        return is_ready_to_start
            
            logging.info("Chessbaord is ready to start the game - all piceses are in correct place.")
            return is_ready_to_start
        except IndexError:
            print("asd")
            logging.error("Something went wrong with scaling the chessboard. Resize the chessboard by shortcut: \"ctrl +\" or \"ctrl -\"")
            raise IndexOutOfChessBoard
    





    def find_opponent_move(self):
        """
        Return notation of the last move whish has been done by opppenet, for example: "a2a4"
        
        Most of the Online chess display last move by changing the color of the fields (e. g. Chesscom, Lichess.com). 
        Two fields have a different color than others:
        - First one has not got any pieces of chess on itself and the color is the same for whole the area. 
          (THIS IS THE PLACE FROM PIECE OF CHESS WAS TAKEN)
        - Second one has a piece of chess on itself. This means some piece is presented on-field and it is 
          possible to spot them by checking the color of the center
        
        Fields color:
        o - bright
        x - dark 

        o x o x o x o x
        x o x o x o x o
        o x o x o x o x
        x o x o x o x o
        o x o x o x o x
        x o x o x o x o
        o x o x o x o x
        x o x o x o x o        

        """
        bright_color, dark_color = self._cb.get_f_colors

        # field_color is grasped by [y,x] coordiantes:
        # different color also is grasped by [y + 6/8 * y, x - 3/8 * x] coordinates
        #             x
        # . . . . . . . .
        # . . . . . . f . y 
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . d . . . .
        # . . . . . . . .


        for y in range(int(self._cb.get_f_size[0] * 1 / 8), # rop right cornerof the first field
                            int(self._cb.get_cb_size[0] - self._cb.get_f_size[0] * 1 / 8), # top right corner of the last field
                            int(self._cb.get_f_size[0])): # step by width of field
            for x in range(int(self._cb.get_f_size[1] * 7 / 8), # rop right cornerof the first field
                            int(self._cb.get_cb_size[1] - self._cb.get_f_size[1] * 7 / 8 + self._cb.get_f_size[1]), # top right corner of the last field
                            int(self._cb.get_f_size[1])): # step by width of field
                
                field_color = self._cb.get_cb_image[y,x]
                field_color = field_color[:-1] #cut last layer from the image

                # bright field color
                if np.array_equal(field_color, bright_color):
                    continue
                # dark field color
                elif np.array_equal(field_color, dark_color):
                    continue
                # otherwise
                else:
                    # TODO
                    d_y = int(y + (6/8) * y)
                    d_x = int(x - (3/8) * x)
                    different_color = self._cb.get_cb_image[d_y,d_x]
                    different_color = different_color[:-1]
                    print(different_color, field_color)

                    if np.array_equal(different_color, field_color):
                        pass

        