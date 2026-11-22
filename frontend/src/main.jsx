import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

// No <React.StrictMode> on purpose: in development it starts every effect twice, which would
// open the WebSocket twice and take two player slots for one browser tab.
createRoot(document.getElementById("root")).render(<App />);
