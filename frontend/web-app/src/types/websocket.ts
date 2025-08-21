export interface MessageRequest {
    type: 'join_room' | 'leave_room' | 'message';
    content: string;
    room_id: string;
    user_id: string;
    timestamp: string;
  }
  
  export interface MessageResponse {
    type: string;
    content: string;
    room_id: string;
    user_id: string;
    timestamp: string;
  }