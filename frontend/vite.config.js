import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 5173 }, // host: true = reachable from outside a container too
  test: { environment: "jsdom" },     // tests run in a fake browser
});
