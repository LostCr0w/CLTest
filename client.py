import socket
import sys

#set up board
def print_board(board):
    print("\nThe Game Board:")
    print("   " + " ".join(str(i) for i in range(6)))
    for i in range(6):
        print(f"{i}  " + " ".join(board[i]))
    print()

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py [PORT_NUMBER]")
        return

    #set up vars
    port = int(sys.argv[1])
    host = 'localhost'
    guess_board = [['.' for _ in range(6)] for _ in range(6)]
    total_hits_needed = 9
    hits = 0
    guesses = 0

    #serverconnect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to server. Enter a guess (row [space] column)!\n")

    #guess request
    while hits < total_hits_needed:
        print_board(guess_board)
        try:
            guess = input("Enter a guess (row [space] col): ").strip()
            row, col = map(int, guess.split())
        except:
            print("Unable to use that input, please enter two integers separated by space.")
            continue

        #send to server
        client_socket.send(guess.encode())
        response = client_socket.recv(1024).decode()

        #guess options
        if response == "Hit":
            guess_board[row][col] = 'X'
            hits += 1
            print(">> Hit!\n")
        elif response == "Miss":
            guess_board[row][col] = 'O'
            print(">> Miss!\n")
        elif response == "PrevGuess":
            print(">> You already tried that spot.\n")
        elif response == "Invalid":
            print(">> Invalid guess. Try again.\n")
        elif response == "Win":
            guess_board[row][col] = 'X'
            guesses += 1
            print_board(guess_board)
            print(f">> Nice Shot! You sank all ships in {guesses} guesses!")
            break
        elif response == "Error":
            print(">> There was an error processing your guess. Please try again.\n")
        else:
            print(">> Unknown response from server.\n")

        guesses += 1

    #end
    client_socket.close()

if __name__ == "__main__":
    main()
