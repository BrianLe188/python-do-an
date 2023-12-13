import axios from "axios";
import qs from "query-string";

export const load_chats = async (query) => {
  try {
    const querystring = qs.stringify(query);
    const data = await axios.get(`http://localhost:5001/chats?${querystring}`);
    return data.data;
  } catch (error) {
    console.log(error);
  }
};

export const login = async (query) => {
  try {
    const querystring = qs.stringify(query);
    const data = await axios.get(`http://localhost:5001/login?${querystring}`);
    return data.data;
  } catch (error) {
    console.log(error);
  }
};

export const new_chat = async (body) => {
  try {
    const data = await axios.post(`http://localhost:5001/new_chat`, body);
    return data.data;
  } catch (error) {
    console.log(error);
  }
};
