import json
import aiohttp
from typing import Dict, Any, List, Optional, Union

class Odacova:
    """A client for interacting with the Odacova API.

    param base_url: The base URL of the Odacova API.
    type base_url: str
    param bot_token: The authentication token to use when making API requests.
    type bot_token: str
    """
    def __init__(self, base_url: str, bot_token: str):
        """
        Initialize a new instance of the Odacova client.

        param base_url: The base URL of the Odacova API.
        type base_url: str
        param bot_token: The authentication token to use when making API requests.
        type bot_token: str
        """
        self.base_url = base_url
        self.bot_token = bot_token
        self.session = aiohttp.ClientSession()
        self.headers = {'Authorization': f'Bearer {bot_token}'}

        if not bot_token:
            raise ValueError('Missing bot token.')
        
        if not base_url:
            raise ValueError('Missing base URL.')
        
        if not base_url.startswith('http'):
            raise ValueError('Base URL must start with http or https.')
        
        if not base_url.endswith('/'):
            self.base_url = f'{base_url}/'

    async def _handle_response(self, response: aiohttp.ClientResponse)-> Union[Dict[str, Any], None]:
        """
        Handle the response from an API request.

        :param response: The response object from the API request.
        :type response: aiohttp.ClientResponse
        :return: The data from the response, or None if there was an error.
        :rtype: Union[Dict[str, Any], None]
        :raises ValueError: If the response contains an error status code.
        """
        try:
            response.raise_for_status()
            response_text = await response.text()
            return json.loads(response_text)
        except (aiohttp.ClientError, json.JSONDecodeError, ValueError) as e:
            print(f'Error handling response: {e}')
            return None

    async def get_events(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """
        Get a list of events from the API.

        Returns:
            List of dictionaries containing event data, or None if there are no events.
        Raises:
            ValueError: If the token is invalid, the resource is not found, or a server error occurs.
        """
        async with self.session.get(f'{self.base_url}/events', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def get_heartbeat(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """
        Returns the current state of the bot. This should be called every 5 minutes to keep the bot's connection to the server
        alive. 

        Returns:
            If successful, returns a list of event dictionaries that occurred since the last heartbeat. If no events occurred,
            an empty list is returned. If the request is unsuccessful, returns None.
        Raises:
            ValueError: If the request returns a status code of 401 (invalid token), 403 (forbidden), or >= 500 (server error).
            ValueError: If the request returns a status code of 404 (resource not found), or if the response cannot be decoded
            into JSON.
        """
        async with self.session.get(f'{self.base_url}/heartbeat', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def get_channels(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """
        Returns a list of all channels in the server. 

        Returns:
            If successful, returns a list of dictionaries, where each dictionary corresponds to a channel in the server.
            If the server has no channels, an empty list is returned. If the request is unsuccessful, returns None.
        Raises:
            ValueError: If the request returns a status code of 401 (invalid token), 403 (forbidden), or >= 500 (server error).
            ValueError: If the request returns a status code of 404 (resource not found), or if the response cannot be decoded
            into JSON.
        """
        async with self.session.get(f'{self.base_url}/channels', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def get_users(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """
        Returns a list of all users in the server. 

        Returns:
            If successful, returns a list of dictionaries, where each dictionary corresponds to a user in the server.
            If the server has no users, an empty list is returned. If the request is unsuccessful, returns None.
        Raises:
            ValueError: If the request returns a status code of 401 (invalid token), 403 (forbidden), or >= 500 (server error).
            ValueError: If the request returns a status code of 404 (resource not found), or if the response cannot be decoded
            into JSON.
        """
        async with self.session.get(f'{self.base_url}/users', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def get_bots(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """
        Returns a list of all bots in the server. 

        Returns:
            If successful, returns a list of dictionaries, where each dictionary corresponds to a bot in the server.
            If the server has no bots, an empty list is returned. If the request is unsuccessful, returns None.
        Raises:
            ValueError: If the request returns a status code of 401 (invalid token), 403 (forbidden), or >= 500 (server error).
            ValueError: If the request returns a status code of 404 (resource not found), or if the response cannot be decoded
            into JSON.
        """
        async with self.session.get(f'{self.base_url}/bots', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore
    
    async def route_bot(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        async with self.session.get(f'{self.base_url}/route_bot', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def on_ready(self):
        """Called when the bot is ready to start processing events."""
        pass  # Implement your logic here
    
    async def on_message(self, message):
        """Called when a new message is received.
        
        Parameters:
        -----------
        message : dict
            A dictionary containing information about the received message.
        """  
        pass  # Implement your logic here

    async def post_message(self, message: str, token: str) -> Optional[Union[List[Dict[str, Any]], None]]:
        """Send a message to the server.
        
        Parameters:
        -----------
        message : str
            The message to send.
        user : str
            The user to send the message to. If None, the message is sent to the server.
        """  
        
        test_headers = {"Content-Type": "application/json"}
        test_data = {"message": message, "token": token}
        
        async with self.session.post(f'{self.base_url}/chat', headers=test_headers, json=test_data) as response:
            return await self._handle_response(response) # type: ignore

    async def get_message(self) -> Optional[Union[List[Dict[str, Any]], None]]:
        """Get a message from the server.
        
        Parameters:
        -----------
        message : str
            The message to send.
        user : str
            The user to send the message to. If None, the message is sent to the server.
        """  
        async with self.session.get(f'{self.base_url}/chat', headers=self.headers) as response:
            return await self._handle_response(response) # type: ignore

    async def on_message_edit(self, message):
        """Called when a message is edited.
        
        Parameters:
        -----------
        message : dict
            A dictionary containing information about the edited message.
        """  
        pass  # Implement your logic here

    async def on_member_join(self, message):
        """Called when a new member joins the server.
        
        Parameters:
        -----------
        message : dict
            A dictionary containing information about the new member.
        """  
        pass  # Implement your logic here
    
    async def on_member_leave(self, message):
        """Called when a member leaves the server.
        
        Parameters:
        -----------
        message : dict
            A dictionary containing information about the member who left.
        """  
        pass # Implement your logic here
    
    async def terminate(self):
        """Close the client session and frees memory."""
        await self.session.close()
        
    