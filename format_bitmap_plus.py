#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function
import chess
import chess.pgn
import numpy as np


# In[2]:


def splitter(inputStr, black):

    inputStr = format(inputStr, "064b")
    tmp = [inputStr[i:i+8] for i in range(0, len(inputStr), 8)]
    
    for i in range(len(tmp)):
        tmp2 = list(tmp[i])
        tmp2 = [int(x) * black for x in tmp2]
        tmp[i] = tmp2

    return tmp


# In[3]:


def get_bitmap_plus(board):
    """
    Generates a bitmap representation of the chess.Board argument plus castling rights and turn
        given as input.
    :param board: board to convert
    :return: 773-size vector representing the board in bitmap plus
    """
    
    # we don't need the baseBoard since board object has the function pieces() and it behaves the same 
    # as in Sabatelli's version of python-chess (check that we re using board.pieces() below)
    
    
    P_input = splitter(int(board.pieces(chess.PAWN, chess.WHITE)), 1)
    R_input = splitter(int(board.pieces(chess.ROOK, chess.WHITE)), 1)
    N_input = splitter(int(board.pieces(chess.KNIGHT, chess.WHITE)), 1)
    B_input = splitter(int(board.pieces(chess.BISHOP, chess.WHITE)), 1)
    Q_input = splitter(int(board.pieces(chess.QUEEN, chess.WHITE)), 1)
    K_input = splitter(int(board.pieces(chess.KING, chess.WHITE)), 1)

    p_input = splitter(int(board.pieces(chess.PAWN, chess.BLACK)), -1)
    r_input = splitter(int(board.pieces(chess.ROOK, chess.BLACK)), -1)
    n_input = splitter(int(board.pieces(chess.KNIGHT, chess.BLACK)), -1)
    b_input = splitter(int(board.pieces(chess.BISHOP, chess.BLACK)), -1)
    q_input = splitter(int(board.pieces(chess.QUEEN, chess.BLACK)), -1)
    k_input = splitter(int(board.pieces(chess.KING, chess.BLACK)), -1)
    

    bitmap = [P_input, R_input, N_input, B_input, Q_input, K_input, 
             p_input, r_input, n_input, b_input, q_input, k_input]
    
    
    # convert to np.ndarray to be flatten
    bitmap_plus = np.zeros(773, dtype = np.int8)
    
    bitmap = np.array(bitmap, dtype = np.int8)
    bitmap = bitmap.flatten()
    
    bitmap_plus[: 768] = bitmap
    
    # encoding castling rights
    bitmap_plus[768] = int(board.has_kingside_castling_rights(True)) # True means White
    bitmap_plus[769] = int(board.has_queenside_castling_rights(True))
    bitmap_plus[770] = int(board.has_kingside_castling_rights(False)) # False means Black
    bitmap_plus[771] = int(board.has_queenside_castling_rights(False))
    
    # turn
    bitmap_plus[772] = int(board.turn)
    
    return bitmap_plus


# In[4]:


