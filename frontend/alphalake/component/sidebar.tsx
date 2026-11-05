'use client';
import { getAllConversations, deleteConversation, renameConversation } from "@/utils/api";
import { useEffect, useState } from "react";
import AddCommentIcon from '@mui/icons-material/AddComment';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import ClickAwayListener from "@mui/material/ClickAwayListener";


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
    const [openMenuSessionId, setOpenMenuSessionId] = useState<string | null>(null);
    const [selectedOption, setSelectedOption] = useState<string | null>(null);
    

    const options = ["delete", "rename"]

    const handleOptionClick = (option: string) => {
        setSelectedOption(option);
        if (option === "delete" && openMenuSessionId) {
            deleteConversation(openMenuSessionId)
                .then(() => {
                    setConversations(prev => prev.filter(conversation => conversation.session_id !== openMenuSessionId));
                    setOpenMenuSessionId(null);
                })
                .catch(error => {
                    console.error("Error deleting conversation:", error);
                });
        }
        if (option === "rename" && openMenuSessionId) {
            const newTitle = prompt("Enter new title:");
            if (newTitle) {
                renameConversation(openMenuSessionId, newTitle)
                    .then(() => {
                        setConversations(prev => prev.map(conversation => conversation.session_id === openMenuSessionId ? { ...conversation, title: newTitle } : conversation));
                        setOpenMenuSessionId(null);
                    })
                    .catch(error => {
                        console.error("Error renaming conversation:", error);
                    });
            }
        }
    };
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
            <div className='flex items-center cursor-pointer gap-2' onClick={() => {onSelect(crypto.randomUUID())}}>
                <AddCommentIcon/>
                <span>New Chat</span>
            </div>
            <div className='flex flex-col gap-2'>
                {conversations.map((conversation) => (
                    <div key={conversation.session_id}
                    className='group relative p-2 cursor-pointer hover:bg-gray-100'
                    >
                        <div onClick={() => onSelect(conversation.session_id)}>{conversation.title}</div>
                        <MoreHorizIcon className='invisible group-hover:visible' onClick={() => {setOpenMenuSessionId(conversation.session_id)}}/>
                        {openMenuSessionId === conversation.session_id && (
                        <ClickAwayListener onClickAway={() => setOpenMenuSessionId(null)}>
                            <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-300 rounded-md shadow-lg z-10">
                                {options.map((option) => (
                                    <div
                                        key={option}
                                        className="px-4 py-2 cursor-pointer hover:bg-gray-100"
                                        onClick={() => handleOptionClick(option)}
                                    >
                                        {option}
                                    </div>
                                ))}
                            </div>
                            </ClickAwayListener>
                        )}
                        
                    </div>
                ))}

            </div>
        </div>
    );
    
}