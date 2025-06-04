const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, 'public')));

io.on('connection', (socket) => {
  socket.on('join', (room) => {
    socket.join(room);
    socket.to(room).emit('message', 'Opponent joined');
  });

  socket.on('move', ({ room, move }) => {
    socket.to(room).emit('move', move);
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
