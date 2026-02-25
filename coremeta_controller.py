"""
Meta-Controller: The orchestrator for the Autonomous Self-Replicating Trading Ecosystem.
Manages global capital allocation, component lifecycle, and evolutionary pressure.
"""
import asyncio
import traceback
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import structlog

from config.settings import settings
from utils.firebase_client import FirebaseClient
from utils.logger import EcosystemLogger

logger = EcosystemLogger(__name__).get_logger()

class ComponentStatus(str, Enum):
    """Status of ecosystem components"""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"
    TERMINATED = "terminated"
    EVOLVING = "evolving"

class ComponentType(str, Enum):
    """Types of components in the ecosystem"""
    GENERATOR = "strategy_generator"
    EVALUATOR = "strategy_evaluator"
    DEPLOYER = "strategy_deployer"
    RISK_MANAGER = "risk_manager"
    DATA_FEEDER = "data_feeder"

@dataclass
class ComponentMetrics: