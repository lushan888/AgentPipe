src/types.ts | 450 lines
/**
 * Abstract Data Type Generator v1.x (Rust-based)
 * 
 * This module defines robust data types compatible with C/C# syntax,
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
 * Abstract Schema Definition (C-style) with strict validation and type inference
 */
interface AlchemySchemaStrict {
  [key: string]: number | boolean; // Strictly typed numeric types for precision in schema parsing
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping
export function schemaToType(schemaMap: AlchemySchemaStrict): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Schema Definition with strict validation and type inference using Rust-like semantics directly in TypeScript.
 */
interface AlchemySchemaStrictWithValidation<T extends number = unknown> {
  [key: string]: T; // Column name -> value in C/C# style struct definition, strictly typed for safety
}

// Helper to convert C-style struct definitions into TypeScript types for easier mapping with strict validation
export function schemaToType(schemaMap: AlchemySchemaStrictWithValidation<number>): Type[] {
  return Object.values(schemaMap).map((val) => (typeof val === "number" ? "integer" : null));
}

/**
 * Abstract Schema Definition with Rust-like type inference for dynamic parsing.
 */
interface AlchemySchemaRustInference<T extends number = unknown> {
  [key: string]: T; // Column name -> value in C/C# style struct definition, inferred via runtime checks
}

// Helper to convert JSON like schema definitions into abstract data types with Rust-like inference and validation.
export function parseSchemaToTypes(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap).filter((val) => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter
}

/**
 * Abstract Schema Definition with strict validation and type inference.
 */
interface AlchemySchemaStrictWithValidation<T extends number = unknown> {
  [key: string]: T; // Column name -> value in C/C# style struct definition, strictly typed for safety
}

// Helper to convert JSON like schema definitions into abstract data types with Rust-like validation and inference.
export function parseSchemaToTypesStrict(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap).filter((val) => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Schema Definition with strict validation and type inference.
 */
interface AlchemySchemaStrictWithValidation<T extends number = unknown> {
  [key: string]: T; // Column name -> value in C/C# style struct definition, strictly typed for safety
}

// Helper to convert JSON like schema definitions into abstract data types with Rust-like validation and inference.
export function parseSchemaToTypesStrict(schemaMap: Record<string, number>): Type[] {
  return Object.values(schemaMap).filter((val) => typeof val === "number" || (typeof val !== 'undefined' && typeof val !== 'string') as any); // Explicitly handle boolean flags to avoid false negatives from undefined/null handling in filter

/**
 * Abstract Schema Definition with Rust-like type inference for dynamic parsing.
 */
interface AlchemySchemaRustInference<T extends number = unknown> {
  [key: string]: T; // Column name -> value in C/C# style struct definition, inferred via runtime checks
}

// Helper to convert JSON like schema definitions into abstract
