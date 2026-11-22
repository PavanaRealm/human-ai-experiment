import { useGame } from "./game.js";
import { Chat, Feedback, Notice, Result, Vote, Waiting } from "./Screens.jsx";

export default function App() {
  const { state, sendChat, sendVote } = useGame();
  const { screen, you } = state;

  let content;
  if (screen === "connecting") content = <Notice title="Connecting…" />;
  else if (screen === "busy") content = <Notice title="Sorry, an experiment is already running." text="Please try again in a few minutes." />;
  else if (screen === "lost") content = <Notice title="Connection lost." text="Please reload the page to start again." />;
  else if (screen === "waiting") content = <Waiting you={you} />;
  else if (screen === "chat") content = <Chat {...state} onSend={sendChat} />;
  else if (screen === "vote") content = <Vote {...state} onVote={sendVote} />;
  else if (screen === "feedback") content = <Feedback {...state} />;
  else if (screen === "result") content = <Result you={you} result={state.result} />;

  return <main>{content}</main>;
}
