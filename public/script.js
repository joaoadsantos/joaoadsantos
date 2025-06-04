const boardElement = document.getElementById('board');
const statusEl = document.getElementById('status');
const vsAiBtn = document.getElementById('vs-ai');
const vsOnlineBtn = document.getElementById('vs-online');

let board = null;
let game = new Chess();
let socket = null;
let room = null;
let vsAI = false;

function updateStatus() {
  let status = '';
  let moveColor = game.turn() === 'b' ? 'Pretas' : 'Brancas';
  if (game.in_checkmate()) {
    status = 'Fim de jogo, ' + moveColor + ' estão em cheque-mate.';
  } else if (game.in_draw()) {
    status = 'Empate!';
  } else {
    status = 'Vez das ' + moveColor + (game.in_check() ? ' (em cheque)' : '');
  }
  statusEl.innerHTML = status;
}

function onDragStart(source, piece) {
  if (game.game_over()) return false;
  if (!vsAI && socket && game.turn() === 'w' && piece.search(/^b/) !== -1) return false;
  if (!vsAI && socket && game.turn() === 'b' && piece.search(/^w/) !== -1) return false;
}

function makeRandomMove() {
  const possibleMoves = game.moves();
  if (possibleMoves.length === 0) return;
  const move = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
  game.move(move);
  board.position(game.fen());
  updateStatus();
}

function onDrop(source, target) {
  let move = game.move({ from: source, to: target, promotion: 'q' });
  if (move === null) return 'snapback';
  if (socket) {
    socket.emit('move', { room, move });
  }
  updateStatus();
  if (vsAI && !game.game_over()) {
    window.setTimeout(makeRandomMove, 250);
  }
}

function startGameAI() {
  game.reset();
  vsAI = true;
  if (socket) {
    socket.disconnect();
    socket = null;
  }
  board = Chessboard('board', {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: () => board.position(game.fen()),
  });
  updateStatus();
}

function startGameOnline() {
  vsAI = false;
  socket = io();
  room = prompt('Digite o nome da sala:');
  if (!room) return;
  socket.emit('join', room);
  game.reset();
  board = Chessboard('board', {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: () => board.position(game.fen()),
  });
  socket.on('move', (move) => {
    game.move(move);
    board.position(game.fen());
    updateStatus();
  });
  updateStatus();
}

vsAiBtn.addEventListener('click', startGameAI);
vsOnlineBtn.addEventListener('click', startGameOnline);
