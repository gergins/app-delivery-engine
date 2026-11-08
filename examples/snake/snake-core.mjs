// Pure, dependency-free game rules. No DOM, timers, storage or framework.
export function initialState(size = 16) {
  if (!Number.isInteger(size) || size < 4) throw new Error("size must be an integer >= 4");
  const mid = Math.floor(size / 2);
  return { size, snake: [{ x: mid, y: mid }], direction: "right", food: { x: mid + 1, y: mid }, score: 0, status: "playing" };
}
const VECTORS = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
const OPPOSITE = { up: "down", down: "up", left: "right", right: "left" };
export function nextFood(size, snake, random = Math.random) {
  const occupied = new Set(snake.map(({ x, y }) => y * size + x));
  const free = [];
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++)
    if (!occupied.has(y * size + x)) free.push({ x, y });
  if (!free.length) return null;
  const n = random();
  if (!Number.isFinite(n) || n < 0 || n >= 1) throw new Error("random must return [0,1)");
  return free[Math.floor(n * free.length)];
}
export function turn(state, direction) {
  if (state.status !== "playing" || !(direction in VECTORS) || direction === OPPOSITE[state.direction]) return state;
  return { ...state, direction };
}
export function step(state, random = Math.random) {
  if (state.status !== "playing") return state;
  const [dx, dy] = VECTORS[state.direction];
  const head = { x: state.snake[0].x + dx, y: state.snake[0].y + dy };
  const eating = !!state.food && head.x === state.food.x && head.y === state.food.y;
  // The tail vacates its cell on a non-growing step.
  const body = eating ? state.snake : state.snake.slice(0, -1);
  if (head.x < 0 || head.y < 0 || head.x >= state.size || head.y >= state.size ||
      body.some(p => p.x === head.x && p.y === head.y)) return { ...state, status: "gameover" };
  const snake = [head, ...state.snake].slice(0, state.snake.length + (eating ? 1 : 0));
  const food = eating ? nextFood(state.size, snake, random) : state.food;
  return { ...state, snake, food, score: state.score + (eating ? 1 : 0), status: food === null ? "won" : "playing" };
}
