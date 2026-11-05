'use client';
import { getAllConversations } from "@/utils/api";
import { useEffect, useState } from "react";
import ChatIcon from '@mui/icons-material/Chat';

interface Conversation {
    session_id: string;
    title: string;
    updated_at: string;
}

interface SideBarProps {
    onSelect: (sessionId: string) => void;
}

export function SideBar ( { onSelect }: SideBarProps ) {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    useEffect(() => {
        const fetchConversations = async () => {
            const response = await getAllConversations();
            if (response) {
                const data = await response.json();
                console.log("Fetched conversations:", data);
                setConversations(data);
            }
        };
        fetchConversations();
    }, []);
    return (
        <div className="flex flex-col gap-4">
            <div className='flex items-center gap-2'>
                <ChatIcon/>
                <span>Conversations</span>
            </div>
            <div className='flex flex-col gap-2'>
                {conversations.map((conversation) => (
                    <div key={conversation.session_id} className='p-2 cursor-pointer hover:bg-gray-100' onClick={() => onSelect(conversation.session_id)}>
                        {conversation.title}
                    </div>
                ))}

            </div>
        </div>
    );
    
}