import { error } from "console";

const isServer = typeof window === 'undefined';

export const API_BASE_URL = isServer
? 'http://backend-api:8000' 
  : 'http://localhost:8000';

  export const WS_BASE_URL = isServer
? 'ws://backend-api:8000' 
  : 'ws://localhost:8000';

export function createChatSocket(){
    return new WebSocket(`${WS_BASE_URL}/v1/ws/chat`)
}

export async function getAllConversations(){
  try{
    const response = await fetch(`/v1/conversations`, { method: 'GET'})
    return response
  }catch(error){
    console.log("Transition error", error);
  }
  
}
