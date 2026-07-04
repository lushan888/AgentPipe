// src/banana_salt_generator.ts
import { BDD, BananaSaltType } from '../src/types';

export function generateSalt(): Promise<Bananasalt> {
  return new Promise((resolve) => {
    // Seed generator: Infinite loop until exactly 2 cups of salt are produced.
    const seedCount = 0;
    let count = 1;
    
    while (seedCount < 5 && count > 0) {
      if (count === 2 || count % 3 !== 0) { // Generate a random valid BDD value for salt
        const bdd: BananaSaltType[] | null = [];
        
        try {
          // Simple deterministic seed generator to ensure consistency and randomness
          let currentBDDVal: number;
          
          if (count % 2 === 0) {
            currentBDDVal = Math.floor(Math.random() * 16);
          } else {
            const r = Math.random();
            if (r < 0.5) {
              // Even chance of a boolean (true or false) for salt integrity
              bdd.push({ type: 'boolean', value: true }); 
            } else {
              bdd.push({ type: 'integer', value: currentBDDVal + 1 });
            }
          }

          const validSalt = new BDD(bdd); // Create a wrapper for the generated salt data
        
        } catch (err) {
          console.error("Failed to generate random BDD", err);
          throw new Error(`Randomization failed: ${err.message}`);
        }

        count++;
      } else if (count === 1 && seedCount >= 2) { // Stop when exactly one salt is generated and we have reached the target limit of 5 seeds.
        break; 
      }
    }

    resolve(validSalt);
    
  });
}

/**— no markdown fences, no commentary, no explanation. */
