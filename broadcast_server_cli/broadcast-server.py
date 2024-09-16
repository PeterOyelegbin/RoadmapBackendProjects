#!/usr/bin/env python3

import asyncio
import argparse
import websockets

# Shared data for handling connected clients
connected_clients = set()


# Handler for WebSocket connections in server mode.
async def handler(websocket, path):
    # Register the new client
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            # Broadcast the received message to all connected clients except the sender
            await asyncio.gather(*(client.send(message) for client in connected_clients if client != websocket))
    except websockets.ConnectionClosed:
        print("Connection closed")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")


# Start the WebSocket server.
async def start_server(port):
    server = await websockets.serve(handler, 'localhost', port)
    print(f"Server started on ws://localhost:{port}")
    try:
        await server.wait_closed()
    except asyncio.CancelledError:
        print("Server is shutting down...")


def run_server(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = loop.create_task(start_server(port))
    try:
        loop.run_until_complete(server)
    except KeyboardInterrupt:
        server.cancel()
        loop.run_until_complete(asyncio.shield(server))
    finally:
        loop.close()
        print("Server has been shut down.")


# Client-side logic for connecting and sending messages.
async def connect_client(uri):
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to server: {uri}")
            while True:
                message = input("Enter a message to send: ")
                await websocket.send(message)
                # Optionally, receive and print the response
                try:
                    response = await websocket.recv()
                    print(f"Received: {response}")
                except websockets.ConnectionClosed:
                    print("Connection closed by server")
                    break
    except websockets.ConnectionClosed:
        print("Connection closed by server")
    except asyncio.CancelledError:
        print("Connection was cancelled")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description='WebSocket broadcast server/client.')
    subparsers = parser.add_subparsers(dest='mode', required=True)

    # Subparser for server mode
    server_parser = subparsers.add_parser('start', help='Start the WebSocket server.')
    server_parser.add_argument('--port', type=int, default=8080, help='Port for the server to listen on.')
    
    # Subparser for client mode
    client_parser = subparsers.add_parser('connect', help='Connect to the WebSocket server as a client.')
    client_parser.add_argument('--uri', type=str, default='ws://localhost:8080', help='URI of the WebSocket server to connect to.')
    
    args = parser.parse_args()

    if args.mode == 'start':
        # Run the server
        run_server(args.port)
    elif args.mode == 'connect':
        # Run the client
        asyncio.run(connect_client(args.uri))


if __name__ == "__main__":
    main()
