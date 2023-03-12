if __name__ == "__main__":
    import sys

    sys.path.append('../')

    import socket
    from UMDDecoder import TSLEvent

    dst_ip = "192.168.0.112"
    dst_port = 1337
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    requests = []
    while True:
        print("--- MENU ---")
        print("1.\tДобавить новый пакет")
        print("2.\tДобавить сообщение к существующему пакету")
        print("3.\tОтправить все пакеты")
        print("9.\tОчистить пакеты")
        print("0.\tВыход")
        inp = int(input(">>> "))
        if inp == 1:
            requests.append(b"")
        if inp == 1 or inp == 2:
            camera_num = int(input("Введите номер камеры: "))
            print("Выберите состояние:")
            print("0.\tВне эфира")
            print("1.\tPreview")
            print("2.\tProgram")
            print("3.\tBoth")
            choice = int(input(">>> "))
            tallies = [False] * 4
            if choice == 1 or choice == 3:
                tallies[0] = True
            if choice == 2 or choice == 3:
                tallies[1] = True

            requests[-1] += TSLEvent(camera_num, tallies, 1, " " * 16).to_bytes()
        elif inp == 3:
            for request in requests:
                sock.sendto(request, (dst_ip, dst_port))
        elif inp == 9:
            requests.clear()
        elif inp == 0:
            break
