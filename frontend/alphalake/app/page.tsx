"use client";
import CssBaseline from '@mui/material/CssBaseline';
import AIConversation from "../component/chatbox";
import { SideBar } from "../component/sidebar";
import { useState } from "react";
export default function Dashboard(){
  const [sessionId, setSessionId] = useState<string>(() => crypto.randomUUID());
  const handleSelectConversation = (desiredSessionId: string) => {
    setSessionId(desiredSessionId);
  };
  return(
    <main>
      <CssBaseline/>
      <div className="max-w-6xl mx-auto flex flex-col gap-4">
        <h1 className="text-center text-3xl font-bold font-roboto">AlphaLake</h1>
      </div>
      <div className='grid grid-cols-[250px_1fr] gap-4'>
        <div >
            <SideBar onSelect={handleSelectConversation}/>
        </div>
        <div>
          <AIConversation
            session_id={sessionId}
            />
        </div>
      </div>
    </main>
  )
}