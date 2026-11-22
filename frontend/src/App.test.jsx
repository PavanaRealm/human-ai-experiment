// Runs the whole UI in a fake browser against a FAKE server (no backend needed).
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App.jsx";

class FakeWebSocket {
  static instances = [];
  constructor(url) {
    this.url = url;
    this.sent = []; // what the page sent to the "server"
    FakeWebSocket.instances.push(this);
  }
  send(data) { this.sent.push(JSON.parse(data)); }
  close() { this.onclose?.(); }
  emit(msg) { act(() => this.onmessage({ data: JSON.stringify(msg) })); } // the "server" sends a message
}

let ws;
beforeEach(() => {
  FakeWebSocket.instances = [];
  vi.stubGlobal("WebSocket", FakeWebSocket);
  render(<App />);
  ws = FakeWebSocket.instances[0];
});
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const phase = (extra) => ({ type: "phase", rounds: 2, seconds: 60, ...extra });
// Blind condition: no screen may ever contain a hint about who is human or AI
const noGiveaway = () => expect(document.body.textContent).not.toMatch(/\b(ai|human|bot|robot)\b/i);

describe("App", () => {
  it("connects to the backend on port 8000", () => {
    expect(ws.url).toMatch(/^ws:\/\/.+:8000\/ws$/);
    expect(screen.getByText("Connecting…")).toBeTruthy();
  });

  it("plays a whole game: waiting room, chat, vote, feedback, round 2, result", () => {
    ws.emit({ type: "joined", you: "A" });
    expect(screen.getByText("Waiting for the other participants…")).toBeTruthy();
    expect(document.body.textContent).toContain("You are Player A");
    noGiveaway();

    // round 1 chat
    ws.emit(phase({ phase: "chat", round: 1 }));
    fireEvent.change(screen.getByLabelText("Message"), { target: { value: "  I would pick B  " } });
    fireEvent.click(screen.getByText("Send"));
    expect(ws.sent).toContainEqual({ type: "chat", text: "I would pick B" }); // trimmed
    expect(screen.getByLabelText("Message").value).toBe(""); // input was cleared
    ws.emit({ type: "chat", round: 1, from: "A", text: "I would pick B" });
    ws.emit({ type: "chat", round: 1, from: "C", text: "Why B?" });
    expect(screen.getByText("Why B?")).toBeTruthy();
    expect(document.body.textContent).toContain("Player C:");
    noGiveaway();

    // vote
    ws.emit(phase({ phase: "vote", round: 1, seconds: 15 }));
    fireEvent.click(screen.getByText("Player B"));
    expect(ws.sent).toContainEqual({ type: "vote", target: "B" });
    expect(document.body.textContent).toContain("Your vote: Player B");
    fireEvent.click(screen.getByText("Player A (you)")); // changing the vote is allowed
    expect(ws.sent).toContainEqual({ type: "vote", target: "A" });

    // feedback shows counts, not who voted for whom
    ws.emit(phase({ phase: "feedback", round: 1, seconds: 8, tally: { A: 1, B: 2, C: 0 } }));
    expect(screen.getByText("Player B: 2 votes")).toBeTruthy();
    expect(screen.getByText("Player A (you): 1 vote")).toBeTruthy();
    noGiveaway();

    // round 2 starts with an empty chat and no old vote
    ws.emit(phase({ phase: "chat", round: 2 }));
    expect(screen.queryByText("Why B?")).toBeNull();
    expect(document.body.textContent).toContain("Round 2 of 2");

    // result
    ws.emit({ type: "phase", phase: "result", winner: "B", totals: { A: 1, B: 3, C: 2 }, tie_break: null,
              round_tallies: [{ A: 1, B: 2, C: 0 }, { A: 0, B: 1, C: 2 }] });
    expect(screen.getByText("Player B is the Decision Maker")).toBeTruthy();
    expect(document.body.textContent).toContain("Round 2: A 0, B 1, C 2");
    noGiveaway();
  });

  it("explains a tie break", () => {
    ws.emit({ type: "joined", you: "C" });
    ws.emit({ type: "phase", phase: "result", winner: "A", totals: { A: 3, B: 0, C: 3 }, tie_break: "last_round",
              round_tallies: [] });
    expect(document.body.textContent).toContain("the votes of the last round decided");
  });

  it("keeps working when the browser's scrollIntoView returns a Promise (real Chrome bug, found in a real browser)", () => {
    const original = window.HTMLElement.prototype.scrollIntoView;
    window.HTMLElement.prototype.scrollIntoView = vi.fn(() => Promise.resolve()); // jsdom has none, Chrome has one
    try {
      ws.emit({ type: "joined", you: "A" });
      ws.emit(phase({ phase: "chat", round: 1 }));
      ws.emit({ type: "chat", round: 1, from: "B", text: "first message" });
      expect(screen.getByText("first message")).toBeTruthy();   // the page is still there
      expect(window.HTMLElement.prototype.scrollIntoView).toHaveBeenCalled();
    } finally {
      window.HTMLElement.prototype.scrollIntoView = original;
    }
  });

  it("does not send an empty message", () => {
    ws.emit({ type: "joined", you: "A" });
    ws.emit(phase({ phase: "chat", round: 1 }));
    fireEvent.click(screen.getByText("Send"));
    expect(ws.sent).toEqual([]);
  });

  it("tells a third visitor that the experiment is running", () => {
    ws.emit({ type: "busy" });
    expect(document.body.textContent).toContain("already running");
  });

  it("shows an error when the connection drops in the middle of the game", () => {
    ws.emit({ type: "joined", you: "A" });
    ws.emit(phase({ phase: "chat", round: 1 }));
    act(() => ws.onclose());
    expect(screen.getByText("Connection lost.")).toBeTruthy();
  });
});
