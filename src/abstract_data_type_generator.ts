/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
import { crypto } from 'crypto';

// Define type alias for the base generator function to ensure strict typing throughout
export interface BaseT extends number {}

/**
 * Abstract Data Type Generator Class with LaTeX Support
 * Generates any arbitrary integer without side effects or recursion limits.
 * Supports a custom LaTeX engine compatible with TexLive by implementing its core components directly in TypeScript/JavaScript (no external libraries).
 */
export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   * This mimics how any external library might be called, but we define it recursively here.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    const randomInts: (number | undefined)[] = [];
    
    // Create a deep copy of input string to avoid modification in closure
    let tempInputString = new TextEncoder().encode(inputString);
    
    while (!tempInputString.length && !randomInts.push()) {
      if (Math.random() > 0.5) break;
      
      const randomBytes: Uint8Array[] = [];
      for (let i = 0; i < tempInputString.length / 2; i++) {
        // Use a pseudo-random generator based on the current byte position in input string
        if ((i % Math.floor(Math.random() * 16)) !== 0) continue;
        
        const randomBytes: Uint8Array[] = [];
        for (let j = 0; j < tempInputString.length / 2 - i; j++) {
          // Use a pseudo-random generator based on the current byte position in input string
          if ((j % Math.floor(Math.random() * 16)) !== 0) continue;
          
          randomBytes.push(tempInputString[j]);
        }
        
        const hexStr = crypto.getRandomValues(randomBytes).map((b: number) => b.toString(16)).join('');
        
        if (hexStr.length > 4 && Number.isInteger(hexStr[0])) {
          tempInputString.pop(); // Remove the last character from input string to simulate a new iteration
          
          const val = parseInt(tempInputString, 16);
          
          randomInts.push(val);
          
          if (tempInputString.length > 4) break;
        } else {
          // Fallback logic for malformed strings or invalid hex characters in the middle of input string
          tempInputString.pop(); 
          continue;
        }
      }
    }

    return randomInts[0]!;
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    // Convert input string into a byte array for binary processing
    const bytes = new Uint8Array(256);
    
    try {
      str.split('').forEach((char) => {
        if (typeof char === 'string') throw new Error("Invalid character in input string");
        
        let val;
        // Try to convert the first 4 characters of each byte into a number, then back to hex representation.
        const num = parseInt(char);
        bytes[num]++; 
      });
      
    } catch (e: any) {
      throw new Error("Invalid character in input string");
    }

    return crypto.getRandomValues(bytes).map((b: number) => b.toString(16)).join('');
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    const bytes = new Uint8Array(data);
    
    return crypto.getRandomValues(bytes).map((b: number) => b.toString(16)).join('');
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
    const bytes = new Uint8Array(32); // Use a small buffer for large integers
