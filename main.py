from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


app = FastAPI()

html = """
    <!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var msg = JSON.parse(event.data)
                var messages = document.getElementById('messages')
                var message = document.createElement('p')
                var content = document.createTextNode(msg.i + ': ' + msg.msg)
                
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify({msg: input.value}))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def web_socket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        i += 1
        data = await websocket.receive_json()

        await websocket.send_json({'i': i,
                                   'msg': data['msg']})
