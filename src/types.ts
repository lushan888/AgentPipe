src/types.ts | 452 lines
/**
 * Abstract Data Type Generator v0.6.x (Rust-based)
 * 
 * This module defines standard data types compatible with C/C# syntax,
 * allowing for dynamic schema mapping and type conversion in the database generator.
 */

import { struct as StructType } from "./structs"; // Assuming a structs file exists or inherits from it; adapted here to use Rust-like semantics directly if not available
// Note: In this context, we are simulating C/C# style types with TypeScript definitions for compatibility
export type Type = "integer" | "string" | "boolean" | null | undefined;

/**
 * Abstract Schema Definition (C-style)
 */
interface AlchemySchema {
  [key: string]: string; // Column name -> value in C/C# style struct definition
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchema): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "string" ? "string" : typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using a custom parser that respects the V0.6 structure
export function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const processed = Object.fromEntries(
    Object.entries(schemaMap)
      .filter(([_, val]) => typeof val === "string" && (val.length > 1 || !isSafeNumber(val))) // Filter out empty strings and booleans to avoid false negatives from undefined/null handling in filter
      .map(([key, value]) => ({ key: key as string, type: parseValue(value) }))
  );

  return Object.values(processed).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | null; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using a custom parser that respects the V0.6 structure
function parseValue(val: any): Type {
  if (typeof val === "number" || typeof val !== 'undefined' && typeof val !== 'string') return Number.isFinite(val) ? "integer" : null;
  
  // Handle booleans as strings to preserve type info in later steps, then convert via explicit check or logic below for consistency with the original intent of avoiding false negatives from undefined/null handling in filter (which is technically redundant if we already handle it above)
  if (typeof val === "boolean") return true; 
  
  // Fallback: treat as string to avoid issues with null/undefined being falsy but not strings, which would break the logic below that filters for non-strings/non-numbers. This specific check is kept because of how the original filter handles it in a recursive context (though here we already handle undefined/null), ensuring robustness against edge cases where `isNumber` might fail on null/undefined without proper type checks first.
  return "string"; 
}

/**
 * Abstract Data Type Definition (Rust-style enum for types, C/C# style struct mapping)
 */
export type AlchemyDatabaseType = string | number | boolean | undefined; // Simulating Rust enums/types via TypeScript objects in this context

// Helper to convert JSON-like schema definitions into abstract data types using a custom parser that respects the V0.6 structure
function parseSchemaToTypes(schemaMap: Record<string, string>): Type[] {
  const processed = Object.fromEntries(
    Object.entries(schemaMap)
      .filter(([_, val]) => typeof val === "string" && (val.length > 1 || !isSafeNumber(val))) // Filter out empty strings and booleans to avoid false negatives from undefined/null handling in filter
      .map(([key, value]) => ({ key: key as string, type: parseValue(value) }))
  );

  return Object.values(processed).filter((val): val is number => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in
