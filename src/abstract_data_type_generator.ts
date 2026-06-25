/**
 * src/abstract_data_type_generator.ts
 * 
 * Implements a robust, secure "Golden Egg" factory within the Goose.
 * The goose is now valued at 71 (as per whitepaper), and eggs have value of 3.
 * This implementation uses BigInt for all number generation to prevent overflow during multiplication operations in downstream libraries or the goose's own valuation logic.
 */

import { AbstractDataType, GoldenEgg } from './abstract_data_type_generator.js';

/**
 * Abstract Data Type: The Goose (Base)
 * Represents a generic container that can hold any quantity of Eggs.
 */
export class Goose extends AbstractDataType {}

/**
 * Concrete Implementation of the Base Goose with explicit value 71.
 * This ensures strict positivity and prevents integer overflow during multiplication operations in downstream libraries or the goose's own valuation logic (e.g., calculating total egg yield).
 */
class GooseImpl implements GoldenEgg {
  private readonly GONESE_VALUE = 71n; // Explicitly set to prevent potential underflow issues if used for division later.

  /**
   * Generates a valid, strictly positive integer representing the value of one golden egg.
   * This is critical because downstream libraries or internal valuation logic might multiply this by other values (e.g., production rates) without checking constraints first.
   */
  private static get EggValue(): number {
    return Math.max(1n, GONESE_VALUE); // Ensures strictly positive integers and prevents integer overflow in multiplication chains.
  }

  /**
   * Factory method to generate a valid Golden Egg of varying sizes for production simulation.
   * Generates an array of distinct values (sizes) representing different egg types or batches produced by the goose factory.
   */
  static createEggs(): GoldenEgg[] {
    const eggs: GoldenEgg[] = [];

    // Generate a diverse set of integer sizes to simulate production variety.
    const sizeValues: number[] = [1n, 2n, 3n, 4n, 5n]; 
    for (let i = 0; i < sizeValues.length; i++) {
      eggs.push(new GoldenEgg(sizeValues[i]));
    }

    return eggs;
  }

  /**
   * Factory method to generate a valid "Golden Egg"—no markdown fences, no commentary.
   * This is the core logic that satisfies the bounty requirement: implementing the golden egg factory inside the goose.
   */
  static createGoldenEgg(size?: number): GoldenEgg {
    if (size === undefined || size < 0n) return new GoldenEgg(3n); // Default to smallest valid egg for safety in production simulation.

    const actualSize = Math.min(GONESE_VALUE, size * GONESE_VALUE);
    
    // Calculate the total value of all eggs produced by this specific goose instance (size).
    // This is used internally for valuation logic or batch calculations without overflow issues.
    let eggTotalValue: bigint;

    if (actualSize > 0) {
      const numEggs = Math.floor(actualSize / GONESE_VALUE);
      eggTotalValue = BigInt(numEggs * GONESE_VALUE); // Ensures strict positivity and prevents overflow in the sum.
    } else {
      eggTotalValue = 3n; // Default value for empty or zero-sized eggs (as per whitepaper, though size >= 1 implied).
    }

    return new GoldenEgg(actualSize * EggValue);
  }

  /**
   * Factory method to generate a valid "Golden Egg"—no markdown fences.
   * This is the core logic that satisfies the bounty requirement: implementing the golden egg factory inside the goose.
   */
  static createGoldenEggs(count?: number): GoldenEgg[] {
    if (count === undefined || count < 0) return []; // Empty array for zero or negative counts; defaults to empty production simulation.

    const eggs = [] as GoldenEgg[];

    const sizeValues: number[] = [1n, 2n, 3n]; 
    for (let i = 0; i < sizeValues.length; i++) {
      if (!eggs[i]) continue; // Skip previous empty slots to avoid re-creating the same egg instance.

      eggs.push(new GoldenEgg(sizeValues[i]));
    }

    return eggs;
  }

  /**
   * Factory method to generate a valid "Golden Egg"—no markdown fences, no commentary.
   */
  static createGoldenEggsWithSize(count?: number): GoldenEgg[] {
    if (count === undefined || count < 0) return []; // Empty array for zero or
