/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable react/prop-types */
import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { load_chats } from "../api";

export const GlobalContext = React.createContext();

export default function GlobalContextProvider({ children }) {
  const [auth, setAuth] = useState(JSON.parse(localStorage.getItem("auth")));
  const [socket, setSocket] = useState(null);
  const [chats, setChats] = useState([]);

  useEffect(() => {
    if (auth) {
      loadChats();
      const sock = io("ws://localhost:5001");
      setSocket(sock);
    }
  }, [auth?._id]);

  useEffect(() => {
    const handleNewMessage = (data) => {
      const _chats = [...chats].map((item) => {
        if (item._id === data.in) {
          item["messages"] = [...item["messages"], data];
        }
        return item;
      });
      setChats(_chats);
    };

    const handleGetMessages = (data) => {
      const _chats = [...chats].map((item) => {
        if (item._id === data.in) {
          item["messages"] = data.data;
        }
        return item;
      });
      setChats(_chats);
    };

    socket?.on("get_messages", handleGetMessages);
    socket?.on("new_message", handleNewMessage);

    return () => {
      socket?.off("new_message", handleNewMessage);
      socket?.off("get_messages", handleGetMessages);
    };
  }, [socket, chats]);

  const loadChats = async () => {
    try {
      const data = await load_chats({ user_id: auth?._id });
      setChats(data.data.map((item) => ({ ...item, messages: [] })));
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <GlobalContext.Provider
      value={{
        auth,
        setAuth,
        socket,
        setChats,
        chats,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
}
