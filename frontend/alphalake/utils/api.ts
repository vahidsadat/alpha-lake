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
    const response = await fetch(`${API_BASE_URL}/v1/conversations`, { method: 'GET'})
    return response
  }catch(error){
    console.log("Transition error", error);
  }
  
}

export async function getConversation(session_id:string){
  try{
    const response = await fetch(`${API_BASE_URL}/v1/conversations/${session_id}/messages`, { method: 'GET'})
    return response
  }catch(error){
    console.log("Transition error", error);
  }
}

export async function deleteConversation(session_id:string){
  try{
    const response = await fetch(`${API_BASE_URL}/v1/conversations/${session_id}`, { method: 'DELETE'})
    return response
  }catch(error){
    console.log("Transition error", error);
  }
}

export async function renameConversation(session_id:string, newTitle:string){
  try{
    const response = await fetch(`${API_BASE_URL}/v1/conversations/${session_id}/title`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: newTitle }),
    });
    return response;
  }catch(error){
    console.log("Transition error", error);
  }
}
