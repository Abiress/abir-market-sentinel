import numpy as np
from typing import List

class DifferentialEntropyCollector:
    def __init__(self, epsilon: float = 0.5, sample_count: int = 20):
        self.epsilon = epsilon
        self.sample_count = sample_count
        self.noise_history = []

    def collect(self) -> bytes:
        noise = np.random.laplace(0, 1.0 / self.epsilon, 32)
        noise_bytes = noise.astype(np.float32).tobytes()
        self.noise_history.append({
            'timestamp': len(self.noise_history),
            'entropy_length': len(noise_bytes)
        })
        return noise_bytes

    def get_noise_sample(self, count: int = 1) -> List[bytes]:
        return [self.collect() for _ in range(count)]

    def estimate_privacy_budget(self) -> float:
        return self.epsilon * len(self.noise_history)

    def reset_budget(self):
        self.noise_history = []

class SpectreDefender:
    def __init__(self):
        self.noise_injector = DifferentialEntropyCollector(epsilon=0.1)

    def inject_noise(self, data: np.ndarray) -> np.ndarray:
        noise = self.noise_injector.collect()
        noise_array = np.frombuffer(noise, dtype=np.float32)
        if len(noise_array) < len(data):
            noise_array = np.resize(noise_array, len(data))
        else:
            noise_array = noise_array[:len(data)]
        return data + noise_array

    def constant_time_compare(self, a: bytes, b: bytes) -> bool:
        return hmac.compare_digest(a, b)
