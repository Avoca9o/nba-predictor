import threading
from typing import List, Optional, Dict


class DurationStorage:
    def __init__(self, max_size: Optional[int] = None):
        self._durations: List[float] = []
        self._sorted_durations: List[float] = []
        self._lock = threading.RLock()
        self._max_size = max_size
        self._actual = True
        self._total_sum = 0.0
        self._total_count = 0
        
    def add(self, duration: float) -> None:
        if duration < 0:
            raise ValueError("Duration must be non-negative")
        
        with self._lock:
            self._total_sum += duration
            self._total_count += 1
            
            self._durations.append(duration)
            self._actual = False
            
            if self._max_size is not None and len(self._durations) > self._max_size:
                self._remove_oldest()
    
    
    def _remove_oldest(self) -> None:
        if not self._durations:
            return
        
        removed = self._durations.pop(0)
        self._total_sum -= removed
        self._total_count -= 1
        self._actual = False

    
    def _ensure_sorted(self) -> None:
        if not self._actual:
            with self._lock:
                if not self._actual:
                    self._sorted_durations = self._durations.copy()
                    self._sorted_durations.sort()
                    self._sorted = True
    

    def get_percentile(self, percentile: float) -> Optional[float]:
        if not self._durations:
            return None
        
        self._ensure_sorted()
        
        with self._lock:
            n = len(self._sorted_durations)
            
            if percentile == 0:
                return self._durations[0]
            elif percentile == 100:
                return self._durations[-1]
            
            k = (percentile / 100.0) * (n - 1)
            lower = int(k)
            
            if lower == n - 1:
                return self._durations[lower]
            
            fraction = k - lower
            return self._durations[lower] + fraction * (self._durations[lower + 1] - self._durations[lower])
    

    def get_mean(self) -> Optional[float]:
        if self._total_count == 0:
            return None
        return self._total_sum / self._total_count
    

class RequestsStorage:
    def __init__(self):
        self._total_req_length = 0.0
        self._req_count = 0
        self._lock = threading.RLock()

    def add(self, req_length: int) -> None:
        with self._lock:
            self._req_count += 1
            self._total_req_length += req_length

    def get_req_data(self) -> float:
        return self._total_req_length / self._req_count
