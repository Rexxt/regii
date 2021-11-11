from interpreter import RegII
from sys import argv

if len(argv) > 1 and argv[1] == '-h':
    print("Usage: ./main.py <file>")
    exit()
elif len(argv) > 1:
    file = open(argv[1], 'r')
    interpreter = RegII(argv[1])
    result = interpreter.interpret(file.read())
    if not result[0]:
        print(result[4])
    file.close()
else:
    print("RegII Shell")
    interpreter = RegII("RegII Shell")
    print(f"Running RegII v{interpreter.__version__}")
    while True:
        try:
            result = interpreter.interpret(input("> "))
            if not result[0]:
                print(result[4])
        except KeyboardInterrupt:
            print("\n")
            exit()
            continue
        except EOFError:
            print("\n")
            break
        except Exception as e:
            print(e)
            continue
        except:
            print("Unknown error")
            continue