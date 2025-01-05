import asyncio
import ssl
import json

# Серверная часть
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected to {addr}")
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = json.loads(data.decode())
            print(f"Received: {message}")

            response = {"echo": message}
            writer.write(json.dumps(response).encode())
            await writer.drain()
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def start_server():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('server_cert.pem', 'server_key.pem')
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888, ssl=ssl_context)
    async with server:
        await server.serve_forever()

# Клиентская часть
async def start_client():
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.load_verify_locations('server_cert.pem')
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, ssl=ssl_context)
    try:
        while True:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                break
            writer.write(json.dumps(message).encode())
            await writer.drain()

            data = await reader.read(1024)
            response = json.loads(data.decode())
            print(f"Server response: {response}")
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    choice = input("Run server or client? (s/c): ")
    if choice == 's':
        await start_server()
    elif choice == 'c':
        await start_client()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    asyncio.run(main())