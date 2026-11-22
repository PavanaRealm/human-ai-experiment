// The whole client-side game state lives here: one reducer (a plain function) + one hook that owns the WebSocket.
import { useEffect, useReducer, useRef } from "react";

// Where the backend is. Same machine as the page, port 8000. Can be overridden with VITE_WS_URL.
const WS_URL = import.meta.env.VITE_WS_URL || `ws://${window.location.hostname}:8000/ws`;

export const initialState = {
  screen: "connecting", // connecting | waiting | chat | vote | feedback | result | busy | lost
  you: null,            // my letter, "A" / "B" / "C"
  round: 0,
  rounds: 0,
  endsAt: null,         // time (ms) when the current phase ends, for the countdown
  messages: [],         // all chat messages: { round, from, text }
  myVote: null,         // who I voted for in this round
  tally: null,          // vote counts of the last round (feedback screen)
  result: null,         // final result (result screen)
};

// reducer(oldState, action) -> newState. It never changes the old state and never reads the clock,
// so it is easy to test. "now" is passed in by the caller.
export function reducer(state, action) {
  if (action.kind === "voted") return { ...state, myVote: action.target };

  if (action.kind === "closed") {
    // connection ended: fine after the result or when turned away, otherwise it is an error
    return state.screen === "result" || state.screen === "busy" ? state : { ...state, screen: "lost" };
  }

  // action.kind === "server": a message from the backend
  const msg = action.msg;
  switch (msg.type) {
    case "joined":
      return { ...state, screen: "waiting", you: msg.you };
    case "busy":
      return { ...state, screen: "busy" };
    case "chat":
      return { ...state, messages: [...state.messages, { round: msg.round, from: msg.from, text: msg.text }] };
    case "phase": {
      const common = { ...state, round: msg.round ?? state.round, rounds: msg.rounds ?? state.rounds,
                       endsAt: action.now + (msg.seconds ?? 0) * 1000 };
      if (msg.phase === "chat") return { ...common, screen: "chat", myVote: null };
      if (msg.phase === "vote") return { ...common, screen: "vote", myVote: null };
      if (msg.phase === "feedback") return { ...common, screen: "feedback", tally: msg.tally };
      if (msg.phase === "result") return { ...common, screen: "result", endsAt: null, result: msg };
      return state;
    }
    default:
      return state;
  }
}

export function useGame() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const socket = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    socket.current = ws;
    ws.onmessage = (event) => dispatch({ kind: "server", msg: JSON.parse(event.data), now: Date.now() });
    ws.onclose = () => dispatch({ kind: "closed" });
    return () => ws.close();
  }, []);

  const send = (obj) => socket.current?.send(JSON.stringify(obj));

  return {
    state,
    sendChat: (text) => send({ type: "chat", text }),
    sendVote: (target) => {
      send({ type: "vote", target });
      dispatch({ kind: "voted", target });
    },
  };
}
