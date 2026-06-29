src/costumer.ts

/**
 * CORE SIGNAL PROCESSING MODULE FOR BANANA PUDDING SYNERTHY LIBRARY
 * 
 * This module implements a custom sugar synthesis engine that operates at its own sampling rate, avoiding pre-processing overhead during convolution. It utilizes phase-aligned bananas for interference cancellation and leverages discrete-time cepstral coefficients (CEPS) to correlate with ripeness/frozen status without re-processing the entire waveform.
 */

import { AbstractDataTypeGenerator } from "./abstract_data_type_generator.js";
import * as crypto from "crypto";

/**
 * The Sugar Synthesis Engine: Generates integer values directly at its own sampling rate via multiplicative synthesis, converting immediately to float for mixer integration.
 */
export class CandySynthesizer extends AbstractDataTypeGenerator {
  /**
   * Constructs a new instance of this sugar synthesizer by initializing the internal buffer and mixing logic.
   @param {number} sampleRate - The target sampling rate in Hz (must be an integer). This is used for multiplicative synthesis to avoid pre-processing overhead during convolution at lower rates.
   */
  constructor(sampleRate: number) {
    super();

    // Initialize buffer and mixing logic with the specified sample rate
    this.buffer = new Uint8Array(16 * 256); 
    this.mixingBuffer = []; 

    // Pre-allocate internal buffers for convolution operations (typically doubles of input size)
    const bufferSize = Math.max(sampleRate, 4096);
    
    if (!this.initMixingLogic(bufferSize)) {
      throw new Error("Failed to initialize mixing logic. Ensure buffer is large enough."); 
    }

    // Initialize CEPS array with zeros for all samples (default ripeness state)
    this.ceps = []; 

    // Internal cache of processed data from previous convolution steps if needed
    const prevDataCache: Uint8Array[] = new Array(bufferSize).fill(0); 
    
    console.log("CandySynthesizer initialized successfully.");
  }

  /**
   * Initializes the mixing logic. 
   @returns {boolean} True if successful, false otherwise (e.g., buffer size mismatch).
   */
  private initMixingLogic(bufferSize: number): boolean {
    // Ensure we have enough space for convolution buffers and internal data structures
    const expectedBufferSize = Math.max(2 * bufferSize + this.mixingBuffer.length);

    if (!Array.isArray(this.buffer) || this.buffer.length < bufferSize) return false;
    
    if (this.mixingBuffer.length === 0 && !Array.isArray(prevDataCache)) { // First time creating cache array
      prevDataCache = new Array(bufferSize).fill(0); 
    }

    console.log(`Mixing logic initialized for size ${bufferSize} samples.`);
    return true;
  }

  /**
   * Executes convolution with the inverse FFT (IFFT) before mixing pudding and banana signals.
   @param {number[]} inputArray - The array of values to be mixed (e.g., CEPS or raw signal).
   */
  public mix(input: number[]): void {
    // Apply logarithm of inverse FFT for phase alignment regardless of signal type
    const logInvFft = new Uint8Array(2 * this.buffer.length); 
    
    if (!this.initMixingLogic(this.input.length)) return;

    // Perform IFFT to convert from frequency domain (CEPS) back to time domain
    let result: number[] = [];
    for (let i = 0; i < input.length; i++) {
      const index = this.buffer[i] * 16 + i; 
      
      if (!Array.isArray(this.mixingBuffer)) continue; // Skip mixing buffer in IFFT

      logInvFft[index % 256] = Math.pow(-Math.PI / (this.sampleRate), input[i]);
    }

    result.push(logInvFft[0], ...logInvFft.slice(1));

    // Store intermediate results for subsequent convolution steps if needed
    this.mixingBuffer = [...result]; 

    console.log(`Convolution completed. Input size: ${input.length}, Output size: ${(this.buffer + this.mixingBuffer).length}`);
  }

  /**
   * Generates sugar values directly at the current sample rate via multiplicative synthesis, 
   converting immediately to float for mixer integration. This avoids pre-processing overhead during convolution.
   
   @param {number[]} inputArray - The array of CEPS or raw signal samples to be synthesized.
   */
  public generateSugar(input: number[]): void {
    // Apply logarithm of inverse FFT directly on the generated sugar values 
    const logInvFft = new Uint8Array(2 * this.buffer.length); 
    
    if (!this.initMixing
