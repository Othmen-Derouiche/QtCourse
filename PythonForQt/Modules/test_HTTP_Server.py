from __future__ import annotations
import sys
import json

from PySide6.QtCore import QCoreApplication, QByteArray
from PySide6.QtNetwork import QHttpHeaders, QTcpServer
from PySide6.QtHttpServer import QHttpServer, QHttpServerResponse

def route(request):
    payload = {
        "name": "Test Sample",
        "PredictionId": "pred1",
        "Image": {
            "type": "V4.1",
            "Nature": "MP",
            "Lot": "run18"
        }
    }

    # Return a QHttpServerResponse with JSON
    return QHttpServerResponse(
        QHttpServerResponse.StatusCode.Ok,
        QByteArray(json.dumps(payload).encode("utf-8")),
        b"application/json"
    )

def after_request(request, response):
    headers = response.headers()
    headers.append(QHttpHeaders.WellKnownHeader.WWWAuthenticate,
                   'Basic realm="Simple example", charset="UTF-8"')
    response.setHeaders(headers)

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)

    httpServer = QHttpServer()
    httpServer.route("/", route)
    httpServer.addAfterRequestHandler(httpServer, after_request)

    tcpServer = QTcpServer()
    if not tcpServer.listen() or not httpServer.bind(tcpServer):
        print("Server failed to listen on a port.", file=sys.stderr)
        sys.exit(-1)

    port = tcpServer.serverPort()
    print(f"Running on http://127.0.0.1:{port}/ (Press CTRL+C to quit)")

    sys.exit(app.exec())