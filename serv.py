import asyncio #Асинхронный сервер

writers = []

def forward(writer, addr, message):
    for w in writers:
        if w != writer:
            w.write(f"{addr!r}: {message!r}\n".encode())

async def handle(reader, writer): #функция обработки подключения
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    message = f"{addr!r} - connect"
    print(message)
    forward(writer, addr, message)
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        forward(writer, addr, message)
        await writer.drain()
        if message == "exit":
            message = f"{addr!r} - close"
            print(message)
            forward(writer, "Server", message) #фидбек от сервера
            break
    writers.remove(writer)
    writer.close()

async def main():
    server = await asyncio.start_server(handle, '127.0.0.1', 9100) #асинхронный запуск, обращение к функции обработки подключения
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()
asyncio.run(main())
