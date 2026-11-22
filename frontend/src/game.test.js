import { describe, expect, it } from "vitest";
import { initialState, reducer } from "./game.js";

const server = (state, msg, now = 1000) => reducer(state, { kind: "server", msg, now });

describe("reducer", () => {
  it("joined -> waiting room with my letter", () => {
    const s = server(initialState, { type: "joined", you: "B" });
    expect(s.screen).toBe("waiting");
    expect(s.you).toBe("B");
  });

  it("busy -> busy screen, and closing afterwards does not turn it into an error", () => {
    let s = server(initialState, { type: "busy" });
    s = reducer(s, { kind: "closed" });
    expect(s.screen).toBe("busy");
  });

  it("chat phase sets round, end time and clears the old vote", () => {
    const before = { ...initialState, screen: "vote", myVote: "C" };
    const s = server(before, { type: "phase", phase: "chat", round: 2, rounds: 2, seconds: 60 }, 5000);
    expect(s).toMatchObject({ screen: "chat", round: 2, rounds: 2, endsAt: 65000, myVote: null });
  });

  it("collects chat messages in order", () => {
    let s = server(initialState, { type: "chat", round: 1, from: "A", text: "hi" });
    s = server(s, { type: "chat", round: 1, from: "C", text: "hello" });
    expect(s.messages.map((m) => m.from + ":" + m.text)).toEqual(["A:hi", "C:hello"]);
  });

  it("remembers my own vote", () => {
    const s = reducer({ ...initialState, screen: "vote" }, { kind: "voted", target: "A" });
    expect(s.myVote).toBe("A");
  });

  it("feedback phase keeps the tally", () => {
    const tally = { A: 1, B: 2, C: 0 };
    const s = server(initialState, { type: "phase", phase: "feedback", round: 1, rounds: 2, seconds: 8, tally });
    expect(s.screen).toBe("feedback");
    expect(s.tally).toEqual(tally);
  });

  it("result phase keeps the whole result and stops the countdown", () => {
    const msg = { type: "phase", phase: "result", winner: "C", totals: { A: 1, B: 2, C: 3 }, tie_break: null, round_tallies: [] };
    const s = server(initialState, msg);
    expect(s.screen).toBe("result");
    expect(s.result.winner).toBe("C");
    expect(s.endsAt).toBeNull();
  });

  it("connection closed in the middle of the game -> lost", () => {
    expect(reducer({ ...initialState, screen: "chat" }, { kind: "closed" }).screen).toBe("lost");
  });

  it("connection closed after the result is fine", () => {
    expect(reducer({ ...initialState, screen: "result" }, { kind: "closed" }).screen).toBe("result");
  });

  it("unknown messages are ignored", () => {
    expect(server(initialState, { type: "something-new" })).toBe(initialState);
  });
});
