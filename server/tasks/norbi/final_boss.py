from fastapi import APIRouter, Body
from fastapi.responses import Response
import chess  # pip install python-chess

router = APIRouter(prefix="/final-boss")

@router.post("")
def solve_mate_in_one(body: str = Body(..., media_type="text/plain")):
    # 1. Bemenet feldolgozása sorokra
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    
    # Az utolsó sor a soron következő játékos színe
    turn_color_str = lines[-1].lower()
    board_rows = lines[:-1]

    # 2. Üres tábla létrehozása
    board = chess.Board(None)

    # Unicode karakterek megfeleltetése a chess könyvtár típusainak
    # White: ♔♕♖♗♘♙, Black: ♚♛♜♝♞♟
    piece_map = {
        '♖': chess.ROOK, '♘': chess.KNIGHT, '♗': chess.BISHOP, 
        '♕': chess.QUEEN, '♔': chess.KING, '♙': chess.PAWN,
        '♜': chess.ROOK, '♞': chess.KNIGHT, '♝': chess.BISHOP, 
        '♛': chess.QUEEN, '♚': chess.KING, '♟': chess.PAWN
    }
    
    white_pieces = {'♖', '♘', '♗', '♕', '♔', '♙'}

    # 3. Tábla feltöltése (A bemenet a 8. sortól indul lefelé az 1. sorig)
    for r, line in enumerate(board_rows):
        rank = 7 - r  # A chess libben a 0. index az 1-es sor, a 7. a 8-as
        for f, char in enumerate(line):
            file = f  # 0 = 'a', 7 = 'h'
            
            if char in piece_map:
                piece_type = piece_map[char]
                color = chess.WHITE if char in white_pieces else chess.BLACK
                piece = chess.Piece(piece_type, color)
                
                # Helyezzük el a bábut a megfelelő négyzeten
                square = chess.square(file, rank)
                board.set_piece_at(square, piece)

    # 4. Következő játékos beállítása
    board.turn = chess.WHITE if turn_color_str == "white" else chess.BLACK

    # 5. Matt lépés keresése
    # Végigmegyünk az összes szabályos lépésen
    for move in board.legal_moves:
        board.push(move)  # Lépés megtekintése
        if board.is_checkmate():
            # Megvan a matt!
            uci_move = move.uci() # pl. "a7a8q" (kisbetűs promóció)
            
            # Formázás: Ha promóció van (5 karakter), a feladat nagybetűt vár (pl. e7e8Q)
            if len(uci_move) == 5:
                uci_move = uci_move[:4] + uci_move[4].upper()
            
            return Response(content=uci_move, media_type="text/plain")
        
        board.pop()  # Lépés visszavonása, próbáljuk a következőt

    return Response(content="error", media_type="text/plain")