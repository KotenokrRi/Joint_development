# server.py
import asyncio
import cowsay

# Здесь будут храниться данные о клиентах и их именах
clients = {}  # {username}
available_cows = set(cowsay.list_cows())


async def chat(reader, writer):
    # Эта функция будет запускаться для каждого нового клиента
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    # Регистрируем writer клиента, но пока без имени
    clients[writer] = ""

    # Основной цикл обработки сообщений от клиента
    while True:
        data = await reader.read(1024)
        if not data:
            break  #отключился

        message = data.decode().strip()
        print(f"Received from {addr}: {message}")


    # Клиент отключился, убираем его из списка
    print(f"Connection from {addr} closed")
    username = clients.pop(writer, "")
    if username:
        available_cows.add(username)  # Возвращаем имя коровы в список свободных
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        chat, '0.0.0.0', 1337)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())