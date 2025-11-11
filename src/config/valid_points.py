import random
from typing import List, Tuple, Union
from config import CONFIG

# Internal storage for samplers per profile
_SAMPLERS = {}

class NonRepeatingSampler:
    '''Pick random points without repeats until exhausted, then reshuffle.'''
    def __init__(self, points: List[Tuple[int,int]], seed: int = 42):
        self._all = points.copy()
        self._pool = []
        self._seed = seed
        self.reset()

    def reset(self):
        random.seed(self._seed)
        self._pool = self._all.copy()
        random.shuffle(self._pool)

    def pop(self, n: int = 1) -> List[Tuple[int,int]]:
        if n <= 0:
            return []
        if len(self._pool) < n:
            self.reset()
        return [self._pool.pop() for _ in range(n)]

def _get_points_from_config(profile: str) -> List[Tuple[int,int]]:
    '''Return screen pixel coordinates from CONFIG for the given profile.'''
    config_attr = f'valid_points_{profile}'
    if not hasattr(CONFIG, config_attr):
        raise ValueError(f'No valid points loaded in CONFIG for profile \'{profile}\'')

    raw = getattr(CONFIG, config_attr)
    pts = getattr(raw, 'points', [])
    normalized = getattr(raw, 'normalized', False)

    left = CONFIG.coords.left
    top = CONFIG.coords.top
    width = CONFIG.coords.width
    height = CONFIG.coords.height

    pixel_points = []
    if normalized:
        for nx, ny in pts:
            x = int(nx * width + left)
            y = int(ny * height + top)
            pixel_points.append((x, y))
    else:
        for x, y in pts:
            pixel_points.append((int(x + left), int(y + top)))
    return pixel_points

def pick_random_point(profile: str, n: int = 1) -> Union[Tuple[int,int], List[Tuple[int,int]]]:
    '''
    Return n non-repeating random points from the YAML already loaded in CONFIG.
    - If n=1, returns a single tuple (x, y)
    - If n>1, returns a list of tuples
    '''
    if profile not in _SAMPLERS:
        points = _get_points_from_config(profile)
        _SAMPLERS[profile] = NonRepeatingSampler(points)

    sampler = _SAMPLERS[profile]
    points = sampler.pop(n)

    return points[0] if n == 1 else points
