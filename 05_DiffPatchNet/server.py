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

    # Разбираем команду
    command, *args = message.split(None, 1)
    args = args[0] if args else ""

    # --- Команда LOGIN ---
    if command == "login":
        cow_name = args.strip()
        if cow_name in available_cows:
            clients[writer] = cow_name
            available_cows.remove(cow_name)
            writer.write(f"Logged in as {cow_name}\n".encode())
            await writer.drain()
        else:
            writer.write(f"Cow name '{cow_name}' is not available or does not exist.\n".encode())
            await writer.drain()

    # --- Команда WHO ---
    elif command == "who":
        logged_in_users = [name for name in clients.values() if name]
        writer.write("Logged in users:\n".encode())
        writer.write("\n".join(logged_in_users).encode() + b'\n')
        await writer.drain()

    # --- Команда COWS ---
    elif command == "cows":
        writer.write("Available cows:\n".encode())
        writer.write("\n".join(sorted(list(available_cows))).encode() + b'\n')
        await writer.drain()

        # Проверка, что пользователь залогинен для других команд
    elif not clients.get(writer):
        writer.write("Please login first using 'login <cow_name>'.\n".encode())
        await writer.drain()

    # --- Команда SAY (личное сообщение) ---
    elif command == "say":
        try:
            recipient_name, text = args.split(None, 1)
        except ValueError:
            writer.write("Usage: say <recipient_cow> <message>\n".encode())
            await writer.drain()
            continue

        sender_name = clients[writer]
        message_to_send = cowsay.cowsay(text, cow=sender_name)

        recipient_writer = None
        for w, name in clients.items():
            if name == recipient_name:
                recipient_writer = w
                break

        if recipient_writer:
            recipient_writer.write(f"\nMessage from {sender_name}:\n".encode())
            recipient_writer.write(message_to_send.encode() + b'\n')
            await recipient_writer.drain()
        else:
            writer.write(f"User '{recipient_name}' not found.\n".encode())
            await writer.drain()

    # --- Команда YIELD (сообщение всем) ---
    elif command == "yield":
        sender_name = clients[writer]
        text = args
        message_to_send = cowsay.cowsay(text, cow=sender_name)

        # Рассылаем всем залогиненным клиентам, кроме себя
        for w, name in clients.items():
            if name and w != writer:
                w.write(f"\nBroadcast from {sender_name}:\n".encode())
                w.write(message_to_send.encode() + b'\n')
                await w.drain()


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