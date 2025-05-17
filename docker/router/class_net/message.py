"""
Message Formatting Module

This module provides utilities for formatting console messages with colors
using RGB values for better visual feedback in the application.
"""

from typing import Tuple

class Mensagem:
    """
    A class for formatting console messages with colors.
    
    Provides static methods for formatting messages with custom RGB colors,
    including predefined formats for success and error messages.
    """
    
    def __init__(self):
        """Initialize a Mensagem instance."""
        pass
    
    @staticmethod
    def formatar_mensagem(message: str, rgb_color: Tuple[int, int, int]) -> str:
        """
        Format a message with custom RGB color coding.
        
        Args:
            message: The message to be formatted
            rgb_color: RGB color values as (red, green, blue)
            
        Returns:
            str: ANSI color-formatted message
        """
        red, green, blue = rgb_color
        return f"\033[38;2;{red};{green};{blue}m{message}\033[0m"
    
    @staticmethod
    def formatar_sucesso(message: str) -> str:
        """
        Format a success message in green color.
        
        Args:
            message: The success message to be formatted
            
        Returns:
            str: Green-colored formatted message
        """
        return Mensagem.formatar_mensagem(message, (0, 255, 0))
    
    @staticmethod
    def formatar_erro(message: str) -> str:
        """
        Format an error message in red color.
        
        Args:
            message: The error message to be formatted
            
        Returns:
            str: Red-colored formatted message
        """
        return Mensagem.formatar_mensagem(message, (255, 0, 0))