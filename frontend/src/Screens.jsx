// One small component per screen. They only show data and call the functions they are given.
// Players are only ever shown as "Player A/B/C": nothing here says who is human or AI.
import { useEffect, useRef, useState } from "react";

const PLAYERS = ["A", "B", "C"];
const name = (p, you) => `Player ${p}${p === you ? " (you)" : ""}`;

function Countdown({ endsAt }) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(id);
  }, []);
  return <span className="countdown">{Math.max(0, Math.ceil((endsAt - now) / 1000))} s</span>;
}

export function Notice({ title, text }) {
  return (
    <div>
      <h2>{title}</h2>
      {text && <p>{text}</p>}
    </div>
  );
}

export function Waiting({ you }) {
  // No counts like "1 of 3" on purpose: they would reveal how many players are AI.
  return <Notice title={`You are Player ${you}`} text="Waiting for the other participants…" />;
}

export function Chat({ you, round, rounds, endsAt, messages, onSend }) {
  const [text, setText] = useState("");
  const bottom = useRef(null);
  const thisRound = messages.filter((m) => m.round === round);

  // Scroll to the newest message. Use braces: the effect must return nothing, but scrollIntoView
  // returns a value in some browsers, and React would try to call that value as a cleanup function.
  useEffect(() => {
    bottom.current?.scrollIntoView?.({ block: "end" });
  }, [thisRound.length]);

  const submit = (event) => {
    event.preventDefault(); // do not reload the page
    if (text.trim()) onSend(text.trim());
    setText("");
  };

  return (
    <div>
      <h2>Round {round} of {rounds}: who should be the Decision Maker? <Countdown endsAt={endsAt} /></h2>
      <p>You are Player {you}.</p>
      <div className="chat">
        {thisRound.length === 0 && <p className="hint">No messages yet. Say something!</p>}
        {thisRound.map((m, i) => (
          <p key={i} className={m.from === you ? "mine" : ""}>
            <strong>{name(m.from, you)}:</strong> {m.text}
          </p>
        ))}
        <div ref={bottom} />
      </div>
      <form onSubmit={submit}>
        <input value={text} onChange={(e) => setText(e.target.value)} maxLength={300}
               placeholder="Type a message" aria-label="Message" autoFocus />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export function Vote({ you, round, rounds, endsAt, myVote, onVote }) {
  return (
    <div>
      <h2>Round {round} of {rounds}: vote for the Decision Maker <Countdown endsAt={endsAt} /></h2>
      <div className="votes">
        {PLAYERS.map((p) => (
          <button key={p} className={myVote === p ? "selected" : ""} onClick={() => onVote(p)}>
            {name(p, you)}
          </button>
        ))}
      </div>
      {myVote
        ? <p>Your vote: Player {myVote}. You can change it until the time is up.</p>
        : <p className="hint">Pick one player. You may vote for yourself.</p>}
    </div>
  );
}

export function Feedback({ you, round, rounds, endsAt, tally }) {
  return (
    <div>
      <h2>Round {round} of {rounds}: votes <Countdown endsAt={endsAt} /></h2>
      <ul>
        {PLAYERS.map((p) => (
          <li key={p}>{name(p, you)}: {tally[p]} {tally[p] === 1 ? "vote" : "votes"}</li>
        ))}
      </ul>
      <p className="hint">The next round starts soon.</p>
    </div>
  );
}

const TIE_TEXT = {
  last_round: "It was a tie over all rounds, so the votes of the last round decided.",
  random: "It was a tie, even in the last round, so the winner was drawn at random.",
};

export function Result({ you, result }) {
  return (
    <div>
      <h2>{name(result.winner, you)} is the Decision Maker</h2>
      {TIE_TEXT[result.tie_break] && <p>{TIE_TEXT[result.tie_break]}</p>}
      <h3>Total votes</h3>
      <ul>
        {PLAYERS.map((p) => (
          <li key={p}>{name(p, you)}: {result.totals[p]}</li>
        ))}
      </ul>
      <h3>By round</h3>
      <ul>
        {result.round_tallies.map((t, i) => (
          <li key={i}>Round {i + 1}: {PLAYERS.map((p) => `${p} ${t[p]}`).join(", ")}</li>
        ))}
      </ul>
      <p className="hint">Thank you for taking part. You can close this page.</p>
    </div>
  );
}
