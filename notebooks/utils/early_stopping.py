from tensorflow.keras.callbacks import EarlyStopping, Callback
import numpy as np

class CustomEarlyStopping(Callback):
    def __init__(self, monitor='val_accuracy', min_improvement=0.02, patience=10):
        super().__init__()
        self.monitor = monitor
        self.min_improvement = min_improvement
        self.patience = patience
        # Initialize based on metric type
        if 'loss' in monitor.lower():
            self.best_score = np.inf  # For loss, lower is better
        else:
            self.best_score = 0.0     # For accuracy, higher is better
        self.wait = 0
        
    def on_epoch_end(self, epoch, logs=None):
        current_score = logs.get(self.monitor)
        
        if current_score is None:
            # Try alternative metric names
            alt_monitor = self.monitor.replace('val_', '')
            current_score = logs.get(alt_monitor)
            
            if current_score is None:
                print(f"Epoch {epoch+1}: {self.monitor} not found in logs. Available metrics: {list(logs.keys())}")
                return
            
        # Check if improved by at least min_improvement
        if current_score > self.best_score + self.min_improvement:
            self.best_score = current_score
            self.wait = 0
            print(f"Epoch {epoch+1}: ✅ Improvement detected! {self.monitor}: {current_score:.4f} (best: {self.best_score:.4f})")
        else:
            self.wait += 1
            improvement_needed = self.best_score + self.min_improvement
            print(f"Epoch {epoch+1}: ❌ Insufficient improvement. {self.monitor}: {current_score:.4f} (needs: {improvement_needed:.4f}) Wait: {self.wait}/{self.patience}")
            
        # Stop training if patience exceeded
        if self.wait >= self.patience:
            print(f"\n🛑 Early Stopping! Stopped at epoch {epoch+1}")
            print(f"Best {self.monitor}: {self.best_score:.4f}")
            self.model.stop_training = True