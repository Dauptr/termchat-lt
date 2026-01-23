import numpy as np
import random
from .core import Tensor, Softmax

class Linear:
    def __init__(self, in_features, out_features):
        self.weights = Tensor(np.random.randn(in_features, out_features) * 0.1)
        self.bias = Tensor(np.zeros(out_features))

    def __call__(self, x):
        # x * weights + bias
        return Tensor(np.dot(x.data, self.weights.data) + self.bias.data)
    
    def parameters(self):
        return [self.weights, self.bias]

class Embedding:
    def __init__(self, vocab_size, embed_size):
        self.weights = Tensor(np.random.randn(vocab_size, embed_size) * 0.1)
    
    def __call__(self, x):
        # Simple lookup - in practice this would be more sophisticated
        return Tensor(self.weights.data[x] if isinstance(x, int) else self.weights.data)

class SelfAttention:
    def __init__(self, embed_size):
        # Weights for Query, Key, and Value
        self.W_q = Tensor(np.random.randn(embed_size, embed_size) * 0.1)
        self.W_k = Tensor(np.random.randn(embed_size, embed_size) * 0.1)
        self.W_v = Tensor(np.random.randn(embed_size, embed_size) * 0.1)
        self.softmax = Softmax()

    def __call__(self, x_tensor):
        # x_tensor shape: (context_length, embed_size)
        
        # 1. Calculate Q, K, V (Query, Key, Value)
        # This represents: "What am I looking for?", "What do I contain?", "What do I offer?"
        Q = np.dot(x_tensor.data, self.W_q.data)
        K = np.dot(x_tensor.data, self.W_k.data)
        V = np.dot(x_tensor.data, self.W_v.data)
        
        # 2. Attention Scores
        # How much focus should word A put on word B?
        score = np.dot(Q, K.T) 
        
        # 3. Scale (prevent numbers from getting too huge)
        embed_size = K.shape[1]
        scaled_scores = score / np.sqrt(embed_size)
        
        # 4. Softmax (Convert to probabilities)
        attention_weights = self.softmax(Tensor(scaled_scores)).data
        
        # 5. Weighted Sum
        # The final output is the sum of values, weighted by attention
        output_data = np.dot(attention_weights, V)
        
        return Tensor(output_data)

class TransformerBlock:
    def __init__(self, embed_size):
        self.attention = SelfAttention(embed_size)
        # In a full model, you would add a FeedForward Network here
    
    def __call__(self, x):
        # "Residual connection" helps gradient flow
        attended = self.attention(x)
        
        # Add the input back to the output (Helps the AI learn faster)
        # Note: Simplified element-wise addition
        return Tensor(attended.data + x.data)

class MiniGPT:
    def __init__(self, vocab_size, embed_size, num_layers):
        self.embedding = Embedding(vocab_size, embed_size)
        # STACK THE BLOCKS - This is "Scaling"
        self.blocks = [TransformerBlock(embed_size) for _ in range(num_layers)]
        self.head = Linear(embed_size, vocab_size) # Output layer

    def __call__(self, x):
        x = self.embedding(x)
        
        # Pass data through every layer in the stack
        for block in self.blocks:
            x = block(x)
            
        logits = self.head(x)
        return logits

class SimpleChatBot:
    def __init__(self, vocab_size=10):
        self.vocab_size = vocab_size
        # 1. The Brain: A Linear layer
        # In a real LLM, this would be a massive stack of Transformer layers
        self.layer = Linear(in_features=vocab_size, out_features=vocab_size)
        self.softmax = Softmax()
        
        # A fake "memory" mapping input IDs to output probabilities
        # This simulates a trained brain for demonstration
        self.memory = {} 

    def think(self, input_text):
        # Simulate turning text into numbers (Tokenization)
        # In a real app, you would use a proper tokenizer here
        input_id = hash(input_text) % self.vocab_size
        
        # Create a one-hot vector (the input tensor)
        input_vector = np.zeros(self.vocab_size)
        input_vector[input_id] = 1.0
        x = Tensor(input_vector)

        # 2. Forward Pass: The "Thought Process"
        logits = self.layer(x)       # Raw calculations
        probabilities = self.softmax(logits) # Convert to chances
        
        # 3. Decoding: Pick the next word based on probability
        predicted_id = np.argmax(probabilities.data)
        
        # Map ID back to a word (Reverse Tokenization)
        responses = [
            "Hello!", "How are you?", "Tell me more.", 
            "That is interesting.", "Why?", 
            "I am learning.", "TermChat is cool.", 
            "Data is power.", "Computing...", "Error."
        ]
        
        return responses[predicted_id]