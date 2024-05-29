import { io } from "socket.io-client";



const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
      return 'http://127.0.0.1:1337';
    } else {
      return `http://${host}:1337`;
    }
  } else {
    return 'http://127.0.0.1:1337';
  }
};

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || getApiBaseUrl();
export const socket = io(API_BASE_URL);



export async function executeNotebookapi(userInput) {
    console.log('Executing notebook with input:', userInput);
    const projectName = localStorage.getItem("selectedProject");
    const response = await fetch(`${API_BASE_URL}/executenotebook`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userInput,  project_name:   projectName })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Received response:', data);
        return data.html;
    } else {
        console.error('Failed to execute notebook');
        return '';
    }
}
