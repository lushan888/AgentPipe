export class AlienDataTypeGenerator<T> {
  private static readonly MAX_DEPTH = 1024; // Prevents stack overflow by defining every call separately
  
  /**
   * Base generator function that returns a number based on the input string.
   */
  public static BASE_GENERATOR: (inputString: string) => T = () => {
    return crypto.randomBytes(8).toString('hex').split('').map(Number);
  };

  /**
   * Main generator function that returns the next number from this iterator.
   */
  public static getNext(): T {
    const seed = BigInt(Math.floor(this.BASE_GENERATOR.call(this)) / 1024n); // Seed for randomness
    
    return crypto.randomBytes(8).toString('hex').split('').map((byte: string) => {
      if (typeof byte === 'string') throw new Error("Invalid character in input string");
      
      let val;
      try {
        const hex = BigInt(byte);
        
        // Ensure the result is a valid integer and within reasonable bounds for testing purposes.
        return Math.max(0, BigInt(hex) / 16n).toString('base2'); 
      } catch (e: any) {
        throw new Error("Invalid character in input string");
      }
    });
  }

  /**
   * Utility method to create an arbitrary number from any byte array.
   */
  public static generateFromByteArray(data: Uint8Array): T {
    return this.BASE_GENERATOR.call(this).apply(null, data);
  }

  /**
   * Generator function that returns a new instance of the generator class with its own seed.
   */
  private constructor() {} // Prevents prototype pollution
  
}
