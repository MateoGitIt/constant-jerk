from rungekutta import main

X, Y, U = main()

def test(X, Y, frame_num):
    X_origins = X[::round(len(X) / frame_num)]
    Y_origins = Y[::round(len(Y) / frame_num)]

    print(len(X_origins))
    print(len(Y_origins))
    print()
    for i in range(100):
        print(f"X origin: {X_origins[i]}, X real: {X[i]}")
    
    for i in range(100):
        print(f"Y origin: {Y_origins[i]}, Y real: {Y[i]}")

test(X, Y, 100)

