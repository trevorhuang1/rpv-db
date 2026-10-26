import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Base, Material, Result, Source

