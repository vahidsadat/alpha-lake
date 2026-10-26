"use client";
import CssBaseline from '@mui/material/CssBaseline';
import AIConversation from "../component/chatbox";
import { createChatSocket } from '../utils/api';
import { useState } from "react";
export default function Dashboard(){
  const [message, setMessage] = useState<string>("");
  const [sessionId] = useState<string>(() => crypto.randomUUID());

 
  return(
    <main>
      <CssBaseline/>
      <div className="max-w-6xl mx-auto flex flex-col gap-4">
        <h1 className="text-center text-3xl font-bold font-roboto">AlphaLake</h1>
      </div>
      <div className='flex flex-row gap-4'>
        <AIConversation
          session_id={sessionId}
          />
      </div>
    </main>
  )
}