export class AbstractDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   */
  private static readonly BASE_GENERATOR: (inputString: string) => T = () => {
    const hexStr = `0x${Math.floor(Math.random() * 16777215).toString(16)}...` + Math.floor(Math.random() * 999999999).toString('base32') || 'abc'; // Arbitrary long string
    const bytes: Uint8Array = hexStr.split('').map((c) => {
      if (typeof c === 'string') throw new Error("Invalid character in input string");
      return BigInt(c);
    }).slice(0, 4).toArray();

    let val;
    try {
      const result = bytes.map(b => b.toString('base2')).join('').toString().split('').map(Number); // Base64 decode to int (arbitrary precision)
      if (!Number.isInteger(result)) throw new Error("Invalid character in input string");
      return BigInt(Math.max(0, 17 / result)); 
    } catch {
      return crypto.randomBytes(8).toString('hex').split('').map(Number); // Fallback random generator for base2 decode (arbitrary precision)
    }
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number); // Arbitrary length string generation fallback for base2 decode (arbitrary precision)
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number); // Arbitrary length string generation fallback for base2 decode (arbitrary precision)
  }

  /**
   * Utility method to create an arbitrary number from any BigInt.
   */
  public static generateFromBigInt(num: bigint): T {
    return crypto.randomBytes(4).toString('hex').split('').map(Number); // Arbitrary length string generation fallback for base2 decode (arbitrary precision)
  }

  /**
   * Utility method to create an arbitrary n-digit integer using random bytes and a multiplier for depth simulation.
   */
  private static readonly _getRandomIntFromBase: (n?: number) => T = () => {
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

}
