import type { ChatMessage } from "@/types/chat";

type MessageListProps = {
  messages: ChatMessage[];
};

export function MessageList({ messages }: MessageListProps) {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <div key={message.id} className={`message ${message.role}`}>
          <div className="message-role">{message.role}</div>
          <div>{message.content}</div>
        </div>
      ))}
    </div>
  );
}
