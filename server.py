
import socket
import sys
import random

SHIPS = [(4, 'A'), (3, 'B'), (2, 'C')] #SLen and SLabel
SHIPS = [(4, 'A'), (3, 'B'), (2, 'C')] 
#SLen, SLabel

def generate_board():
    board = [['.' for _ in range(6)] for _ in range(6)]

    #place ships
    for SLen, SLabel in SHIPS:
        placed = False
        while not placed:
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                row = random.randint(0, 6 - 1)
                col = random.randint(0, 6 - SLen)
                if all(board[row][col + i] == '.' for i in range(SLen)):
                    for i in range(SLen):
                        board[row][col + i] = SLabel
                    placed = True
            else:  # Vertical
            else:  
                row = random.randint(0, 6 - SLen)
                col = random.randint(0, 6 - 1)
                if all(board[row + i][col] == '.' for i in range(SLen)):
                    for i in range(SLen):
                        board[row + i][col] = SLabel
                    placed = True
    return board

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py [PORT_NUMBER]")
        return

    #vars
    port = int(sys.argv[1])
    board = generate_board()
    hits_remaining = sum(length for length, _ in SHIPS)

    #connect server to client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        try:
            row, col = map(int, data.strip().split())
            if not (0 <= row < 6 and 0 <= col < 6):
                conn.send("Invalid".encode())
                continue

            #check guess status
            cell = board[row][col]
            if cell in ('X', 'O'):
                result = "PrevGuess"
            elif cell == '.':
                board[row][col] = 'O'
                result = "Miss"
            else:
                board[row][col] = 'X'
                hits_remaining -= 1
                result = "Hit"

            if hits_remaining == 0:
                result = "Win"

            #send result
            conn.send(result.encode())
        except Exception as e:
            conn.send("Error".encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
