/* eslint-disable react/prop-types */
import { useContext, useState } from "react";
import { new_chat } from "../api";
import { GlobalContext } from "../context";

const Sidebar = ({ onSelectChat }) => {
  const { auth, setChats, chats } = useContext(GlobalContext);
  const [name, setName] = useState("");
  const [open, setOpen] = useState(false);

  const handleNewChat = async () => {
    try {
      const data = await new_chat({
        user_id: auth?._id,
        name,
      });
      if (data?.data) {
        setChats((state) => [...state, data.data]);
        setOpen(false);
        setName("");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="bg-primary-500 w-full h-full p-2">
      {open && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-md shadow-md w-96 z-50 p-2 flex flex-col bg-white">
          <button
            className="absolute top-1 right-1"
            onClick={() => setOpen(false)}
          >
            x
          </button>
          <label htmlFor="">Name</label>
          <input
            type="text"
            className="border"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button
            onClick={handleNewChat}
            className="bg-primary-500 text-white p-1 rounded-sm mt-2"
          >
            Submit
          </button>
        </div>
      )}
      <button
        className="w-full bg-white py-2 rounded-sm"
        onClick={() => setOpen(true)}
      >
        New Chat
      </button>
      <div className="flex flex-col gap-2 mt-4 h-[calc(100%-150px)] overflow-auto">
        {chats?.map((item) => (
          <button
            className="bg-white p-2 rounded-sm"
            key={item._id}
            onClick={() => onSelectChat(item._id)}
          >
            {item.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
