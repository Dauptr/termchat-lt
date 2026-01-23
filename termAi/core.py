import numpy as np

class Tensor:
    def __init__(self, data, requires_grad=False):
        # Ensure data is a numpy array
        self.data = np.array(data)
        self.requires_grad = requires_grad
        self.grad = None
        self._backward = lambda: None

    def __repr__(self):
        return f"Tensor(data={self.data}, grad={self.grad})"

    def backward(self):
        # Topological sort for backpropagation (simplified)
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                # If we had a computation graph history, we would traverse parents here
                topo.append(v)
        build_topo(self)
        
        # Go backwards
        for node in reversed(topo):
            node._backward()

    # Example basic operation: Addition
    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data)

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        
        out._backward = _backward
        return out

    # Example basic operation: Multiplication
    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data)

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

class Softmax:
    def __init__(self):
        pass
    
    def __call__(self, x_tensor):
        # Shift data for numerical stability
        exp_data = np.exp(x_tensor.data - np.max(x_tensor.data))
        softmax_data = exp_data / np.sum(exp_data)
        return Tensor(softmax_data)