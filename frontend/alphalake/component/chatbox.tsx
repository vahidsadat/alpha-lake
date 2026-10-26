import { createChatSocket } from "@/utils/api";
import styled from "@emotion/styled";
import { useEffect,useRef,useState } from "react";
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';

const Input = styled.input`
    width: 100%;
    padding: 0.2rem;
    font-size: large;
`;
interface AIConversationProps {
  session_id: string;
}
const AIConversation = ({ session_id}: AIConversationProps ) => {
    const [message, setMessage] = useState<string>("");
    const [messages, setMessages] = useState<{ role: "user" | "assistant"; content: string }[]
    >([]);

    const socketRef = useRef<WebSocket | null>(null);
    useEffect(() => {
    const socket = createChatSocket();

    socket.onopen = () => {
      console.log("WebSocket OPEN");
    };

    socket.onmessage = (event) => {
      console.log("Received:", event.data);

      const data = JSON.parse(event.data);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket CLOSED");
    };

    socketRef.current = socket;

    return () => {
      socket.close();
    };
  }, []);
    const handleSend = () => {
        console.log("SEND BUTTON CLICKED");
      if (!message.trim()) return;  

      const socket = socketRef.current;
      console.log("Socket state:", socket?.readyState);
      if(!socket || socket.readyState !== WebSocket.OPEN){
        console.error("WebSocket is not open");
      return;
      }
      console.log("Sending:", message);
      setMessages((prev) => [
            ...prev,
            { role: "user", content: message}
        ]);
      socket.send(
        JSON.stringify({
          session_id,
          message
        })
      );

      setMessage("");
      };
    return(
    <main>
    <div className="w-full">
      <Input 
        type="text"
        placeholder="Search name..."
        className="w-full p-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
        <Button variant="contained" endIcon={<SendIcon />}
        onClick={handleSend}>
        Send
        </Button>
    </div>
    <div className="w-full min-h-[300px] border rounded-lg p-4 overflow-y-auto">
        {messages.map((msg, index) => (
            <div key={index}>
                <strong>
                    {msg.role ==="user" ? "You" : "AlphaLake"}:
                </strong>
                <p>{msg.content}</p>
            </div>
        ))}
    </div>
    </main>
    );
}

export default AIConversation;