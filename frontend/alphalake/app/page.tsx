"use client";
import CssBaseline from '@mui/material/CssBaseline';
import AIConversation from "../component/chatbox";
import { SideBar } from "../component/sidebar";
import SearchBar from "../component/searchbar";
import { useState } from "react";
export default function Dashboard(){
  const [sessionId, setSessionId] = useState<string>(() => crypto.randomUUID());
  const [searchTerm, setSearchTerm] = useState<string>("");
  const handleSelectConversation = (desiredSessionId: string) => {
    setSessionId(desiredSessionId);
  };
  return(
    <main>
      <CssBaseline/>
      <div className="max-w-6xl mx-auto flex flex-col gap-4">
        <h1 className="text-center text-3xl font-bold font-roboto">AlphaLake</h1>
      </div>
      <div className='grid grid-cols-[250px_1fr] h-[calc(100vh-4rem)] gap-4'>
        <div className="overflow-y-auto">
            <SideBar onSelect={handleSelectConversation}/>
        </div>
        <div className="grid grid-rows-[auto_1fr] h-full min-h-0 gap-4">
          <div>
            <SearchBar
              searchTerm={searchTerm}
              onSearchTermChange={setSearchTerm}
            />
          </div>
          <div className="min-h-0">
            <AIConversation
              session_id={sessionId}
              />
          </div>
        </div>
      </div>
    </main>
  )
}