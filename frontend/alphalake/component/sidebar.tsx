import { getAllConversations } from "@/utils/api";
import { useEffect } from "react";
import ChatIcon from '@mui/icons-material/Chat';

export function SideBar () {
    return (
        <div className="flex flex-col gap-4">
            <div className='flex items-center gap-2'>
                <ChatIcon/>
                <span>Conversations</span>
            </div>
        </div>
    );
    
}