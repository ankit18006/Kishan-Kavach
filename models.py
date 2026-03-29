from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    role: str
    phone: str = ''
    created_at: Optional[str] = None


@dataclass
class Device:
    id: int
    device_id: str
    owner_id: int
    name: str = 'My Device'
    location: str = ''
    created_at: Optional[str] = None


@dataclass
class AccessControl:
    id: int
    farmer_id: int
    owner_id: int
    device_id: Optional[int]
    status: str = 'pending'
    requested_at: Optional[str] = None
    responded_at: Optional[str] = None


@dataclass
class SensorData:
    id: int
    device_id: str
    temperature: float
    humidity: float
    gas: float
    battery: float
    spoilage_level: str = 'LOW'
    timestamp: Optional[str] = None


@dataclass
class AlertLog:
    id: int
    device_id: str
    alert_type: str
    message: str = ''
    sent_at: Optional[str] = None
