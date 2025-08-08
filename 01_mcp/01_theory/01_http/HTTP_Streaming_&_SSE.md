# HTTP Streaming & Server-Sent Events (SSE)

This README provides a complete overview of HTTP Streaming and Server-Sent Events (SSE). You'll learn how each works, see real request/response examples, and understand when to use one over the other.

---

## Table of Contents

1. [Introduction](#introduction)
2. [HTTP Streaming](#http-streaming)

   * [What Is HTTP Streaming?](#what-is-http-streaming)
   * [Chunked Transfer Encoding (HTTP/1.1)](#chunked-transfer-encoding-http11)
   * [HTTP/2 Streaming](#http2-streaming)
   * [Use Cases](#use-cases)
   * [Example: Raw HTTP Chunked Response](#example-raw-http-chunked-response)
3. [Server-Sent Events (SSE)](#server-sent-events-sse)

   * [What Is SSE?](#what-is-sse)
   * [Event Stream Format](#event-stream-format)
   * [Client Request & Server Response](#client-request--server-response)
   * [Event Framing Fields](#event-framing-fields)
   * [Reconnection & Last-Event-ID](#reconnection--last-event-id)
   * [Example: SSE Exchange](#example-sse-exchange)
4. [Key Differences](#key-differences)
5. [Choosing Between HTTP Streaming and SSE](#choosing-between-http-streaming-and-sse)
6. [Appendix: Example Client Code](#appendix-example-client-code)

---

## Introduction

Web applications often need to deliver data incrementally or in real time. Two common approaches:

* **HTTP Streaming**: Send arbitrary data chunks over one HTTP response.
* **Server-Sent Events (SSE)**: A text-based protocol on top of HTTP Streaming for server→client event delivery.

This document explains both, compares them, and provides concrete examples.

---

## HTTP Streaming

### What Is HTTP Streaming?

The server sends parts of the response body as they become available, without closing the connection until all data is sent.

### Chunked Transfer Encoding (HTTP/1.1)

* **Header:** `Transfer-Encoding: chunked`
* **Format:**

  ```http
  <chunk-size in hex>\r\n
  <chunk-data>\r\n
  ```

  A zero-length chunk (`0`) signals the end of the stream.

### HTTP/2 Streaming

HTTP/2 uses DATA frames within a stream. The server sends DATA frames when ready; the end is marked by the `END_STREAM` flag.

### Use Cases

* Live video or audio streaming
* Large file downloads in parts
* Custom real-time protocols (e.g., newline-delimited JSON)

### Example: Raw HTTP Chunked Response

```http
-- TCP connection opens to example.com:80 --

▶ CLIENT → SERVER
GET /stream HTTP/1.1
Host: example.com
Connection: keep-alive

◀ SERVER → CLIENT
HTTP/1.1 200 OK
Content-Type: text/plain
Transfer-Encoding: chunked
Connection: keep-alive

4\r\n
ping\r\n

7\r\n
:pong!\r\n

0\r\n
\r\n
# End of stream
```

* The client reads a 4-byte chunk `ping`, then a 7-byte chunk `:pong!`, then the end.

---

## Server-Sent Events (SSE)

### What Is SSE?

SSE is a unidirectional event-streaming protocol standardized by HTML5. It runs over HTTP/1.1 or HTTP/2 and delivers text-based events to the client. Browsers support it via the `EventSource` API.

### Event Stream Format

* **Content-Type:** `text/event-stream`
* **Framing:** Each event is a block of lines ending with a blank line.
* **Syntax example:**

  ```text
  data: First line of message
  data: Second line of message

  ```

### Client Request & Server Response

**Client → Server**

```http
GET /events HTTP/1.1
Host: example.com
Accept: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

```

**Server → Client**

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

# Stream opens immediately
```

The connection stays open until closed by either side or a network error.

### Event Framing Fields

* `data:` (required) — the event payload (can span multiple lines)
* `event:` (optional) — client-visible event type
* `id:` (optional) — unique identifier for reconnection
* `retry:` (optional) — reconnection delay in milliseconds

### Reconnection & Last-Event-ID

* **Auto-reconnect:** Browsers retry on network failure.
* **`Last-Event-ID` header:** Client sends it on reconnect to resume from a specific event ID.

### Example: SSE Exchange

```http
# Client opens the stream
GET /events HTTP/1.1
Host: example.com
Accept: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

# Server begins response
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

# Event 1
data: Hello, client! Welcome.

# Event 2 (with id & event name)
id: 2
event: update
data: {"status":"ok"}

# More events can follow indefinitely
```

---

## Key Differences

| Feature           | HTTP Streaming                        | Server-Sent Events (SSE)             |
| ----------------- | ------------------------------------- | ------------------------------------ |
| Direction         | server → client                       | server → client                      |
| Framing           | no built-in framing                   | `data:`, `id:`, `event:` framing     |
| Content Type      | any (text, JSON, binary)              | `text/event-stream` (text only)      |
| Client Support    | manual parsing (e.g., fetch + reader) | native `EventSource` in browsers     |
| Reconnection      | manual                                | automatic with `Last-Event-ID`       |
| Typical Use Cases | video, file download, custom streams  | live notifications, logs, UI updates |

---

## Choosing Between HTTP Streaming and SSE

* **HTTP Streaming**: Best for flexible, custom data or binary streams.
* **SSE**: Ideal for simple, text-based event feeds with minimal client code and auto-reconnect.

---

## Appendix: Example Client Code

**JavaScript SSE Client**

```javascript
const source = new EventSource('/events');
source.onmessage = e => console.log('Message:', e.data);
source.addEventListener('update', e => {
  const obj = JSON.parse(e.data);
  console.log('Update event:', obj);
});
```

**Python HTTP Streaming Client**

```python
import requests

with requests.get('http://example.com/stream', stream=True) as response:
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            print('Received chunk:', chunk)
```

---
