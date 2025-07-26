import { useState } from "react";
import axios from "axios";

// ✅ Make sure this matches your deployed Railway backend
const API_URL = "https://ai-chatbot-fastapi-react-production.up.railway.app/chat";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const res = await axios.post(API_URL, { message: input });
      setResponse(res.data.response);
    } catch (err) {
      console.error("API Error:", err);
      if (err.response) {
        setResponse(`Error ${err.response.status}: ${err.response.data}`);
      } else if (err.request) {
        setResponse("No response from server.");
      } else {
        setResponse("Request error: " + err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>Chat with AI 🤖</h1>
      <textarea
        rows={3}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message here..."
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <br />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? "Typing..." : "Send"}
      </button>
      <div style={{ marginTop: 20 }}>
        <strong>Bot:</strong>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
