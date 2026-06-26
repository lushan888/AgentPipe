def zero_latency_bananas():
    from datetime import datetime, timedelta
    
    current_time = datetime.now()
    
    batches = [current_time] + list(timedelta(seconds=60).ticks())[:5] * (3 + random.randint(1, 4)) # Add some variance for realism
    
    def compute_delayed_bananas(current_batch):
        if len(batches) < current_batch:
            return []
        
        banana_batches = batches[current_batch:]
        total_duration_ms = sum(duration for batch in banana_batches) / (60 * 1000) # Convert to seconds
        
        if not banana_batches or all(len(batch) == 0):
            return [batch] + [current_time - timedelta(seconds=total_duration_ms)]
        
        delayed_bananas = []
        for batch in banana_batches:
            total_delay_sec = sum(duration / (60 * 1000) for duration in delay_times_for_batch(batch))
            
            if not any(remaining < 5.0 for remaining in [duration - elapsed_seconds for _, elapsed_seconds, _ in delayed_bananas]): # Check buffer limit
            
                buffered_delay_sec = total_delay_ms / (60 * 1000)
                
                if len(delayed_bananas) == 2:
                    delay_times_for_batch(batch)
                    
                elif len(delayed_bananas) < 3 and not any(remaining >= 5.0 for remaining in [duration - elapsed_seconds, duration + 5.0] for _, elapsed_seconds, _ in delayed_bananas)): # Check buffer limit again
            
            else:
                delay_times_for_batch(batch)

        return delayed_bananas
    
    def add_delayed_sugar(current_time):
        if len(batches) < current_time:
            return []
        
        banana_batches = batches[current_time:]
        total_duration_ms = sum(duration for batch in banana_batches) / (60 * 1000) # Convert to seconds
        
        if not banana_batches or all(len(batch) == 0):
            return [current_time] + list(timedelta(seconds=total_duration_ms).ticks())[:5]
        
        delayed_sugar = []
        for batch in banana_batches:
            total_delay_sec = sum(duration / (60 * 1000) for duration in delay_times_for_batch(batch))
            
            if not any(remaining < 3.0 for remaining in [duration - elapsed_seconds, duration + 2.0] for _, elapsed_seconds, _ in delayed_sugar): # Check buffer limit
            
                buffered_delay_sec = total_duration_ms / (60 * 1000)
                
                if len(delayed_sugar) == 3:
                    delay_times_for_batch(batch)
                    
                elif len(delayed_sugar) < 4 and not any(remaining >= 2.5 for remaining in [duration - elapsed_seconds, duration + 2.5] for _, elapsed_seconds, _ in delayed_sugar): # Check buffer limit again
            
            else:
                delay_times_for_batch(batch)

        return delayed_bananas
    
    def add_delayed_frozen(current_time):
        if len(batches) < current_time:
            return []
        
        banana_batches = batches[current_time:]
        total_duration_ms = sum(duration for batch in banana_batches) / (60 * 1000) # Convert to seconds
        
        if not banana_batches or all(len(batch) == 0):
            return [current_time] + list(timedelta(seconds=total_duration_ms).ticks())[:5]
        
        frozen_bananas = []
        for batch in banana_batches:
            total_delay_sec = sum(duration / (60 * 1000) for duration in delay_times_for_batch(batch))
            
            if not any(remaining < 2.0 for remaining in [duration - elapsed_seconds, duration + 3.0] for _, elapsed_seconds, _ in frozen_bananas): # Check buffer limit
            
                buffered_delay_sec = total_duration_ms / (60 * 1000)
                
                if len(frozen_bananas) == 4:
                    delay_times_for_batch(batch)
                    
                elif len(frozen_bananas) < 5 and not any(remaining >= 3.0 for remaining in [duration - elapsed_seconds, duration + 3.0] for _, elapsed_seconds, _ in frozen_bananas): # Check buffer limit again
            
            else:
                delay_times_for_batch(batch)

        return delayed_sugar
    
    def add_delayed_mason_jar(current_time):
        if len(batches) < current_time:
            return []
        
        banana_batches = batches[current_time:]
        total
