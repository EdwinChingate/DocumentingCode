from __future__ import annotations



def default_third_party_map() -> Dict[str, str]:
    """
    Return the default alias → full import line map for third-party libraries.
    Defined as a function so it is never a module-level variable.
    No global variables, no classes.
    """
    return {
        "np"          : "import numpy as np",
        "pd"          : "import pandas as pd",
        "plt"         : "import matplotlib.pyplot as plt",
        "sns"         : "import seaborn as sns",
        "px"          : "import plotly.express as px",
        "go"          : "import plotly.graph_objects as go",
        "tf"          : "import tensorflow as tf",
        "torch"       : "import torch",
        "nn"          : "from torch import nn",
        "F"           : "from torch.nn import functional as F",
        "cv2"         : "import cv2",
        "yaml"        : "import yaml",
        "toml"        : "import toml",
        "tqdm"        : "from tqdm import tqdm",
        "requests"    : "import requests",
        "aiohttp"     : "import aiohttp",
        "pydantic"    : "import pydantic",
        "boto3"       : "import boto3",
        "redis"       : "import redis",
        "celery"      : "import celery",
        "sqlalchemy"  : "import sqlalchemy",
        "psycopg2"    : "import psycopg2",
        "pymongo"     : "import pymongo",
        "paramiko"    : "import paramiko",
        "sklearn"     : "import sklearn",
        "scipy"       : "import scipy",
        "nx"          : "import networkx as nx",
        "sp"          : "import scipy as sp",
    }
