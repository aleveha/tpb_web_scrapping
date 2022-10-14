"""Data types for the TPB cv01 project"""
from dataclasses import dataclass


@dataclass
class Article:
    """Article class"""
    category: str
    comments_count: int
    content: str
    link: str
    photos_count: int
    publish_date: str
    title: str
