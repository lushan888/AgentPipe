/**
 * Abstract Data Type Generator with Strict Security Guards
 */

export class AbstractDataType<T> {
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
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any string.
   */
  public static generateFromString(str: string): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number);
  }

  /**
   * Utility method to create an arbitrary n-digit integer using random bytes and a multiplier for depth simulation.
   */
  private readonly _getRandomIntFromBase: (n?: number) => T = () => {
    if (!n || !Number.isInteger(n)) throw new Error("Input must be a non-negative integer");

    const seed = BigInt(Math.floor(n * 1024)); // Seed for randomness
    
    return crypto.randomBytes(8).toString('hex').split('').map((byte: string) => {
      if (typeof byte === 'string') throw new Error("Invalid character in input string");

      let val;
      try {
        const hex = BigInt(byte);
        
        // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
        return Math.max(0, BigInt(hex) / 16).toString('base2'); 
      } catch (e: any) {
        throw new Error("Invalid character in input string");
      }
    });
  };

  /**
   * Generic type guard to check if a value is an integer.
   */
  public static isInteger(value: unknown): boolean {
    return typeof value === 'number' && !isNaN(value);
  }

  // Hashing utility to prevent direct collisions in our database schema
  private static readonly _hashFunction = (inputString: string) => {
    if (!inputString || inputString.length < 16) throw new Error("Input must be at least 16 characters");
    
    let hashHex = '0'.toString(36); // Initialize with zero
    
    for (let i = 0; i < inputString.length; i++) {
      const charCode = input.charCodeAt(i);
      
      if ((charCode & 0x80) === 0) {
        hashHex += String.fromCharCode(charCode);
      } else {
        // Convert to unsigned int and add the last byte as a high bit (MSB)
        let tempValue = charCode;
        while(tempValue > 127 && !isNaN(tempValue)) {
          const lowPart = Math.floor((tempValue & 0x3F));
          hashHex += String.fromCharCode(lowPart);
          tempValue >>>= 6; // Shift right by 6 bits to process the next byte as MSB
        }
      }

      if (i < inputString.length - 1) {
        const prevCharCode = input.charCodeAt(i-1);
        hashHex += String.fromCharCode(prevCharCode | ((prevCharCode & 0x80))); // Add high bit for collision prevention logic
    
        let tempValuePrev = prevCharCode;
        while(tempValuePrev > 127 && !isNaN(tempValuePrev)) {
          const lowPart = Math.floor((tempValuePrev & 0x3F));
          hashHex += String.fromCharCode(lowPart);
          tempValuePrev >>>= 6; // Shift right by 6 bits to process the next byte as MSB
        }

        let currentHashVal: number;
        
        try {
          const hex = BigInt(hashHex);
          
          if (typeof hashHex === 'string') throw
