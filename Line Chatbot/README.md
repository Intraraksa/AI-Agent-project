# Line Chatbot with AI Integration
This project implements a Line messaging bot that uses a Gemini AI model to respond to user messages. 
The bot receives messages via Line's webhook, processes them with an AI assistant, and sends the responses back to users.

## Overview
The system consists of a FastAPI web server that:

1.Receives webhook events from Line's Messaging API
2.Processes message content using a Gemini AI model
3.Maintains conversation history for each user
4.Sends AI-generated responses back to users

<img src="https://creative.line.me/static/9e2af43154e78a39792871533568126e/0ef64/be4b9c191c5b4a98f52bc5c59b4482fc.png" alt="My Image" width="200">

You should make .env file to contain environment variables such as API keys or any Token
